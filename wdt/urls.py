from ariadne.contrib.django.views import GraphQLView
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from wdt.schema.schema import schema

urlpatterns = [
    url(r"^favicon\.ico$", RedirectView.as_view(url="/static/images/favicon.ico")),
    path("admin/", admin.site.urls),
    path("graphql/", GraphQLView.as_view(schema=schema), name="graphql"),
]
