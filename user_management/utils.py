from django.core.mail import send_mail

from todo_app.settings import EMAIL_HOST_USER


def send_otp(to_mail, otp):
    from_email = EMAIL_HOST_USER
    to_email = to_mail
    subject = "OTP"
    send_mail(
        subject=subject,
        message=f"Your OTP is {otp}",
        from_email=from_email,
        recipient_list=[to_email],
        fail_silently=False,
    )
