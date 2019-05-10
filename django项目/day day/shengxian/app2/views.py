from django.shortcuts import render
from django.http import HttpResponse

def index2(request):
    return HttpResponse('hello world!')

