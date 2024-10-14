from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User, Faculty, Comment, Field, Subject, Document


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'is_active', 'role', 'print_image')
    list_display_links = ('pk', 'username', )
    list_filter = ('faculty', 'role')

    def print_image(self, obj):
        return mark_safe(f'<img src="{obj.get_image()}" width="50" height="50" style="border-radius: 50%;"/>')


    class Meta:
        model = User
        fields = "__all__"


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'status', 'print_logo')
    list_display_links = ('pk', 'name', )
    # list_editable = ('status',)

    def print_logo(self, obj):
        return mark_safe(f'<img src="{obj.get_logo()}" width="70" height="70" style="border-radius: 50%;"/>')
    print_logo.short_description = 'Logo'


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'faculty', 'status', 'print_logo')
    list_display_links = ('pk', 'name', )

    def print_logo(self, obj):
        return mark_safe(f'<img src="{obj.get_logo()}" width="70" height="70" style="border-radius: 50%;"/>')
    print_logo.short_description = 'Logo'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'field', 'faculty', 'status')
    list_display_links = ('pk', 'name', )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'user', 'department_head_sign', 'dean_sign', 'study_head_sign', 'study_prorector_sign', 'overall', 'status')
    list_display_links = ('pk', 'subject', )
    list_editable = ('status', 'department_head_sign', 'dean_sign', 'study_head_sign', 'study_prorector_sign', 'overall')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'document', 'comment')
    list_display_links = ('pk', 'user', )
