from django.shortcuts import render, redirect
from forms import SignUpForm
from models import User
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta

# Create your views here.


def signup_view(request):
    if request.method == "POST":
        print 'Sign up form submitted'
    elif request.method == 'GET':
        form = SignUpForm()
    five_hours_thirty_mins_from_now = datetime.now() + timedelta(hours=5.5)
    today = five_hours_thirty_mins_from_now
    return render(request, 'index.html',{'today': today}, {'form' : form})
