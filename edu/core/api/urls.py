from django.conf import urls
from django.urls import path
from core.api import views

urlpatterns = [
    path("user-create/", views.UserCreateAPIView.as_view()),
    path("login/", views.LoginAPIView.as_view()),
    path("useraccount-retrieve-update/<id>/", views.UserAccountRetrieveUpdateAPIView.as_view()),
    path("password-reset/", views.PasswordResetAPIView.as_view()),
    path("resource-list/", views.ResourceListAPIView.as_view()),
    path("resource-retrieve/<id>/", views.ResourceRetrieveAPIView.as_view()),
    path("helpform-create/", views.HelpFormCreateAPIView.as_view()),
    path("site-settings/", views.SiteSettingsListAPIView.as_view())
]