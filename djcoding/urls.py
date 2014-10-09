from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^sources/', include('sources.urls')),
    url(r'^arithmetic/', include('sources.arithmetic.urls')),
    url(r'^contact/', TemplateView.as_view(template_name="contact.html"),
        name="contact"),
    url(r'^about/', TemplateView.as_view(template_name="about.html"),
        name="about"),

    # url(r'^admin/', include(admin.site.urls)),
)
