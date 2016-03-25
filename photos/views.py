import logging

from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from taskqueue import make_thumbnail

from rest_framework import serializers, viewsets
from pystagram.middlewares import HelloWorldError

from .models import Photo, Like
from .forms import ImageForm

logger = logging.getLogger('django')

class PhotoSerializer(serializers.ModelSerializer) :  # Photo 모델 시리얼라이저
    class Meta :
        model = Photo
        fields = ('id', 'image', 'content', 'created_at', )

class PhotoViewSet(viewsets.ModelViewSet) :
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


def toppage(request) :
    logger.warning('warning message log')
    photos = Photo.objects.order_by('-updated_at')
    ctx = {
        'object_list' : photos,
    }
    return render(request, 'toppage.html', ctx)

def view_photo(request, pk) :
#    messages.info(request, '글 목록에 접근함')
    photo = get_object_or_404(Photo, pk=pk)
    ctx = {
        'photo' : photo,
    }
    return render(request, 'view_photo.html', ctx)

@login_required
def like_photo(request, pk) :
    photo = get_object_or_404(Photo, pk=pk)

    like, is_created = Like.objects.get_or_create(
        user=request.user,
        photo=photo,
        defaults = {
            'user' : request.user,
            'photo' : photo,
            'status' : True,
        }
    )

    if is_created is False :
        like.status = not like.status
        like.save()
        if like.status is True :
            messages.info(request, '좋아요')
        else :
            messages.info(request, '좋아요 취소')
    else :
        messages.info(request, '좋아요')

    return redirect('photos:view_photo', pk= photo.pk)

"""
@login_required
def create_photo(request) :
    if request.method == 'GET' :
        form = ImageForm()
    else :
        form = ImageForm(request.POST)

        if form.is_valid() :
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()

            make_thumbnail.delay(photo.image.path, 100, 100)
            return redirect('photos:view_photo', pk=post.pk)
        else :
            return None

    render (request, 'photos:photo_upload', {
            'form' : form,
    })
"""

@login_required
def photo_upload(request) :
    if request.method == 'POST' :
        form_instance = ImageForm(request.POST, request.FILES)
        if form_instance.is_valid() :
            photo = form_instance.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('photos:view_photo', pk=photo.pk)

    else : # if request.GET
        form_instance = ImageForm()

    return render(request, 'upload.html', {
            'form' : form_instance,
    })
