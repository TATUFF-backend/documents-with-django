import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from shared.mixins import TeacherMixin
from user.models import Document, WAITING, CANCELLED, ACCEPTED
from user.forms import DocumentForm


class HomeView(TeacherMixin, View):
    def get(self, request):
        documents = Document.objects.filter(user=request.user)
        waiting_documents = documents.filter(overall=WAITING)
        statistic = {
            'total': documents.count(),
            'waiting': documents.filter(overall=WAITING).count(),
            'cancelled': documents.filter(overall=CANCELLED).count(),
            'accepted': documents.filter(overall=ACCEPTED).count()
        }
        context = {
            'title': 'Bosh sahifa',
            'notification': "Sizda hammasi yaxshi",
            'waiting_documents': waiting_documents,
            'statistic': statistic,
        }
        return render(request, 'main/index.html', context)


class DocumentListView(LoginRequiredMixin, View):
    def get(self, request):
        documents = Document.objects.filter(user=request.user)
        context = {
            'title': 'Barcha fayllar',
            'documents': documents,
        }
        return render(request, 'main/document_list.html', context)


class DocumentDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
        except:
            return redirect('main:document_list')
        context = {
            'title': f'{document.subject}',
            'document': document,
        }
        return render(request, 'main/document_detail.html', context)


class DocumentCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = DocumentForm()
        context = {
            'title': 'Fayl qo\'shish',
            'form': form,
        }
        return render(request, 'main/document_create.html', context)

    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            return redirect('main:document_list')
        context = {
            'title': 'Fayl qo\'shish',
            'form': form,
        }
        return render(request, 'main/document_create.html', context)


@login_required
def download_file(request, file_id):
    file_instance = get_object_or_404(Document, id=file_id)
    if file_instance.sillabus_file:
        file_path = file_instance.sillabus_file.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                # Fayl turiga qarab Content-Type ni avtomatik aniqlash mumkin
                content_type = "application/pdf"  # PDF hujjatlar uchun
                response = HttpResponse(fh.read(), content_type=content_type)
                response['Content-Disposition'] = f'attachment; filename="{file_instance.file_name()}"'
                return response
    raise Http404("Fayl mavjud emas yoki topilmadi.")


@login_required
def view_file(request, file_id):
    file_instance = get_object_or_404(Document, id=file_id)
    if file_instance.sillabus_file:
        file_path = file_instance.sillabus_file.path
        try:
            return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404("Fayl mavjud emas yoki topilmadi.")
    raise Http404("Fayl mavjud emas yoki topilmadi.")

