from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def main(request):
    return render(request, 'main/main.html')
        # HttpResponse('main page')

def detail_news(request):
    return render(request, 'main/detail_news.html')

def detail_books(request):
    return render(request, 'main/detail_books.html')