import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK


@pytest.mark.django_db
def test_view_drones_get(client):
    url = reverse('drone:view_drones')
    r = client.get(url)
    assert r.status_code == HTTP_200_OK


def test_get_drone_info_get(client):
    url = reverse('drone:get_drone_info', kwargs={'pk': 1})
    r = client.get(url)
    assert r.status_code == HTTP_200_OK

