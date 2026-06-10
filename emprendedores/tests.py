from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Category, Service, ServiceRequest, Review

User = get_user_model()

class EmprendedoresTests(APITestCase):
    def setUp(self):
        self.category_plomeria, _ = Category.objects.get_or_create(name='Plomería', defaults={'description': 'Fontanería'})
        self.category_electricidad, _ = Category.objects.get_or_create(name='Electricidad', defaults={'description': 'Eléctricos'})

        self.entrepreneur = User.objects.create_user(
            username='entrepreneur1',
            email='ent1@example.com',
            password='Password123!',
            role='entrepreneur'
        )
        self.resident = User.objects.create_user(
            username='resident1',
            email='res1@example.com',
            password='Password123!',
            role='resident'
        )
        self.other_resident = User.objects.create_user(
            username='resident2',
            email='res2@example.com',
            password='Password123!',
            role='resident'
        )

        self.category_list_url = reverse('category-list')
        self.service_list_url = reverse('service-list')
        self.request_list_url = reverse('request-list')
        self.review_list_url = reverse('review-list')

    def test_category_list_public(self):
        response = self.client.get(self.category_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_create_service_role_enforcement(self):
        service_data = {
            'category': self.category_plomeria.id,
            'title': 'Reparación de goteras',
            'description': 'Reparo goteras y tuberías de cocina',
            'price_estimate': '50.00',
            'horarios_disponibilidad': 'Lunes a Viernes 8am - 12pm'
        }

        response = self.client.post(self.service_list_url, service_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.resident)
        response = self.client.post(self.service_list_url, service_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.entrepreneur)
        response = self.client.post(self.service_list_url, service_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Service.objects.count(), 1)
        self.assertEqual(Service.objects.first().entrepreneur, self.entrepreneur)

    def test_filter_services_by_category(self):
        Service.objects.create(
            entrepreneur=self.entrepreneur,
            category=self.category_plomeria,
            title='Servicio Plomería',
            description='Plomero profesional',
            horarios_disponibilidad='Cualquier horario'
        )
        Service.objects.create(
            entrepreneur=self.entrepreneur,
            category=self.category_electricidad,
            title='Servicio Electricidad',
            description='Electricista profesional',
            horarios_disponibilidad='Cualquier horario'
        )

        response = self.client.get(f"{self.service_list_url}?category={self.category_plomeria.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Servicio Plomería')

    def test_service_request_lifecycle(self):
        service = Service.objects.create(
            entrepreneur=self.entrepreneur,
            category=self.category_plomeria,
            title='Servicio Plomería',
            description='Plomero profesional',
            horarios_disponibilidad='Cualquier horario'
        )

        request_data = {
            'service': service.id,
            'scheduled_datetime': timezone.now() + timezone.timedelta(days=1),
            'description': 'Tubería rota en el baño'
        }

        self.client.force_authenticate(user=self.resident)
        response = self.client.post(self.request_list_url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        req_id = response.data['id']
        service_request = ServiceRequest.objects.get(id=req_id)
        self.assertEqual(service_request.status, 'pending')

        review_data = {
            'request': req_id,
            'rating': 5,
            'comment': 'Excelente trabajo'
        }
        response = self.client.post(self.review_list_url, review_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.force_authenticate(user=self.entrepreneur)
        accept_url = reverse('request-accept', args=[req_id])
        response = self.client.post(accept_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'accepted')

        complete_url = reverse('request-complete', args=[req_id])
        response = self.client.post(complete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')

        self.client.force_authenticate(user=self.other_resident)
        response = self.client.post(self.review_list_url, review_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.force_authenticate(user=self.resident)
        response = self.client.post(self.review_list_url, review_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

