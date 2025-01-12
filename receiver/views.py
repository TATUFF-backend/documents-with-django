from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from shared.mixins import ReceiverMixin
from user.models import (Document, DEPARTMENT, DEAN, PRORECTOR, STUDY_HEAD,
                         WAITING, ACCEPTED, CANCELLED, NO_PROCESS, Comment)
from django.contrib import messages


class DashboardView(ReceiverMixin, View):
    def get(self, request):
        user = request.user
        waiting_documents = None
        all = 0
        waiting = 0
        accepted = 0
        cancelled = 0

        if user.role == DEPARTMENT:
            waiting_documents = Document.objects.filter(department_head_sign=WAITING)
            all = Document.objects.exclude(department_head_sign=NO_PROCESS).count()
            waiting = waiting_documents.count()
            accepted = Document.objects.filter(department_head_sign=ACCEPTED).count()
            cancelled = Document.objects.filter(department_head_sign=CANCELLED).count()

        elif user.role == DEAN:
            waiting_documents = Document.objects.filter(dean_sign=WAITING)
            all = Document.objects.exclude(dean_sign=NO_PROCESS).count()
            waiting = waiting_documents.count()
            accepted = Document.objects.filter(dean_sign=ACCEPTED).count()
            cancelled = Document.objects.filter(dean_sign=CANCELLED).count()

        elif user.role == STUDY_HEAD:
            waiting_documents = Document.objects.filter(study_head_sign=WAITING)
            all = Document.objects.exclude(study_head_sign=NO_PROCESS).count()
            waiting = waiting_documents.count()
            accepted = Document.objects.filter(study_head_sign=ACCEPTED).count()
            cancelled = Document.objects.filter(study_head_sign=CANCELLED).count()

        elif user.role == PRORECTOR:
            waiting_documents = Document.objects.filter(study_prorector_sign=WAITING)
            all = Document.objects.exclude(study_prorector_sign=NO_PROCESS).count()
            waiting = waiting_documents.count()
            accepted = Document.objects.filter(overall=ACCEPTED).count()
            cancelled = Document.objects.filter(overall=CANCELLED).count()

        statistics = {
            "all": all,
            "waiting": waiting,
            "accepted": accepted,
            "cancelled": cancelled
        }

        data = {
            "waiting_documents": waiting_documents,
            "statistics": statistics,
        }

        return render(request, "receiver/index.html", context=data)


class AllPageView(ReceiverMixin, View):
    def get(self, request):
        user = request.user
        all_documents = None
        if user.role == DEPARTMENT:
            all_documents = Document.objects.exclude(department_head_sign=NO_PROCESS)
        elif user.role == DEAN:
            all_documents = Document.objects.exclude(dean_sign=NO_PROCESS)
        elif user.role == STUDY_HEAD:
            all_documents = Document.objects.exclude(study_head_sign=NO_PROCESS)
        elif user.role == PRORECTOR:
            all_documents = Document.objects.exclude(overall=NO_PROCESS)

        data = {
            "all_documents": all_documents,
        }

        return render(request, "receiver/all.html", context=data)


class WaitingPageView(ReceiverMixin, View):
    def get(self, request):
        user = request.user
        waiting_documents = None
        if user.role == DEPARTMENT:
            waiting_documents = Document.objects.filter(department_head_sign=WAITING)
        elif user.role == DEAN:
            waiting_documents = Document.objects.filter(dean_sign=WAITING)
        elif user.role == STUDY_HEAD:
            waiting_documents = Document.objects.filter(study_head_sign=WAITING)
        elif user.role == PRORECTOR:
            waiting_documents = Document.objects.filter(study_prorector_sign=WAITING)

        data = {
            "waiting_documents": waiting_documents,
        }

        return render(request, "receiver/waiting.html", context=data)


class AcceptedPageView(ReceiverMixin, View):
    def get(self, request):
        user = request.user
        accepted_documents = None
        if user.role == DEPARTMENT:
            accepted_documents = Document.objects.filter(department_head_sign=ACCEPTED)
        elif user.role == DEAN:
            accepted_documents = Document.objects.filter(dean_sign=ACCEPTED)
        elif user.role == STUDY_HEAD:
            accepted_documents = Document.objects.filter(study_head_sign=ACCEPTED)
        elif user.role == PRORECTOR:
            accepted_documents = Document.objects.filter(study_prorector_sign=ACCEPTED)

        data = {
            "accepted_documents": accepted_documents,
        }

        return render(request, "receiver/accepted.html", context=data)


class CancelledPageView(ReceiverMixin, View):
    def get(self, request):
        user = request.user
        cancelled_documents = None
        if user.role == DEPARTMENT:
            cancelled_documents = Document.objects.filter(department_head_sign=CANCELLED)
        elif user.role == DEAN:
            cancelled_documents = Document.objects.filter(dean_sign=CANCELLED)
        elif user.role == STUDY_HEAD:
            cancelled_documents = Document.objects.filter(study_head_sign=CANCELLED)
        elif user.role == PRORECTOR:
            cancelled_documents = Document.objects.filter(study_prorector_sign=CANCELLED)

        data = {
            "cancelled_documents": cancelled_documents,
        }

        return render(request, "receiver/cancelled.html", context=data)


class ReceiveDocumentView(ReceiverMixin, View):
    def get(self, request, pk):
        document = Document.objects.get(pk=pk)
        context = {
            'title': f'{document.subject}',
            'document': document,
        }
        return render(request, 'receiver/receive.html', context)

    def post(self, request, pk):
        document = get_object_or_404(Document, id=pk)
        user = request.user
        comment = request.POST.get('comment')
        decision = request.POST.get('decision')
        file_upload = request.FILES.get('fileUpload')

        if comment:
            # document.document_comment = comment
            if user.role == DEPARTMENT:
                if decision == 'accepted':
                    # document.department_head_sign = decision
                    document.dean_sign = 'waiting'
                else:
                    document.overall = CANCELLED
                document.department_head_sign = decision

                document.save()
                comment = Comment.objects.create(document=document, user=user, comment=comment, status=decision)
                if file_upload:
                    comment.file = file_upload
                    comment.save()

                if document.department_head_sign == ACCEPTED:
                    messages.success(request, "Hujjat muvaffaqqiyatli qabul qilindi!")
                else:
                    messages.warning(request, "Hujjat muvaffaqqiyatli rad etildi!")

                return redirect('receiver:all')

            elif user.role == DEAN:
                if decision == 'accepted':
                    # document.dean_sign = decision
                    document.study_head_sign = 'waiting'
                else:
                    document.overall = CANCELLED
                document.dean_sign = decision
                document.save()
                comment = Comment.objects.create(document=document, user=user, comment=comment, status=decision)
                if file_upload:
                    comment.file = file_upload
                    comment.save()

                if document.dean_sign == ACCEPTED:
                    messages.success(request, "Hujjat muvaffaqqiyatli qabul qilindi!")
                else:
                    messages.warning(request, "Hujjat muvaffaqqiyatli rad etildi!")

                return redirect('receiver:all')

            elif user.role == STUDY_HEAD:
                if decision == 'accepted':
                    # document.study_head_sign = decision
                    document.study_prorector_sign = 'waiting'
                else:
                    document.overall = CANCELLED
                document.study_head_sign = decision
                document.save()
                comment = Comment.objects.create(document=document, user=user, comment=comment, status=decision)
                if file_upload:
                    comment.file = file_upload
                    comment.save()

                if document.study_head_sign == ACCEPTED:
                    messages.success(request, "Hujjat muvaffaqqiyatli qabul qilindi!")
                else:
                    messages.warning(request, "Hujjat muvaffaqqiyatli rad etildi!")

                return redirect('receiver:all')

            elif user.role == PRORECTOR:
                if decision == 'accepted':
                    # document.study_prorector_sign = decision
                    document.overall = decision
                else:
                    document.overall = CANCELLED
                document.study_prorector_sign = decision
                document.save()
                comment = Comment.objects.create(document=document, user=user, comment=comment, status=decision)
                if file_upload:
                    comment.file = file_upload
                    comment.save()

                if document.study_prorector_sign == ACCEPTED:
                    messages.success(request, "Hujjat muvaffaqqiyatli qabul qilindi!")
                else:
                    messages.warning(request, "Hujjat muvaffaqqiyatli rad etildi!")

                return redirect('receiver:all')

            else:
                messages.warning(request, "Qandaydir xatolik mavjud!")
                return redirect('receiver:all')






