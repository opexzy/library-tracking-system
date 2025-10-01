from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

@shared_task
def check_overdue_loans():
    now = timezone.now()
    try:
        overdue_books_loans = Loan.objects.filter(is_returned=False, due_date__gt=now).select_related('book','member__user')
        for overdue_book in overdue_books_loans:
            send_mail(
                subject=f'The Book: {overdue_book.book.title} is past return date',
                message=f'Hello {overdue_book.member.user.username},\n\nThe Book: {overdue_book.book.title}, loaned to you is past return date".\nKindly return it.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[overdue_book.member.user.email],
                fail_silently=False,
            )
    except Exception:
        pass