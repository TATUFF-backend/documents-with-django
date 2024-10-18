from django.shortcuts import render
from django.views.generic import View
from shared.mixins import ReceiverMixin


class DashboardView(ReceiverMixin, View):
    def get(self, request):
        return render(request, "receiver/index.html")
