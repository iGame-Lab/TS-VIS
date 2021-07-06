"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from .api import api
from django.views.generic import TemplateView

api_urlpatterns = [
    path('init', api.init_process),
    path('getCategory', api.get_category),
    path('scalar', api.get_scalar),
    path('histogram', api.get_histogram),
    path('distribution', api.get_distribution),
    path('text', api.get_text),
    path('audio', api.get_audio_meta),
    path('audio_raw', api.get_audio),
    path('image', api.get_image_meta),
    path('image_raw', api.get_image),
    path('graph', api.get_graph),
    path('hyperparm', api.get_hparams),
    path('projector', api.get_projector_meta),
    path('projector_raw', api.get_projector_raw),
    path('projector_data', api.get_projector),
    path('projector_sample', api.get_projector_sample),
    path('exception', api.get_exception_meta),
    path('exception_data', api.get_exception),
    path('exception_hist', api.get_exception_hist),
    path('exception_box', api.get_exception_box)
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
    path(r'', TemplateView.as_view(template_name='index.html'))
]
