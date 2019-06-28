from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.core.files import File

from .file_storage import FileStorage

# Create your views here.


def index(request):
    """Выдаёт список файлов"""
    files = FileStorage().list()

    if request.is_ajax():
        return JsonResponse(files, safe=False)
    else:
        return render(request, 'files/index.html', {'files': files})


def del_file(request):
    """Удаляет файл из директории"""
    if not request.method == 'POST':
        return HttpResponseBadRequest()

    name = request.POST.get('filename')
    if not name:
        raise Http404()

    result = FileStorage().delete(name)

    if request.is_ajax():
        return JsonResponse({'result': 'Ok'})
    else:
        return HttpResponseRedirect(reverse_lazy('files:del_after'))


def del_file_after(request):
    return render(request, 'files/del-after.html')


def add_file(request):
    """Добавляет новый файл в директорию"""
    if not request.method == 'POST':
        return HttpResponseBadRequest()

    if request.FILES:
        file_data = request.FILES['file']
        name = file_data.name
        content = File(file_data)
    else:
        return HttpResponseBadRequest()

    result = FileStorage().save(name, content)

    if request.is_ajax():
        return JsonResponse({'result': 'Ok'})
    else:
        return HttpResponseRedirect(reverse_lazy('files:add_after'))


def add_file_after(request):
    return render(request, 'files/add-after.html')


def show_file(request):
    """Показывает страницу, где пользователь может выбрать загруженный файл из списка и увидеть его в браузере."""
    files = FileStorage().list()
    context = {'files': files}

    selected = request.GET.get('selected', None)
    if selected:
        # На страницу перешли с уже выбранным файлом
        context['selected'] = selected

    if request.is_ajax():
        return JsonResponse(files, safe=False)
    else:
        return render(request, 'files/show-file.html', context)

