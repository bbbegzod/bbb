from django.urls import path
from app1.services.Ishchi import IshchiView
from app1.services.auth import RegisView, LoginView, LogOutView, UserActions, AuthOne, AuthTwo

urlpatterns = [
    path('ishchi/', IshchiView.as_view()),
    path('ishchi/<int:pk>/', IshchiView.as_view()),
    path('regis/', RegisView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('user/actions/', UserActions.as_view()),
    path('auth/one/', AuthOne.as_view()),
    path('auth/two/', AuthTwo.as_view()),
]