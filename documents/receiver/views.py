from django.shortcuts import render
from django.views.generic import View
from shared.mixins import ReceiverMixin
from user.models import (Document, DEPARTMENT, DEAN, PRORECTOR, STUDY_HEAD,
                         WAITING, ACCEPTED, CANCELLED, NO_PROCESS)


class DashboardView(ReceiverMixin, View):
    def get(self, request):
        user = request.user
        waiting_documents = None
        all_docs = 0

        if user.role == DEPARTMENT:
            waiting_documents = Document.objects.filter(department_head_sign=WAITING)
            all_docs = Document.objects.exclude(department_head_sign=NO_PROCESS).count()
        elif user.role == DEAN:
            waiting_documents = Document.objects.filter(dean_sign=WAITING)
            all_docs = Document.objects.exclude(dean_sign=NO_PROCESS).count()
        elif user.role == STUDY_HEAD:
            waiting_documents = Document.objects.filter(study_head_sign=WAITING)
            all_docs = Document.objects.exclude(study_head_sign=NO_PROCESS).count()
        elif user.role == PRORECTOR:
            waiting_documents = Document.objects.filter(study_prorector_sign=WAITING)
            all_docs = Document.objects.exclude(study_prorector_sign=NO_PROCESS).count()

        data = {
            "waiting_documents": waiting_documents,
            "all_docs": all_docs,
        }

        return render(request, "receiver/index.html", context=data)
