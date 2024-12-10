# recruitment/urls.py
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    # Autres URL ici
    # Autres URLS
    # path('login/', LoginView.as_view(), name='login'),  # Connexion de l'utilisateur
    # path('logout/', LogoutView.as_view(), name='logout'),  # Déconnexion de l'utilisateur
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    # Autres URLS
    path('cv/upload/', views.upload_cv, name='upload_cv'),
    path('search/', views.search_cvs, name='search_cvs'),
    # Ajoutez cette ligne dans le fichier urls.py
    path('accounts/profile/', views.profile, name='profile'),
    path('profile/', views.profile, name='profile'),
    path('cv/list/', views.cv_list, name='cv_list'),
    path('cv/edit/<int:cv_id>/', views.edit_cv, name='edit_cv'),
    path('cv/delete/<int:cv_id>/', views.delete_cv, name='delete_cv'),
    path('cv/download_all/', views.download_all_cvs, name='download_all_cvs'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Autres URL de l'API

    # path('cv/list/', views.cv_list, name='cv_list'),

]
