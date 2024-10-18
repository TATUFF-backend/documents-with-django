from django.http import HttpResponseRedirect
from django.urls import reverse
from user.models import DEAN, STUDY_HEAD, PRORECTOR, DEPARTMENT, TEACHER, ADMIN


class RoleRequiredMixin:
    roles = None
    role = None
    redirect_url = 'main:home'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('user:login'))

        if self.role and request.user.role != self.role:
            return HttpResponseRedirect(reverse(self.redirect_url))

        if self.roles and request.user.role not in self.roles:
            return HttpResponseRedirect(reverse(self.redirect_url))

        return super().dispatch(request, *args, **kwargs)


class TeacherMixin(RoleRequiredMixin):
    roles = [TEACHER, ADMIN]
    redirect_url = 'receiver:dashboard'


class ReceiverMixin(RoleRequiredMixin):
    roles = [PRORECTOR, DEAN, DEPARTMENT, STUDY_HEAD]
