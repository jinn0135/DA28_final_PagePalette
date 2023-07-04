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
    if request.method == 'GET':
        return render(request, 'common/login.html')

    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        errMsg = {}

        if not (username and password):
            errMsg['error'] = "모든 값을 입력하세요"
        else:
            user = UserInfo.objects.get(email = username)
            if check_password(password, user.password):
                request.session['email'] = user.email
                return redirect('/')
            else:
                errMsg['error'] = "비밀번호를 다시 입력하세요"
        return render(request, 'common/login.html', errMsg)

def LogOut(request):
    return render(request, 'main/main.html')

# def check_pw_len(pw, MIN_PW_LENGTH = 8):
#     if len(pw) < MIN_PW_LENGTH:
#         return JsonResponse({'message':'비밀번호는 8글자 이상이어야 합니다.'}, status=409)

# 가입 페이지
def SignUp(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if UserInfo.objects.filter(email=email).exists():
                error_message = '이미 가입된 이메일입니다.'
                return render(request, 'common/signup.html', {'form': form, 'error_message': error_message})
            else:
                form.save()
                return redirect('/common/login')
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