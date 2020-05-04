"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from ble import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('input/', views.get_input),
    path('new_device/', views.device_register, name='newDevice'),
    path('list_device/', views.device_list, name='listDevice'),

    path('json/rssi/', views.get_rssi, name='getRssi'),
    path('json/avg_rssi/', views.get_avg_rssi, name='avgRssi'),
    path('show_rssi/<int:device_id>/', views.show_rssi, name='rssiDisplay'),
    path('edit_device/<int:device_id>/', views.device_edit, name='editDevice'),
]
