"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from debug_toolbar.toolbar import debug_toolbar_urls

from mysite import settings

# 这个urlpatterns是负责整体项目的url搭配
urlpatterns = [
    path("admin/", admin.site.urls),
    path('polls/', include("polls.urls")),  # 如果调用到路径polls，那么就去polls.urls下面找
] + debug_toolbar_urls()

# 运行测试时禁用工具栏
if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()
