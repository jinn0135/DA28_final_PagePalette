from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True, max_length=100)
    pw = models.CharField(max_length=30)

    GENDER_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    AGE_CHOICES = (
        (10, '10대'),
        (20, '20대'),
        (30, '30대'),
        (40, '40대'),
        (50, '50대'),
        (60, '60대'),
    )
    age = models.CharField(max_length=3, choices=AGE_CHOICES)

    # create_at = models.DateTimeField(auto_now_add=True)
    # update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
    # class Meta:
    #     db_table = 'users' # forms.py에 작성 됨


class UserOption(models.Model):
    email = models.EmailField(unique=True, max_length=100)

    TIME_CHOICES = (
        (0, '오전 7시'),
        (1, '오후 5시'),
    )
    WEEKEND_CHOICES = (
        (0, '주말메일 받지 않기'),
        (1, '주말에도 메일 받기'),
    )
    BOOKSERVICE_CHOICES = (
        (0, '도서 서비스 받지 않기'),
        (1, '도서 서비스 구독 하기'),
    )
    reception_time = models.CharField(max_length=1, choices=TIME_CHOICES)
    weekend = models.CharField(max_length=1, choices=WEEKEND_CHOICES)
    book_service = models.CharField(max_length=1, choices=BOOKSERVICE_CHOICES)

    def __str__(self):
        return self.email, self.book_service

class BookService(models.Model):
    email = models.EmailField(unique=True, max_length=100)
    # book_service =
    # large_category =
    # middle_category =
    # selected_book_isbn =