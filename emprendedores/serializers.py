from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Service, ServiceRequest, Review
from authentication.serializers import UserSerializer

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

class ServiceSerializer(serializers.ModelSerializer):
    entrepreneur = UserSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Service
        fields = (
            'id', 'entrepreneur', 'category', 'category_name', 
            'title', 'description', 'price_estimate', 
            'horarios_disponibilidad', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'entrepreneur', 'created_at', 'updated_at')

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.user:
            if request.user.role != 'entrepreneur':
                raise serializers.ValidationError("Solo los usuarios con el rol de Emprendedor (entrepreneur) pueden publicar servicios.")
        return attrs

class ServiceRequestSerializer(serializers.ModelSerializer):
    resident = UserSerializer(read_only=True)
    service_title = serializers.CharField(source='service.title', read_only=True)
    entrepreneur_name = serializers.CharField(source='service.entrepreneur.username', read_only=True)

    class Meta:
        model = ServiceRequest
        fields = (
            'id', 'resident', 'service', 'service_title', 'entrepreneur_name',
            'scheduled_datetime', 'status', 'description', 
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'resident', 'created_at', 'updated_at')

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.user:
            if request.user.role != 'resident':
                raise serializers.ValidationError("Solo los residentes pueden realizar solicitudes de servicios.")
        return attrs

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'request', 'rating', 'comment', 'created_at')
        read_only_fields = ('id', 'created_at')

    def validate(self, attrs):
        request = self.context.get('request')
        service_request = attrs.get('request')

        if request and request.user:
            if service_request.resident != request.user:
                raise serializers.ValidationError("Solo el residente que solicitó el servicio puede calificarlo.")

            if service_request.status != 'completed':
                raise serializers.ValidationError("Solo se pueden calificar solicitudes de servicios que hayan sido marcadas como Completadas (completed).")

            if Review.objects.filter(request=service_request).exists():
                raise serializers.ValidationError("Ya existe una calificación para esta solicitud de servicio.")

        return attrs
