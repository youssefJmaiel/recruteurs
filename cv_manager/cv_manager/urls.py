from django.contrib import admin
from django.urls import path, include
from recruitment import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recruitment/', include('recruitment.urls')),  # Ajouter cette ligne pour inclure les URLs de l'app recrutement
    path('login/', include('django.contrib.auth.urls')),  # Connexion
    path('logout/', include('django.contrib.auth.urls')),  # Déconnexion
    path('add_cv/', views.add_cv, name='add_cv'),  # Route pour ajouter un CV
    path('', views.home, name='home'),  # Page d'accueil
    path('cv/upload/', views.upload_cv, name='upload_cv'),
    # Ajoutez cette ligne dans le fichier urls.py
    path('accounts/profile/', views.profile, name='profile'),
    path('cv/list/', views.cv_list, name='cv_list'),
    path('accounts/profile/', views.profile, name='profile'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search_cvs, name='search_cvs'),
    path('cv/edit/<int:cv_id>/', views.edit_cv, name='edit_cv'),
    path('cv/delete/<int:cv_id>/', views.delete_cv, name='delete_cv'),
    path('cv/download_all/', views.download_all_cvs, name='download_all_cvs'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  # Autres URL de l'API

    # path('cv/list/', views.cv_list, name='cv_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
