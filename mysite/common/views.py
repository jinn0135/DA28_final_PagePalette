from django.shortcuts import render, redirect
# import json, re, traceback
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
import pandas as pd
# from django.views import View
# from django.core.exceptions import ValidationError
# from django.db.models import Q
from .models import UserInfo, UserOption, BookOption
from .forms import SignupForm, SubscribeForm

# Create your views here.

def LogIn(request):
    if request.method == "POST":
        email = request.POST.get('email')
        pw = request.POST.get('pw')
        try:
            # UserInfo 모델에서 해당 이메일과 비밀번호 확인
            user = UserInfo.objects.get(email=email)
            if user.pw == pw:
                # 로그인 성공
                request.session['user_id'] = user.email
                return redirect('main:main')
            else:
                # 비밀번호가 일치하지 않다면
                error_message = '이메일과 비밀번호를 확인해주세요'
                return render(request, 'common/login.html', {'error_message': error_message})
        except UserInfo.DoesNotExist:
            error_message = '존재하지 않는 이메일입니다'
            return render(request, 'common/login.html', {'error_message': error_message})
    else:
        return render(request, 'common/login.html')

def LogOut(request):
    # 로그아웃 처리
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('main:main')

# 가입 페이지
def SignUp(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if UserInfo.objects.filter(email=email).exists():
                messages.error(request, '이미 가입된 이메일입니다.')
                return render(request, 'common/signup.html', {'form':form})
            else:
                # 추가 유효성 검사
                age = form.cleaned_data['age']
                gender = form.cleaned_data['gender']
                if not age or gender is None:
                    messages.error(request, '성별과 연령대를 선택해주세요.')
                    return render(request, 'common/signup.html', {'form':form})
                form.save()
                return redirect('common:login')

    else:
        form = SignupForm()

    return render(request, 'common/signup.html', {'form':form})

def Subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = request.session.get('user_id')
            form.instance.email = UserInfo.objects.get(email=email)
            form.save()
            book_service = form.cleaned_data['book_service']
            if book_service == '0':
                # 뉴스만 구독하기 선택 시
                msg = '뉴스 구독이 완료되었습니다.'
                print(form.errors)
                return render(request, 'common/subscribe_success.html', {'msg':msg})
            elif book_service == '1':
                # 책도 같이 구독하기 선택 시
                return render(request, 'common/subscribe_book.html')
            else:
                return render(request, 'common/subscribe.html')
        else:
            print(form.errors)
    else:
        form = SubscribeForm()
    return render(request, 'common/subscribe.html', {'form':form})

from .select_books import sortBook
def subscribe_book(request):
    email = request.session.get('user_id')
    book_service = True
    # to DB
    return render(request, 'common/subscribe_book.html', {'result':''})

def subscribe_book2(request):
    genrid_dic = {'01': [i for i in range(1, 9)], '03': [i for i in range(1, 5)],
                  '05': [i for i in range(1, 5)], '13': [i for i in range(1, 5)],
                  '15': [i for i in range(1, 5)], '17': [i for i in range(1, 5)],
                  '19': [i for i in range(1, 5)], '23': [i for i in range(1, 5)],
                  '29': [i for i in range(1, 4)], '00': [i for i in range(1, 6)],
                  }
    id2g = {'01':'소설', '03':'시에세이', '05':'인문', '13':'경제경영',
            '15':'자기계발', '17':'정치사회', '19':'역사문화',
            '23':'예술대중문화', '29':'과학', '00':'기타'}

    g1s, g2s = [], []
    for g1_id, g2ids in genrid_dic.items():
        for g2_id in g2ids:
            input_genre = request.POST.get('{}_{}'.format(g1_id,g2_id),'')
            if input_genre=='': continue
            else:
                g1s.append(id2g[g1_id])
                g2s.append(input_genre)


    large_category = ','.join(g1s)
    middle_category = ','.join(g2s)
    dic = {'large_category': large_category, 'middle_category': middle_category}
    user_info = pd.DataFrame(dic, index=[0])
    select = sortBook(user_info)
    result_df = select()
    books = []
    for row in result_df.itertuples():
        books.append({'img_url': row.img,'title': row.title,
                      'author': row.author,'isbn': row.isbn,
                      'order': row.order})

    email = request.session.get('user_id')
    user = UserInfo.objects.get(email=email)  # UserInfo 인스턴스 가져오기
    book_service = True
    #large_category = ','.join(g1s)
    #middle_category = ','.join(g2s)
    #selected_book_isbn = request.POST.get('selected_book_isbn', '')

    # BookOption 모델에 값 저장
    book_option, created = BookOption.objects.update_or_create(
        email=user,
        book_service = True,
        defaults={
            'large_category': large_category,
            'middle_category': middle_category,
            #'selected_book_isbn': selected_book_isbn
        }
    )
    return render(request, 'common/subscribe_book2.html', {'result':books})

def subscribe_success(request):
    titles = []
    for i in range(1, 13):
        title = request.POST.get('count{}'.format(i), '')
        if title != '':
            titles.append(str(int(title.split('.')[0])))
    selected_book_isbn = ','.join(titles)
    email = request.session.get('user_id')
    user = UserInfo.objects.get(email=email)

    # BookOption 모델에 값 저장
    book_option, created = BookOption.objects.update_or_create(
       email=user,
        defaults={
            'selected_book_isbn': selected_book_isbn
        }
    )

    msg = '뉴스와 도서 구독이 완료되었습니다.'
    return render(request, 'common/subscribe_success.html', {'msg':msg})

