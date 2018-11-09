# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from .forms import *
from .models import *

# Create your views here.

# TODO: history
# TODO: login mixin
# TODO: organizations in login view
# TODO: organization result for admin
# TODO: how to set an admin for organization??
# TODO: payment


def home(request):
    return render(
        request,
        'index.html',
        {
            'title': 'Home page',
        }
    )


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.userprofile.organization = form.cleaned_data.get('organization')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(
        request,
        'signup.html',
        {
            'title': 'Sign Up',
            'form': form,
        }
    )


def contact(request):
    return render(
        request,
        'contact.html',
        {
            'title': 'Contact',
            'message': 'Your contact page.',
        }
    )


def about(request):
    return render(
        request,
        'about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
        }
    )


def test(request):
    questions = [(q, Answer.objects.filter(question=q)) for q in Question.objects.all()]
    return render(
        request,
        'test.html',
        {
            'title': 'Test',
            'questions': questions
        }
    )


def testresults(request, results):  # results = [(q1, a1), (q2, a2), ...]
    if request.method == 'POST':
        test = Test.objects.create(user=request.user)
        for res in results:
            TestResult.objects.create(test=test, question=res[0], answer=res[1])
        return redirect('home')
    return render(
        request,
        'testresults.html',
        {
            'title': 'Test Results'
        }
    )


def history(request):
    tests = Test.objects.filter(user=request.user)
    testresults = [(test, TestResult.objects.filter(test=test)) for test in tests]
    return render(
        request,
        'history.html',
        {
            'title': 'History',
            'testresults': testresults
        }
    )


def orgresults(request):
    tests = Test.objects.filter(user__UserProfile__organization=request.user.userprofile.organization)
    testresults = [(test, TestResult.objects.filter(test=test)) for test in tests]
    return render(
        request,
        'orgresults.html',
        {
            'title': 'Organization Results',
            'testresults': testresults
        }
    )
