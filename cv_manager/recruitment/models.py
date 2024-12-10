# recruitment/models.py
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils.timezone import now

# class CV(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)  # Exemple de champ title
#     file = models.FileField(upload_to='cv_files/')  # Exemple de champ file
#     # Autres champs si nécessaires

# class CV(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cvs')
#     title = models.CharField(max_length=100)
#     file = models.FileField(upload_to='cv_files/')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.title


class CV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who uploaded the CV
    title = models.CharField(max_length=255)  # Title of the CV
    # cv_file = models.FileField(upload_to='cvs/')  # File field for uploading CVs
    # cv_file = models.FileField(upload_to='cvs/', default='default_file.pdf')

    # cv_file = models.FileField(upload_to='cvs/', null=True, blank=True)
    cv_file = models.FileField(upload_to='cv_files/', null=True, blank=True)

    created_at = models.DateTimeField(default=now)
def __str__(self):
    return f'{self.user.username} - CV'

# class CV(models.Model):
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     cv_file = models.FileField(upload_to='cv_files/')
#
#     # created_at = models.DateTimeField(auto_now_add=True)
#     created_at = models.DateTimeField(null=True, blank=True)
# def __str__(self):
#         return f'{self.user.username} CV'