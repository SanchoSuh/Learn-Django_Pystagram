# pystagram/middlewares.py
from django.shortcuts import render
from django.http import HttpResponse


class HelloWorldError(Exception):
    pass


class SampleMiddleware(object):
    def process_request(self, request):
        request.just_say = 'Hello world'
        return

    def process_exception(self, request, exc):
#        if isinstance(exc, HelloWorldError):
#            return HttpResponse('어흑, Hello world error...')
        return

