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
    LARGE_CAT_CHOICES = (
        ('소설', '한국소설'),
        ('소설', '고전소설'),
        ('소설', '영미소설'),
        ('소설', '일본소설'),
        ('소설', '미스터리/스릴러'),
        ('소설', '판타지소설'),
        ('소설', '드라마/영화 소설'),
        ('소설', 'sf/과학'),
        ('시에세이', '현대시'),
        ('시에세이', '한국에세이'),
        ('시에세이', '영미에세이'),
        ('시에세이', '테마에세이'),
        ('인문', '심리학'),
        ('인문', '철학'),
        ('인문', '인문교양'),
        ('인문', '글쓰기'),
        ('자기계발', '성공/처세'),
        ('자기계발', '자기능력계발'),
        ('자기계발', '화술'),
        ('자기계발', '마인드콘트롤/감정'),
        ('경제경영', '재테크/금융'),
        ('경제경영', '부동산'),
        ('경제경영', '마케팅/광고'),
        ('경제경영', '경영전략'),
        ('역사', '한국사'),
        ('역사', '세계사'),
        ('역사', '서양사'),
        ('역사', '역사기행'),
        ('정치사회', '정치'),
        ('정치사회', '사회학'),
        ('정치사회', '사회문제'),
        ('정치사회', '외교'),
        ('예술대중문화', '음악'),
        ('예술대중문화', '미술'),
        ('예술대중문화', '건반악기'),
        ('예술대중문화', '디자인/색채'),
        ('과학', '교양과학'),
        ('과학', '수학'),
        ('과학', '뇌과학'),
        ('기타', '요리'),
        ('기타', '건강'),
        ('기타', '여행'),
        ('기타', '가정/육아'),
        ('기타', '청소년'),
    )
    MIDDLE_CAT_CHOICES = (
        ('한국소설', '한국소설'),
        ('고전소설', '고전소설'),
        ('영미소설', '영미소설'),
        ('일본소설', '일본소설'),
        ('미스터리스릴러', '미스터리/스릴러'),
        ('판타지소설', '판타지소설'),
        ('드라마영화 소설', '드라마/영화 소설'),
        ('SF과학', 'sf/과학'),
        ('현대시', '현대시'),
        ('한국에세이', '한국에세이'),
        ('영미에세이', '영미에세이'),
        ('테마에세이', '테마에세이'),
        ('심리학', '심리학'),
        ('철학', '철학'),
        ('인문교양', '인문교양'),
        ('글쓰기', '글쓰기'),
        ('성공처세', '성공/처세'),
        ('자기능력계발', '자기능력계발'),
        ('화술', '화술'),
        ('마인드콘트롤감정', '마인드콘트롤/감정'),
        ('재테크금융', '재테크/금융'),
        ('부동산', '부동산'),
        ('마케팅광고', '마케팅/광고'),
        ('경영전략', '경영전략'),
        ('한국사', '한국사'),
        ('세계사', '세계사'),
        ('서양사', '서양사'),
        ('역사기행', '역사기행'),
        ('정치', '정치'),
        ('사회학', '사회학'),
        ('사회문제', '사회문제'),
        ('외교', '외교'),
        ('음악', '음악'),
        ('미술', '미술'),
        ('건반악기', '건반악기'),
        ('디자인색채', '디자인/색채'),
        ('교양과학', '교양과학'),
        ('수학', '수학'),
        ('뇌과학', '뇌과학'),
        ('요리', '요리'),
        ('건강', '건강'),
        ('여행', '여행'),
        ('가정육아', '가정/육아'),
        ('청소년', '청소년'),
    )
    large_category = models.CharField(max_length=200, blank=True, null=True, choices=LARGE_CAT_CHOICES)
    middle_category = models.CharField(max_length=300, blank=True, null=True, choices=MIDDLE_CAT_CHOICES)
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