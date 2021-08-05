from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import VideoForm
from .models import Video


class Home(TemplateView):
    template_name = 'home.html'


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)


def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video_list.html', {
        'videos': videos
    })


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('core:video_list')
    else:
        form = VideoForm()
    return render(request, 'core/upload_video.html', {
        'form': form
    })


def delete_video(request, pk):
    if request.method == 'POST':
        video = Video.objects.get(pk=pk)
        video.delete()
    return redirect('video_list')


class VideoListView(ListView):
    model = Video
    template_name = 'class_video_list.html'
    context_object_name = 'videos'


class UploadVideoView(CreateView):
    model = Video
    form_class = VideoForm
    success_url = reverse_lazy('class_video_list')
    template_name = 'upload_video.html'
