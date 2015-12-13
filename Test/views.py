# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import django

def home(request):
	return HttpResponse('<p>Django Version = ' + str(django.get_version()))
