from django.urls import re_path, path, include

from .api import router
# from rest_framework.schemas import get_schema_view
# from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from .views import (EmployeeListView, EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView,
                    EmployeeDetailView, EnterpriseListView, EnterpriseCreateView, EnterpriseUpdateView,
                    EnterpriseDeleteView,
                    EnterpriseDetailView, SiteListView, SiteCreateView, SiteUpdateView, SiteDeleteView,
                    SiteDetailView, TagListView, TagCreateView, TagUpdateView, TagDeleteView,
                    TagDetailView, ZoneListView, ZoneCreateView, ZoneUpdateView, ZoneDeleteView,
                    ZoneDetailPlanningListView, ZoneDetailPlanningCreateView, ZoneDetailPlanningUpdateView,
                    ZoneDetailPlanningDeleteView, ZoneDetailPlanningDetailView, ZoneConfirmPlanningView,
                    ZoneReopenPlanningView)

schema_view = get_schema_view(
   openapi.Info(
      title="SecuGard API",
      default_version='v1',
      description="This API is used to manage secuGardAPI",
    #   terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="secugard@outlook.fr"),
      license=openapi.License(name="BSD License"),
   ),
   public=False,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/', include(router.urls)),
    # Enterprise path
    path('enterprises', EnterpriseListView.as_view(), name='enterprise_list'),
    path('enterprises/create', EnterpriseCreateView.as_view(), name='enterprise_create'),
    path('enterprises/<int:pk>', EnterpriseDetailView.as_view(), name='enterprise_detail'),
    path('enterprises/<int:pk>/update', EnterpriseUpdateView.as_view(), name='enterprise_update'),
    path('enterprises/<int:pk>/delete', EnterpriseDeleteView.as_view(), name='enterprise_delete'),

    # Site path
    path('sites', SiteListView.as_view(), name='site_list'),
    path('sites/create', SiteCreateView.as_view(), name='site_create'),
    path('sites/<int:pk>', SiteDetailView.as_view(), name='site_detail'),
    path('sites/<int:pk>/update', SiteUpdateView.as_view(), name='site_update'),
    path('sites/<int:pk>/delete', SiteDeleteView.as_view(), name='site_delete'),

    # Zone path
    path('zones', ZoneListView.as_view(), name='zone_list'),
    path('zones/create', ZoneCreateView.as_view(), name='zone_create'),
    path('zones/<int:pk>/update', ZoneUpdateView.as_view(), name='zone_update'),
    path('zones/<int:pk>/delete', ZoneDeleteView.as_view(), name='zone_delete'),
    path('zones/<int:pk>/confirm', ZoneConfirmPlanningView.as_view(), name='zone_confirm'),
    path('zones/<int:pk>/reopen', ZoneReopenPlanningView.as_view(), name='zone_reopen'),

    # Zone Planning
    path('zones/<int:parent_pk>/<int:day_index>/plannings/', ZoneDetailPlanningListView.as_view(), name='zone_detail'),
    path('zones/<int:parent_pk>/<int:day_index>/plannings/create', ZoneDetailPlanningCreateView.as_view(), name='planning_create'),
    path('zones/<int:parent_pk>/<int:day_index>/plannings/<int:pk>', ZoneDetailPlanningDetailView.as_view(), name='planning_detail'),
    path('zones/<int:parent_pk>/<int:day_index>/plannings/<int:pk>/update', ZoneDetailPlanningUpdateView.as_view(), name='planning_update'),
    path('zones/<int:parent_pk>/<int:day_index>/plannings/<int:pk>/delete', ZoneDetailPlanningDeleteView.as_view(), name='planning_delete'),

    # Employee path
    path('employees', EmployeeListView.as_view(), name='employee_list'),
    path('employees/create', EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/<int:pk>', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/<int:pk>/update', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/<int:pk>/delete', EmployeeDeleteView.as_view(), name='employee_delete'),

    # tag path
    path('tags', TagListView.as_view(), name='tag_list'),
    path('tags/create', TagCreateView.as_view(), name='tag_create'),
    path('tags/<int:pk>', TagDetailView.as_view(), name='tag_detail'),
    path('tags/<int:pk>/update', TagUpdateView.as_view(), name='tag_update'),
    path('tags/<int:pk>/delete', TagDeleteView.as_view(), name='tag_delete'),

    # docs API path
    # path('docs-api/', include_docs_urls(title='secuGardApi')),
    # path('schema', get_schema_view(
    #     title="secuGardApi",
    #     description="API for secuGardApi",
    #     version="1.0.0"
    # ), name='openapi-schema'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
