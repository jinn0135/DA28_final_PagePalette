from django.db import models

# 모델 가져오기
class UserInfo(models.Model):
    GENDER_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
    )
    AGE_CHOICES = (
        (10, '10대'),
        (20, '20대'),
        (30, '30대'),
        (40, '40대'),
        (50, '50대'),
        (60, '60대'),
    )
    email = models.CharField(primary_key=True, max_length=100)
    pw = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.IntegerField(choices=AGE_CHOICES)

    class Meta:
        managed = False
        db_table = 'user_info'

    def __str__(self):
        return self.email

class BookOption(models.Model):
    email = models.OneToOneField(UserInfo, models.DO_NOTHING, db_column='email', primary_key=True)
    book_service = models.IntegerField()
    large_category = models.CharField(max_length=200, blank=True, null=True)
    middle_category = models.CharField(max_length=300, blank=True, null=True)
    selected_book_isbn = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book_option'

class UserOption(models.Model):
    email = models.OneToOneField(UserInfo, models.DO_NOTHING, db_column='email', primary_key=True)
    TIME_CHOICES = (
        (0, '오전 7시'),
        (1, '오후 5시'),
    )
    WEEKEND_CHOICES = (
        (0, '주말 메일 받지 않기'),
        (1, '주말에도 메일 받기'),
    )
    BOOKSERVICE_CHOICES = (
        (0, '도서 서비스 받지 않기'),
        (1, '도서 서비스 구독 하기'),
    )
    reception_time = models.IntegerField(choices=TIME_CHOICES)
    weekend = models.IntegerField(choices=WEEKEND_CHOICES)
    book_service = models.IntegerField(choices=BOOKSERVICE_CHOICES)

    class Meta:
        managed = False
        db_table = 'user_option'

    def __str__(self):
        return self.email, self.book_service

# 여성, 나이대
class Female10(models.Model):
    agender_rank = models.IntegerField(blank=True, null=True)
    agender_isbn = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'female_10'

class Female20(models.Model):
    agender_rank = models.IntegerField(blank=True, null=True)
    agender_isbn = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'female_20'


class Female30(models.Model):
    agender_rank = models.IntegerField(blank=True, null=True)
    agender_isbn = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'female_30'


class Female40(models.Model):
    agender_rank = models.IntegerField(blank=True, null=True)
    agender_isbn = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'female_40'


class Female50(models.Model):
    agender_rank = models.IntegerField(blank=True, null=True)
    agender_isbn = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'female_50'


class Female60(models.Model):
    agender_rank = models.IntegerField(blank=True, null=True)
    agender_isbn = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'female_60'

# 남성, 나이대
class Male10(models.Model):
    agender_rank = models.IntegerField(blank=True, null=True)
    agender_isbn = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'male_10'


class Male20(models.Model):
    agender_rank = models.IntegerField(blank=True, null=True)
    agender_isbn = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'male_20'


class Male30(models.Model):
    agender_rank = models.IntegerField(blank=True, null=True)
    agender_isbn = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'male_30'


class Male40(models.Model):
    agender_rank = models.IntegerField(blank=True, null=True)
    agender_isbn = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'male_40'


class Male50(models.Model):
    agender_rank = models.IntegerField(blank=True, null=True)
    agender_isbn = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'male_50'


class Male60(models.Model):
    agender_rank = models.IntegerField(blank=True, null=True)
    agender_isbn = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'male_60'

# 도서 정보
class Gyobo13(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    large_category = models.CharField(max_length=200, blank=True, null=True)
    middle_category = models.CharField(max_length=300, blank=True, null=True)
    b_rank = models.SmallIntegerField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    count = models.SmallIntegerField(blank=True, null=True)
    isbn = models.BigIntegerField(blank=True, null=True)
    img = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gyobo_경제경영'


class Gyobo29(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    large_category = models.CharField(max_length=200, blank=True, null=True)
    middle_category = models.CharField(max_length=300, blank=True, null=True)
    b_rank = models.SmallIntegerField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    count = models.SmallIntegerField(blank=True, null=True)
    isbn = models.BigIntegerField(blank=True, null=True)
    img = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gyobo_과학'


class Gyobo(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    large_category = models.CharField(max_length=200, blank=True, null=True)
    middle_category = models.CharField(max_length=300, blank=True, null=True)
    b_rank = models.SmallIntegerField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    count = models.SmallIntegerField(blank=True, null=True)
    isbn = models.BigIntegerField(blank=True, null=True)
    img = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gyobo_기타'


class Gyobo01(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    large_category = models.CharField(max_length=200, blank=True, null=True)
    middle_category = models.CharField(max_length=300, blank=True, null=True)
    b_rank = models.SmallIntegerField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    count = models.SmallIntegerField(blank=True, null=True)
    isbn = models.BigIntegerField(blank=True, null=True)
    img = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gyobo_소설'


class Gyobo03(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    large_category = models.CharField(max_length=200, blank=True, null=True)
    middle_category = models.CharField(max_length=300, blank=True, null=True)
    b_rank = models.SmallIntegerField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    count = models.SmallIntegerField(blank=True, null=True)
    isbn = models.BigIntegerField(blank=True, null=True)
    img = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gyobo_시에세이'


class Gyobo19(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    large_category = models.CharField(max_length=200, blank=True, null=True)
    middle_category = models.CharField(max_length=300, blank=True, null=True)
    b_rank = models.SmallIntegerField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    count = models.SmallIntegerField(blank=True, null=True)
    isbn = models.BigIntegerField(blank=True, null=True)
    img = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gyobo_역사문화'


class Gyobo23(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    large_category = models.CharField(max_length=200, blank=True, null=True)
    middle_category = models.CharField(max_length=300, blank=True, null=True)
    b_rank = models.SmallIntegerField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    count = models.SmallIntegerField(blank=True, null=True)
    isbn = models.BigIntegerField(blank=True, null=True)
    img = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gyobo_예술대중문화'


class Gyobo05(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    large_category = models.CharField(max_length=200, blank=True, null=True)
    middle_category = models.CharField(max_length=300, blank=True, null=True)
    b_rank = models.SmallIntegerField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    count = models.SmallIntegerField(blank=True, null=True)
    isbn = models.BigIntegerField(blank=True, null=True)
    img = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gyobo_인문'


class Gyobo15(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    large_category = models.CharField(max_length=200, blank=True, null=True)
    middle_category = models.CharField(max_length=300, blank=True, null=True)
    b_rank = models.SmallIntegerField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    count = models.SmallIntegerField(blank=True, null=True)
    isbn = models.BigIntegerField(blank=True, null=True)
    img = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gyobo_자기계발'


class Gyobo17(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    large_category = models.CharField(max_length=200, blank=True, null=True)
    middle_category = models.CharField(max_length=300, blank=True, null=True)
    b_rank = models.SmallIntegerField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    count = models.SmallIntegerField(blank=True, null=True)
    isbn = models.BigIntegerField(blank=True, null=True)
    img = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gyobo_정치사회'