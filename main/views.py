import os

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from shared.mixins import TeacherMixin
from user.models import Document, WAITING, CANCELLED, ACCEPTED, NO_PROCESS
from user.forms import DocumentForm


class HomeView(TeacherMixin, View):
    def get(self, request):
        documents = Document.objects.filter(user=request.user)
        waiting_documents = documents.filter(Q(overall=WAITING) | Q(overall=CANCELLED))

        statistic = {
            'total': documents.count(),
            'waiting': documents.filter(overall=WAITING).count(),
            'cancelled': documents.filter(overall=CANCELLED).count(),
            'accepted': documents.filter(overall=ACCEPTED).count()
        }
        context = {
            'title': 'Bosh sahifa',
            'notification': "Sizda hammasi yaxshi",
            'documents': waiting_documents,
            'statistic': statistic,
        }
        return render(request, 'main/index.html', context)


class DocumentListView(TeacherMixin, View):
    def get(self, request):
        documents = Document.objects.filter(user=request.user)
        context = {
            'title': 'Barcha fayllar',
            'documents': documents,
        }
        return render(request, 'main/document_list.html', context)


class DocumentDetailView(TeacherMixin, View):
    def get(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
        except:
            messages.error(request, "Fayl topilmadi")
            return redirect('main:document_list')
        context = {
            'title': f'{document.subject}',
            'document': document,
        }
        return render(request, 'main/document_detail.html', context)


class DocumentCreateView(TeacherMixin, View):
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
            messages.success(request, "Ma'lumot muvaffaqiyatli qo'shildi!")
            return redirect('main:document_list')
        context = {
            'title': 'Fayl qo\'shish',
            'form': form,
        }
        return render(request, 'main/document_create.html', context)


class DocumentUpdateView(TeacherMixin, View):
    def get(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
            if document.overall == 'accepted' or not document.user == request.user:
                messages.warning(request, "O'zgartirish uchun ruxsat yo'q!")
                return redirect('main:document_list')

            form = DocumentForm(instance=document)
            context = {
                'title': 'Tahrirlash',
                'form': form,
                'pk': pk
            }
            return render(request, 'main/document_update.html', context)
        except Document.DoesNotExist:
            return redirect('main:document_list')

    def post(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
            if document.overall == 'accepted' or not document.user == request.user:
                messages.warning(request, "O'zgartirish uchun ruxsat yo'q!")
                return redirect('main:document_list')

            form = DocumentForm(request.POST, request.FILES, instance=document)

            if form.is_valid():
                if 'sillabus_file' in request.FILES:
                    document.sillabus_file = request.FILES['sillabus_file']
                if document.overall == CANCELLED:
                    document.overall = WAITING
                    document.department_head_sign = WAITING if document.department_head_sign == CANCELLED else document.department_head_sign
                    document.dean_sign = WAITING if document.dean_sign == CANCELLED else document.dean_sign
                    document.study_head_sign = WAITING if document.study_head_sign == CANCELLED else document.study_head_sign
                    document.study_prorector_sign = WAITING if document.study_prorector_sign == CANCELLED else document.study_prorector_sign
                    document.save()
                if document.overall == NO_PROCESS and document.status == True:
                    document.overall = WAITING
                    document.department_head_sign = WAITING
                    document.dean_sign = NO_PROCESS
                    document.study_head_sign = NO_PROCESS
                    document.study_prorector_sign = NO_PROCESS
                    document.save()
                if document.overall == WAITING and document.status == False:
                    document.overall = NO_PROCESS
                    document.department_head_sign = NO_PROCESS
                    document.dean_sign = NO_PROCESS
                    document.study_head_sign = NO_PROCESS
                    document.study_prorector_sign = NO_PROCESS
                    document.save()
                messages.success(request, "O'zgartirishlar muvaffaqiyatli saqlandi!")
                form.save()

                return redirect('main:document_list')

            context = {
                'title': 'Tahrirlash',
                'form': form,
                'pk': pk
            }
            return render(request, 'main/document_update.html', context)
        except Document.DoesNotExist:
            messages.error(request, "Ma'lumot topilmadi")
            return redirect('main:document_list')


class DocumentDeleteView(TeacherMixin, View):
    def get(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
            if document.overall == 'accepted' or not document.user == request.user:
                messages.warning(request, "O'chirishga ruxsat yo'q")
                return redirect('main:document_list')
            messages.warning(request, "Malumot o'chirildi!")
            document.delete()
        except Document.DoesNotExist:
            messages.error(request, "Malumot topilmadi!")
        return redirect('main:document_list')


@login_required
def download_file(request, file_id):
    file_instance = get_object_or_404(Document, id=file_id)
    if file_instance.sillabus_file:
        file_path = file_instance.sillabus_file.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                content_type = "application/pdf"
                response = HttpResponse(fh.read(), content_type=content_type)
                response['Content-Disposition'] = f'attachment; filename="{file_instance.file_name()}"'
                return response
    messages.error(request, "Nimadur xato ketdi!")
    return redirect('main:home')


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

