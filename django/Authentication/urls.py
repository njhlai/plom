from django.urls import path

import Authentication.views

urlpatterns = [
    path("login/", Authentication.views.LoginView.as_view(), name="login"),
    path("logout/", Authentication.views.LogoutView.as_view(), name="logout"),
    path("", Authentication.views.Home.as_view(), name="home"),
    path(
        "maintenance/", Authentication.views.Maintenance.as_view(), name="maintenance"
    ),
    # signup path
    path(
        "signup/manager/",
        Authentication.views.SignupManager.as_view(),
        name="signup_manager",
    ),
    path(
        "reset/<slug:uidb64>/<slug:token>/",
        Authentication.views.SetPassword.as_view(),
        name="password_reset",
    ),
    path(
        "reset/done/",
        Authentication.views.SetPasswordComplete.as_view(),
        name="password_reset_complete",
    ),
    path(
        "signup/",
        Authentication.views.Signup.as_view(),
        name="signup",
    ),
    path(
        "signup/scanners/",
        Authentication.views.SignupScanners.as_view(),
        name="signup_scanners",
    ),
    path(
        "signup/markers/",
        Authentication.views.SignupMarkers.as_view(),
        name="signup_markers",
    ),
    path(
        "passwordresetlinks/",
        Authentication.views.PasswordResetLinks.as_view(),
        name="password_reset",
    ),
]
