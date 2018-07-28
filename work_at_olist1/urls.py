"""work_at_olist1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from calls.api.viewsets import PhoneCallViewSet, BillViewSet
from telephone_numbers.api.viewsets import TelephoneNumberViewSet

schema_view = get_schema_view(openapi.Info(
    title="Work at Olist API",
    default_version='v1',
    description="API developed as an avaliation to work at Olist Company",
    contact=openapi.Contact(email="paulozullu@gmail.com"),
    license=openapi.License(name="BSD License"),
),
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'telephone_numbers', TelephoneNumberViewSet,
                base_name='TelephoneNumber')
router.register(r'calls', PhoneCallViewSet, base_name='PhoneCall')
router.register(r'bills', BillViewSet, base_name='Bill')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    url(r'^docs/$', schema_view.with_ui(
        'swagger', cache_timeout=None), name='docs'),
]
