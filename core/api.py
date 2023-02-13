from rest_framework import viewsets
from rest_framework import routers
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions

from core.models import (Employee, Enterprise, Site, Tag, PatrolLog, Planning, Zone)
from core.serializers import (EmployeeSerializer, EnterpriseSerializer, SiteSerializer,
                              TagSerializer, PatrolLogSerializer, PlanningSerializer, ZoneSerializer)


class EnterpriseViewSet(viewsets.ReadOnlyModelViewSet):  # viewsets.ModelViewSet  --> Fill CRUD
    """
    A simple ViewSet for viewing object list and detail.
    .../core/api/enterprises       --> for list
    .../core/api/enterprises/2     --> For detail of enterprise 2

    """
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer

    permission_classes = [IsAuthenticated, DjangoObjectPermissions]


class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

    permission_classes = [IsAuthenticated, DjangoObjectPermissions]


class ZoneViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    permission_classes = [IsAuthenticated, DjangoObjectPermissions]


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    permission_classes = [IsAuthenticated, DjangoObjectPermissions]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    permission_classes = [IsAuthenticated, DjangoObjectPermissions]


class PatrolLogViewSet(viewsets.ModelViewSet):
    queryset = PatrolLog.objects.all()
    serializer_class = PatrolLogSerializer

    permission_classes = [IsAuthenticated, DjangoObjectPermissions]


class PlanningViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Planning.objects.all()
    serializer_class = PlanningSerializer

    permission_classes = [IsAuthenticated, DjangoObjectPermissions]


# Registration
router = routers.DefaultRouter()
router.register('employees', EmployeeViewSet)
router.register('enterprises', EnterpriseViewSet)
router.register('sites', SiteViewSet)
router.register('tags', TagViewSet)
router.register('patrol-logs', PatrolLogViewSet)
router.register('plannings', PlanningViewSet)
router.register('zones', ZoneViewSet)
