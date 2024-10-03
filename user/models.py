from django.db import models
from django.contrib.auth.models import AbstractUser

ADMIN, USER = ('Admin', 'User')
WAITING, CANCELLED, ACCEPTED = (0, 1, 2)


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='faculty/logo/', blank=True, null=True)
    status = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'

    def get_logo(self):
        if self.logo:
            return self.logo.url
        return False


class Field(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name="Fakultet")
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='field/logo/')
    status = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Field'
        verbose_name_plural = 'Fields'

    def get_logo(self):
        if self.logo:
            return self.logo.url
        return False


class Subject(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, verbose_name="Field")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name="Faculty")
    name = models.CharField(max_length=255)
    sample_file = models.FileField(upload_to='subject/file/')
    status = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'


class User(AbstractUser):
    ROLES_CHOICES = (
        (ADMIN, ADMIN),
        (USER, USER),
    )

    image = models.ImageField(upload_to='users/profile/', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLES_CHOICES)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    field = models.ForeignKey(Field, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

    def get_image(self):
        if self.image:
            return self.image.url
        return False


class Document(models.Model):
    STATUS_CHOICES = (
        (WAITING, "Waiting"),
        (CANCELLED, 'Cancelled'),
        (ACCEPTED, 'Accepted'),
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Subject")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    sillabus_file = models.FileField(upload_to='document/sillabus/')
    department_head_sign = models.IntegerField(choices=STATUS_CHOICES, default=WAITING)
    dean_sign = models.IntegerField(choices=STATUS_CHOICES, default=WAITING)
    study_head_sign = models.IntegerField(choices=STATUS_CHOICES, default=WAITING)
    study_prorector_sign = models.IntegerField(choices=STATUS_CHOICES, default=WAITING)
    document_comment = models.TextField(blank=True, null=True)
    status = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.subject.name} - {self.user.username}'

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'


class Comment(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name="Document")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    comment = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='document/comment/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.document.subject.name} - {self.user.username}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
