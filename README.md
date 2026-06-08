# ComuniApp - Plataforma de Servicios Locales

## Descripción del proyecto
ComuniApp es una plataforma virtual diseñada para conectar a emprendedores locales con los residentes de su comunidad. El sistema permite a los emprendedores registrar y publicar los servicios que ofrecen (detallando precios, descripciones y horarios de disponibilidad simples). Por otro lado, los residentes pueden explorar servicios categorizados, solicitar atención y dejar reseñas o calificaciones basadas en su experiencia. El objetivo principal es mejorar la comunicación y fomentar el consumo de servicios locales dentro de la comunidad.

## Arquitectura general del sistema
El sistema está diseñado bajo una arquitectura Cliente-Servidor. El backend provee una **API RESTful** que puede ser consumida por cualquier cliente (aplicación web, móvil, etc.). 

- **Autenticación y Autorización:** Implementa seguridad basada en JSON Web Tokens (JWT). Los usuarios se dividen por roles (`resident` y `entrepreneur`), lo que restringe el acceso a ciertas funcionalidades (ej. solo los emprendedores pueden crear servicios, y solo los residentes pueden solicitar servicios o dejar reseñas).
- **Módulos Principales:**
  - `authentication`: Maneja el modelo de usuario personalizado (con roles), el registro y la generación de tokens.
  - `emprendedores`: Maneja la lógica central del negocio: Categorías, Servicios, Solicitudes (ServiceRequests) y Reseñas (Reviews).
- **Base de Datos:** Utiliza PostgreSQL (actualmente alojado en la nube con Render) para asegurar integridad relacional y escalabilidad.

## Tecnologías utilizadas
- **Lenguaje:** Python 3
- **Framework Web:** Django
- **API REST:** Django REST Framework (DRF)
- **Autenticación:** djangorestframework-simplejwt (JWT)
- **Base de Datos:** PostgreSQL
- **Documentación de API:** drf-yasg (Swagger UI / ReDoc)
- **Gestión de Entorno:** django-environ, dj-database-url, django-cors-headers

## Guía de instalación del sistema

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd Actividad1-disenor-software
   ```

2. **Crear un entorno virtual (recomendado):**
   ```bash
   python -m venv .venv
   ```

3. **Activar el entorno virtual:**
   - En Windows: `.\.venv\Scripts\activate`
   - En macOS/Linux: `source .venv/bin/activate`

4. **Instalar las dependencias del proyecto:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar las variables de entorno:**
   Asegúrate de contar con un archivo `.env` en la raíz del proyecto (donde se encuentra `manage.py`) con el siguiente formato:
   ```env
   DEBUG=True
   SECRET_KEY=tu-secret-key-segura
   DATABASE_URL=postgresql://<usuario>:<password>@<host>/<nombre_db>
   ```
   *(Nota: Actualmente el proyecto ya se conecta a una base de datos PostgreSQL remota en Render).*

## Instrucciones para ejecutar el proyecto localmente

1. **Activar el entorno virtual** (si no lo está).
2. **Aplicar las migraciones:** 
   *(Si estás usando la base de datos remota de Render esto ya está hecho, pero si configuras una base de datos local nueva, debes ejecutarlo).*
   ```bash
   python manage.py migrate
   ```
3. **Ejecutar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```
4. **Explorar la API:**
   Abre tu navegador y dirígete a las siguientes rutas para visualizar y probar los endpoints:
   - **Swagger UI:** [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
   - **ReDoc:** [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)
   - **Ruta de Servicios (Ejemplo):** [http://127.0.0.1:8000/api/emprendedores/services/](http://127.0.0.1:8000/api/emprendedores/services/)

## Pruebas (Testing)
Para ejecutar las pruebas automatizadas (Unit tests / Integration tests) y comprobar el correcto funcionamiento de los módulos y los roles, ejecuta:
```bash
python manage.py test
```
