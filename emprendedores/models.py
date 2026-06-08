from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Service(models.Model):
    entrepreneur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='services'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_estimate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Estimado en pesos/moneda local"
    )
    horarios_disponibilidad = models.CharField(
        max_length=250,
        help_text="Ej: Lunes a Viernes 8:00 AM - 5:00 PM"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.entrepreneur.username}"

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('accepted', 'Aceptada'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    ]

    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='requests'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='requests'
    )
    scheduled_datetime = models.DateTimeField(help_text="Fecha y hora sugerida para el servicio")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción del problema o requerimiento específico"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Solicitud #{self.id} - {self.service.title} ({self.get_status_display()})"

class Review(models.Model):
    request = models.OneToOneField(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name='review'
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Calificación de 1 a 5 estrellas"
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña #{self.id} (Calificación: {self.rating})"

