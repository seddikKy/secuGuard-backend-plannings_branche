from rest_framework import viewsets
from rest_framework import routers
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


from core.models import (Employee, Enterprise, Site, Tag, PatrolLog, Planning, Zone)
from core.serializers import (EmployeeSerializer, EnterpriseSerializer, SiteSerializer,
                              TagSerializer, PatrolLogSerializer, PlanningSerializer, ZoneSerializer)


class EnterpriseViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer
    
    permission_classes = [IsAuthenticated, DjangoObjectPermissions]
    basename = 'enterprise'
    
    @swagger_auto_schema(
        operation_summary="Get a list of enterprises",  
        operation_description="Returns a list of all enterprises in the system", 
        responses={200: EnterpriseSerializer, 404: "Not found"})
    def list(self, request):    
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Get a single enterprise",  
        operation_description="Returns a single enterprise by ID", 
        responses={200: EnterpriseSerializer(), 404: "Not found"})
    def retrieve(self, request, pk=None):
        try:
            enterprise = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(enterprise)
        return Response(serializer.data)

class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

    permission_classes = [IsAuthenticated, DjangoObjectPermissions]
    basename = 'site'
    
    @swagger_auto_schema(
        operation_summary="Get a list of sites",  
        operation_description="Returns a list of all sites in the system", 
        responses={
            200: SiteSerializer, 
            404: "Not found"
            })
    def list(self, request):    
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Get a single site",  
        operation_description="Returns a single site by ID", 
        responses={200: SiteSerializer(), 404: "Not found"})
    def retrieve(self, request, pk=None):
        try:
            site = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(site)
        return Response(serializer.data)


class ZoneViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    permission_classes = [IsAuthenticated, DjangoObjectPermissions]
    basename = 'zone'
    
    @swagger_auto_schema(
        operation_summary="Get a list of zones",  
        operation_description="Returns a list of all zones in the system", 
        responses={
            200: ZoneSerializer, 
            404: "Not found"
            })
    def list(self, request):    
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Get a single zone",  
        operation_description="Returns a single zone by ID", 
        responses={200: ZoneSerializer(), 404: "Not found"})
    def retrieve(self, request, pk=None):
        try:
            enterprise = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(enterprise)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    permission_classes = [IsAuthenticated, DjangoObjectPermissions]
    basename = 'employee'
    
    @swagger_auto_schema(
        operation_summary="Get a list of employees",  
        operation_description="Returns a list of all employee in the system", 
        responses={
            200: EmployeeSerializer, 
            404: "Not found"
            })
    def list(self, request):    
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Get a single employee",  
        operation_description="Returns a single employee by ID", 
        responses={200: EmployeeSerializer(), 404: "Not found"})
    def retrieve(self, request, pk=None):
        try:
            employee = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(employee)
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    permission_classes = [IsAuthenticated, DjangoObjectPermissions]
    basename = 'tag'
    
    @swagger_auto_schema(
        operation_summary="Get a list of tags",  
        operation_description="Returns a list of all tags in the system", 
        responses={
            200: TagSerializer, 
            404: "Not found"
            })
    def list(self, request):    
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Get a single tag",  
        operation_description="Returns a single tag by ID", 
        responses={200: TagSerializer(), 404: "Not found"})
    def retrieve(self, request, pk=None):
        try:
            tag = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(tag)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Create a new tag",
        operation_description="Creates a new tag in the system",
        request_body=TagSerializer,
        responses={201: TagSerializer, 400: "Bad request"})
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        operation_summary="Update an tag",
        operation_description="Updates an existing tag in the system",
        request_body=TagSerializer,
        responses={200: TagSerializer, 400: "Bad request", 404: "Not found"})
    def update(self, request, pk=None):
        tag = self.get_object()
        serializer = self.get_serializer(tag, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Partial update an tag",
        operation_description="Partially updates an existing tag in the system",
        request_body=TagSerializer,
        responses={200: TagSerializer, 400: "Bad request", 404: "Not found"})
    def partial_update(self, request, pk=None):
        tag = self.get_object()
        serializer = self.get_serializer(tag, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Delete an tag",
        operation_description="Deletes an existing tag from the system",
        responses={204: "No content", 404: "Not found"})
    def destroy(self, request, pk=None):
        tag = self.get_object()
        self.perform_destroy(tag)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PatrolLogViewSet(viewsets.ModelViewSet):
    queryset = PatrolLog.objects.all()
    serializer_class = PatrolLogSerializer

    permission_classes = [IsAuthenticated, DjangoObjectPermissions]
    basename = 'patrolLog'
    
    @swagger_auto_schema(
        operation_summary="Get a list of patrolLogs",  
        operation_description="Returns a list of all patrolLogs in the system", 
        responses={
            200: PatrolLogSerializer, 
            404: "Not found"
            })
    def list(self, request):    
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Get a single patrolLog",  
        operation_description="Returns a single patrolLog by ID", 
        responses={200: PatrolLogSerializer(), 404: "Not found"})
    def retrieve(self, request, pk=None):
        try:
            patrolLog = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(patrolLog)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a new patrolLog",
        operation_description="Creates a new patrolLog in the system",
        request_body=PatrolLogSerializer,
        responses={201: PatrolLogSerializer, 400: "Bad request"})
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        operation_summary="Update an patrolLog",
        operation_description="Updates an existing patrolLog in the system",
        request_body=PatrolLogSerializer,
        responses={200: PatrolLogSerializer, 400: "Bad request", 404: "Not found"})
    def update(self, request, pk=None):
        patrolLog = self.get_object()
        serializer = self.get_serializer(patrolLog, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Partial update an patroLog",
        operation_description="Partially updates an existing patrolLog in the system",
        request_body=PatrolLogSerializer,
        responses={200: PatrolLogSerializer, 400: "Bad request", 404: "Not found"})
    def partial_update(self, request, pk=None):
        patrolLog = self.get_object()
        serializer = self.get_serializer(patrolLog, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Delete an patrolLog",
        operation_description="Deletes an existing patrolLog from the system",
        responses={204: "No content", 404: "Not found"})
    def destroy(self, request, pk=None):
        patrolLog = self.get_object()
        self.perform_destroy(patrolLog)
        return Response(status=status.HTTP_204_NO_CONTENT)




class PlanningViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Planning.objects.all()
    serializer_class = PlanningSerializer

    permission_classes = [IsAuthenticated, DjangoObjectPermissions]
    basename = 'planning'
    
    @swagger_auto_schema(
        operation_summary="Get a list of plannings",  
        operation_description="Returns a list of all plannings in the system", 
        responses={
            200: PlanningSerializer, 
            404: "Not found"
            })
    def list(self, request):    
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Get a single planning",  
        operation_description="Returns a single planning by ID", 
        responses={200: PlanningSerializer(), 404: "Not found"})
    def retrieve(self, request, pk=None):
        try:
            planning = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(planning)
        return Response(serializer.data)


# Registration
router = routers.DefaultRouter()
router.register('employees', EmployeeViewSet)
router.register('enterprises', EnterpriseViewSet)
router.register('sites', SiteViewSet)
router.register('tags', TagViewSet)
router.register('patrol-logs', PatrolLogViewSet)
router.register('plannings', PlanningViewSet)
router.register('zones', ZoneViewSet)
