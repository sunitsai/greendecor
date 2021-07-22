"""greenDecor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from rest_framework.authtoken import views
from django.conf.urls.static import static
from django.contrib import admin
from web.admin_views import *
import settings
from django.views.generic import TemplateView

handler404 = 'web.views.error_404_page'
# handler500 = 'web.views.error_500_page'


urlpatterns = [
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/getplants/$', getPlants),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/product/reports', product_report),
    url(r'', include('web.urls')),
    url('', include('social_django.urls', namespace='social')),
    url(r'^api/', include("api.urls")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include('loginas.urls')),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',content_type='text/plain')),
    url(r'^sitemap\.xml$', TemplateView.as_view(template_name='sitemap.xml',content_type='text/xml')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()