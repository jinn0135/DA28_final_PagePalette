from django.shortcuts import render, redirect
# import json, re, traceback
from django.http import JsonResponse, HttpResponse
# from django.views import View
# from django.core.exceptions import ValidationError
# from django.db.models import Q
from .models import UserInfo
from .forms import SignupForm, SubscribeForm

# Create your views here.
def LogIn(request):
    return render(request, 'common/login.html')

def LogOut(request):
    return render(request, 'common/login.html')

def check_pw_len(pw, MIN_PW_LENGTH = 8):
    if len(pw) < MIN_PW_LENGTH:
        return JsonResponse({'message':'SHORT_PASSWORD'}, status=409)

# 가입 페이지
def SignUp(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            pw = form.cleaned_data['pw']
            # 형식 확인
            check_pw_len(pw)

            # 이미 가입된 이메일인지 확인
            if UserInfo.objects.filter(email=email).exists():
                error_message = '이미 가입된 email 입니다'
                return render(request, 'common/signup.html', {'form':form, 'error_message':error_message})
            else:
                form.save()
                return redirect('main:main')
    else:
        form = SignupForm()
    return render(request, 'common/signup.html', {'form':form})

def Subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if UserInfo.objects.filter(email=email).exists():
                form.save()
                return redirect('main:main')
            else:
                error_message = '등록된 본인 이메일이 아닙니다.'
                return render(request, 'common/subscribe.html',
                              {'form':form, 'error_message':error_message})
    else:
        form = SubscribeForm()
    return render(request, 'common/subscribe.html', {'form':form})

def BookService_detail(request):
    pass
    # 조건문 줘서 bookservice=1인 경우
    # large_category, middle_category, selected_book_isbn 입력 창 나오게...