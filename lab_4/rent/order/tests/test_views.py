from datetime import timedelta
import pytest
from django.db.models import Avg
from django.urls import reverse
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED,\
    HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient
from drone.models import Drone
from order.models import Coupon, Order

username = 'test_user'
password = 'test_pass'


@pytest.fixture
def test_user(django_user_model):
    return django_user_model.objects.create_user(username=username,
                                                 password=password)


def test_create_valid_order(test_user):
    drone = drone.objects.create(name='test_drone', model_year='2014',
                             price_hourly=10)
    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    data = {'end_date': '2018-09-09',
            'total_price': 100,
            'pk': drone.pk
           }
    url = reverse('order:create')
    r = client.post(url, data=data)
    assert r.status_code == HTTP_201_CREATED


def test_create_invalid_order(test_user):
    drone = drone.objects.create(name='test_drone', model_year='2014',
                             price_hourly=10)
    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    data = {'total_price': 100,
            'pk': drone.pk
           }
    url = reverse('order:create')
    r = client.post(url, data=data)
    assert r.status_code == HTTP_400_BAD_REQUEST


def test_create_order_unauthorized(test_user):
    drone = drone.objects.create(name='test_drone', model_year='2014',
                             price_hourly=10)
    client = APIClient()
    data = {'end_date': '2018-09-09',
            'total_price': 100,
            'pk': drone.pk
            }
    url = reverse('order:create')
    r = client.post(url, data=data)
    assert r.status_code == HTTP_401_UNAUTHORIZED


def test_valid_coupon_code(test_user):
    now = timezone.now()
    coupon = Coupon.objects.create(expired=now + timedelta(days=1),
                                   discount=10)
    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    data = {'code': coupon.code}
    url = reverse('order:check_coupon')
    r = client.post(url, data=data, format='json')
    assert r.json().get('status') == 'valid'


def test_invalid_coupon_code(test_user):
    now = timezone.now()
    coupon = Coupon.objects.create(expired=now + timedelta(days=1),
                                   discount=10)
    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    data = {'code': coupon.code + '1'}
    url = reverse('order:check_coupon')
    r = client.post(url, data=data, format='json')
    assert r.json().get('status') == 'invalid'


def test_expired_coupon_code(test_user):
    now = timezone.now()
    coupon = Coupon.objects.create(expired=now + timedelta(days=-1),
                                   discount=10)
    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    data = {'code': coupon.code}
    url = reverse('order:check_coupon')
    r = client.post(url, data=data, format='json')
    assert r.json().get('status') == 'expired'


def test_get_pending_orders(test_user):
    drone = drone.objects.create(name='test_drone', model_year='2014',
                             price_hourly=10)
    order = Order.objects.create(end_date='2018-09-09', drone=drone,
                                 user=test_user, approved=False, canceled=False,
                                 finished=False, paid=False)
    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    url = reverse('order:get_orders')
    r = client.get(url)
    assert r.json()[0].get('id') == order.id


def test_get_active_orders(test_user):
    drone = drone.objects.create(name='test_drone', model_year='2014',
                             price_hourly=10)
    order = Order.objects.create(end_date='2018-09-09', drone=drone,
                                 user=test_user, approved=True, canceled=False,
                                 finished=False, paid=False)
    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    url = reverse('order:get_orders')
    r = client.get(url + '?active=True')
    assert r.json()[0].get('id') == order.id


def test_get_finished_orders(test_user):
    drone = drone.objects.create(name='test_drone', model_year='2014',
                             price_hourly=10)
    order = Order.objects.create(end_date='2018-09-09', drone=drone,
                                 user=test_user, approved=True, paid=True,
                                 finished=True, canceled=False)
    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    url = reverse('order:get_orders')
    r = client.get(url + '?finished=True')
    assert r.json()[0].get('id') == order.id


def test_cancel_order(test_user):
    drone = drone.objects.create(name='test_drone', model_year='2014',
                             price_hourly=10)
    order = Order.objects.create(end_date='2018-09-09', drone=drone,
                                 user=test_user, approved=True)
    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    url = reverse('order:cancel_order', kwargs={'pk': order.pk})
    r = client.put(url)
    assert r.status_code == 200
    assert r.json().get('canceled')


def test_rate_drone(test_user):
    drone = drone.objects.create(name='test_drone', model_year='2014',
                             price_hourly=10)
    order = Order.objects.create(end_date='2018-09-09', drone=drone,
                                 user=test_user, approved=True, paid=True)
    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    url = reverse('order:rate_drone', kwargs={'pk': order.pk})
    data = {'rate': 5}
    r = client.put(url, data=data, format='json')
    assert r.status_code == 200
    assert r.json().get('rated')
    assert drone.orders.aggregate(rate=Avg('rate')).get('rate') == 5





