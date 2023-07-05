from django.shortcuts import render, redirect
# import json, re, traceback
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
# from django.views import View
# from django.core.exceptions import ValidationError
# from django.db.models import Q
from .models import UserInfo
from .forms import SignupForm, SubscribeForm

# Create your views here.

def LogIn(request):
    if request.method == "POST":
        email = request.POST.get('email')
        pw = request.POST.get('pw')
        try:
                # UserInfo 모델에서 해당 이메일과 비밀번호 확인
                user = UserInfo.objects.get(email=email, pw=pw)
                # 로그인 처리
                request.session['email'] = user.email
                return redirect('main:main')
        except UserInfo.DoesNotExist:
                error_message = '이메일 또는 비밀번호가 일치하지 않습니다.'
                return render(request, 'common/login.html', {'error_message': error_message})
    else:
        form = SignupForm()

    return render(request, 'common/login.html', {'form':form})

def LogOut(request):
    # 로그아웃 처리
    if 'email' in request.session:
        del request.session['email']
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
