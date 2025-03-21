# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2022 Edith Coates
# Copyright (C) 2022 Brennen Chiu

"""Web_Plom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # contains all the url path from Authentication App
    path("", include("Authentication.urls")),
    path("", include("UserManagement.urls")),
    path("", include("Profile.urls")),
    path("", include("API.urls")),
    path("create/", include("Preparation.urls")),
    path("create/spec/", include("SpecCreator.urls")),
    path("create/paperpdfs/", include("BuildPaperPDF.urls")),
    path("connect/", include("Connect.urls")),
    path("papers/", include("Papers.urls")),
    path("scan/", include("Scan.urls")),
    path("progress/", include("Progress.urls")),
]
