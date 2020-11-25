import os
from io import BytesIO
from django.conf import settings
from django.core.mail import EmailMessage
from celery import task
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Order


@task
def send_order_status_to_email(pk, status):
    try:
        order = Order.objects.get(pk=pk)
        subject = 'Rent-a-drone Order detail'
        if status == 'paid':
            title = 'Paid Order Notification!'
            message = f'Your Order #{order.pk} is successfully paid. Enjoy driving & good luck!'
        elif status == 'finished':
            title = 'Finished Order Notification!'
            message = f'Your Order #{order.pk} is finished. Thank you for using our Rent-a-drone service!'
        else:
            title = 'Canceled Order Notification!'
            message = f'Your Order #{order.pk} is canceled. Best regards from our team!'
        if os.name == 'posix':
            os.system(f'notify-send "{title}" "You have canceled the Order #{order.pk}"')
        else:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=3)

        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.user.email])
        email.send()
        return True
    except Exception as e:
        return str(e)


@task
def send_pdf_to_email(pk):
    try:
        order = Order.objects.get(pk=pk)
        html = render_to_string('order/order_detail_pdf.html', {'order': order})
        out = BytesIO()
        HTML(string=html).write_pdf(out)

        subject = 'Rent-a-drone Order detail'
        message = f'We approved your Order #{order.pk}. You can see Order detail in PDF attachment. ' \
                  'Thank you for using our Rent-a-drone service!'
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.user.email])
        email.attach('Order #{}_{}.pdf'.format(order.pk, order.drone.name),
                     out.getvalue(), 'application/pdf')
        email.send()
        return True
    except Exception as e:
        return str(e)




