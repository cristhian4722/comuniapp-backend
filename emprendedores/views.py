from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Service, ServiceRequest, Review
from .serializers import (
    CategorySerializer,
    ServiceSerializer,
    ServiceRequestSerializer,
    ReviewSerializer
)

class IsEntrepreneur(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'entrepreneur'

class IsResident(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'resident'

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.entrepreneur == request.user

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, IsEntrepreneur, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(entrepreneur=self.request.user)

    def get_queryset(self):
        queryset = Service.objects.all()
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class ServiceRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'resident':
            return ServiceRequest.objects.filter(resident=user)
        elif user.role == 'entrepreneur':
            return ServiceRequest.objects.filter(service__entrepreneur=user)
        return ServiceRequest.objects.none()

    def perform_create(self, serializer):
        serializer.save(resident=self.request.user, status='pending')

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        service_request = self.get_object()
        if service_request.service.entrepreneur != request.user:
            return Response(
                {"detail": "No tienes permiso para aceptar esta solicitud."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if service_request.status != 'pending':
            return Response(
                {"detail": "Solo puedes aceptar solicitudes con estado pendiente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        service_request.status = 'accepted'
        service_request.save()
        return Response(ServiceRequestSerializer(service_request).data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        service_request = self.get_object()
        if service_request.service.entrepreneur != request.user:
            return Response(
                {"detail": "No tienes permiso para completar esta solicitud."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if service_request.status != 'accepted':
            return Response(
                {"detail": "Solo puedes completar solicitudes previamente aceptadas."},
                status=status.HTTP_400_BAD_REQUEST
            )

        service_request.status = 'completed'
        service_request.save()
        return Response(ServiceRequestSerializer(service_request).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        service_request = self.get_object()
        is_resident = service_request.resident == request.user
        is_entrepreneur = service_request.service.entrepreneur == request.user

        if not (is_resident or is_entrepreneur):
            return Response(
                {"detail": "No tienes permiso para cancelar o declinar esta solicitud."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if service_request.status in ['completed', 'cancelled']:
            return Response(
                {"detail": "No se puede cancelar una solicitud ya completada o cancelada."},
                status=status.HTTP_400_BAD_REQUEST
            )

        service_request.status = 'cancelled'
        service_request.save()
        return Response(ServiceRequestSerializer(service_request).data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, IsResident]
        return [permission() for permission in permission_classes]

