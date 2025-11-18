# 📘 Mindful Backend - API Reference Guide

**Base URL:** `https://tu-app.ondigitalocean.app` (o `http://localhost:8000` en desarrollo)

**Documentación interactiva:** `/docs` (Swagger UI) o `/redoc` (ReDoc)

---

## 🔐 Autenticación

La API usa **JWT (JSON Web Tokens)** para autenticación. Algunos endpoints requieren que incluyas el token en el header:

```
Authorization: Bearer <tu_token_jwt>
```

### Obtener token
Usa el endpoint `/auth/login` o `/auth/register` para obtener un token.

---

## 📍 Endpoints

### 🏥 Health Check

#### `GET /`
Verifica que la API esté funcionando.

**Request:**
```bash
curl https://tu-app.ondigitalocean.app/
```

**Response:**
```json
{
  "status": "ok",
  "message": "Mindful Backend API is running"
}
```

---

## 👤 Autenticación (`/auth`)

### `POST /auth/register`
Registra un nuevo usuario en el sistema.

**Request Body:**
```json
{
  "email": "usuario@example.com",
  "password": "password123",
  "role": "student",
  "nombre": "Juan",
  "apellido": "Pérez",
  "telefono": "+57 300 123 4567",
  "documento_identidad": "1234567890",
  "direccion": "Calle 123 #45-67, Bogotá"
}
```

**Campos:**
- `email` (string, requerido): Email del usuario (debe ser válido)
- `password` (string, requerido): Contraseña
- `role` (string, opcional): Rol del usuario. Valores: `"student"` (default), `"teacher"`, `"admin"`
- `nombre` (string, opcional): Primer nombre
- `apellido` (string, opcional): Apellidos
- `telefono` (string, opcional): Número de teléfono
- `documento_identidad` (string, opcional): Documento de identidad
- `direccion` (string, opcional): Dirección completa

**Response:**
```json
{
  "user": {
    "id": "uuid-generado",
    "email": "usuario@example.com",
    "role": "student",
    "nombre": "Juan",
    "apellido": "Pérez"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### `POST /auth/login`
Inicia sesión con email y contraseña.

**Request Body:**
```json
{
  "email": "usuario@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error 401:**
```json
{
  "detail": "Invalid credentials"
}
```

---

### `GET /auth/me`
Obtiene la información del usuario autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "sub": "user-id-uuid",
  "email": "usuario@example.com",
  "role": "student"
}
```

**Error 401:**
```json
{
  "detail": "Invalid or expired token"
}
```

---

## 👥 Usuarios (`/users`)

### `GET /users/`
Lista todos los usuarios del sistema.

**Response:**
```json
{
  "users": [
    {
      "id": "uuid",
      "email": "user1@example.com",
      "role": "student",
      "nombre": "Juan",
      "apellido": "Pérez",
      "telefono": "+57 300 123 4567",
      "created_at": "2025-11-18T10:30:00"
    }
  ]
}
```

---

### `GET /users/{id}`
Obtiene información de un usuario específico.

**Parámetros de ruta:**
- `id` (string): ID del usuario

**Response:**
```json
{
  "id": "uuid",
  "email": "usuario@example.com",
  "role": "student",
  "nombre": "Juan",
  "apellido": "Pérez",
  "telefono": "+57 300 123 4567",
  "documento_identidad": "1234567890",
  "direccion": "Calle 123 #45-67",
  "created_at": "2025-11-18T10:30:00"
}
```

**Error 404:**
```json
{
  "detail": "User not found"
}
```

---

### `PATCH /users/{id}`
Actualiza información de un usuario.

**Parámetros de ruta:**
- `id` (string): ID del usuario

**Request Body:** (todos los campos son opcionales)
```json
{
  "nombre": "Juan Carlos",
  "apellido": "Pérez Gómez",
  "telefono": "+57 301 999 8888",
  "direccion": "Nueva dirección"
}
```

**Response:**
```json
{
  "id": "uuid",
  "email": "usuario@example.com",
  "nombre": "Juan Carlos",
  "apellido": "Pérez Gómez",
  "updated_at": "2025-11-18T15:45:00"
}
```

---

## 🎓 Talleres/Workshops (`/workshops`)

### `GET /workshops/`
Lista todos los talleres disponibles (incluye información del propietario).

**Response:**
```json
{
  "workshops": [
    {
      "id": "uuid",
      "title": "Mindfulness para Principiantes",
      "description": "Introducción a técnicas de mindfulness",
      "image_url": "https://example.com/image.jpg",
      "tags": ["mindfulness", "beginner", "meditation"],
      "active": true,
      "ciudad": "Bogotá",
      "direccion": "Carrera 7 #72-35",
      "referencia": "Cerca al Parque Nacional",
      "schedules": [
        {
          "dia": "Lunes",
          "hora_inicio": "09:00",
          "hora_fin": "11:00"
        },
        {
          "dia": "Miércoles",
          "hora_inicio": "14:00",
          "hora_fin": "16:00"
        }
      ],
      "owner_id": "uuid-del-propietario",
      "owner_email": "instructor@example.com",
      "owner_nombre": "María",
      "owner_apellido": "García",
      "created_at": "2025-11-15T08:00:00",
      "updated_at": "2025-11-18T10:00:00"
    }
  ]
}
```

---

### `GET /workshops/by-city/{ciudad}`
Filtra talleres por ciudad.

**Parámetros de ruta:**
- `ciudad` (string): Nombre de la ciudad (ej: "Bogotá", "Medellín")

**Response:**
```json
{
  "workshops": [
    {
      "id": "uuid",
      "title": "Taller de Meditación",
      "ciudad": "Bogotá",
      ...
    }
  ]
}
```

---

### `GET /workshops/by-tags?tags=tag1&tags=tag2`
Filtra talleres por tags (etiquetas).

**Query Parameters:**
- `tags` (array): Lista de tags a buscar

**Ejemplo:**
```bash
GET /workshops/by-tags?tags=mindfulness&tags=beginner
```

**Response:**
```json
{
  "workshops": [
    {
      "id": "uuid",
      "title": "Mindfulness para Principiantes",
      "tags": ["mindfulness", "beginner"],
      ...
    }
  ]
}
```

---

### `POST /workshops/` 🔒
Crea un nuevo taller. **Requiere autenticación.**

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "Taller de Respiración Consciente",
  "description": "Aprende técnicas de respiración para reducir el estrés",
  "image_url": "https://example.com/workshop-image.jpg",
  "tags": ["breathing", "stress-relief", "intermediate"],
  "active": true,
  "ciudad": "Medellín",
  "direccion": "Calle 10 #50-20",
  "referencia": "Edificio Plaza Mayor, piso 3",
  "schedules": [
    {
      "dia": "Martes",
      "hora_inicio": "18:00",
      "hora_fin": "20:00"
    },
    {
      "dia": "Jueves",
      "hora_inicio": "18:00",
      "hora_fin": "20:00"
    }
  ]
}
```

**Campos requeridos:**
- `title` (string): Título del taller
- `ciudad` (string): Ciudad donde se realiza
- `direccion` (string): Dirección exacta

**Campos opcionales:**
- `description` (string): Descripción del taller
- `image_url` (string): URL de la imagen
- `tags` (array): Lista de etiquetas
- `active` (boolean): Si el taller está activo (default: true)
- `referencia` (string): Punto de referencia
- `schedules` (array): Horarios del taller

**Response:**
```json
{
  "id": "uuid-generado",
  "title": "Taller de Respiración Consciente",
  "owner_id": "uuid-del-usuario-autenticado",
  "ciudad": "Medellín",
  "created_at": "2025-11-18T16:00:00"
}
```

**Error 401:**
```json
{
  "detail": "Authentication required"
}
```

---

### `PATCH /workshops/{id}`
Actualiza un taller existente.

**Parámetros de ruta:**
- `id` (string): ID del taller

**Request Body:** (todos los campos son opcionales)
```json
{
  "title": "Nuevo título",
  "description": "Nueva descripción",
  "active": false,
  "schedules": [
    {
      "dia": "Viernes",
      "hora_inicio": "10:00",
      "hora_fin": "12:00"
    }
  ]
}
```

**Response:**
```json
{
  "id": "uuid",
  "title": "Nuevo título",
  "description": "Nueva descripción",
  "active": false,
  "updated_at": "2025-11-18T17:00:00"
}
```

**Error 404:**
```json
{
  "detail": "Workshop not found"
}
```

---

### `DELETE /workshops/{id}`
Elimina un taller.

**Parámetros de ruta:**
- `id` (string): ID del taller

**Response:**
```json
{
  "ok": true
}
```

**Error 404:**
```json
{
  "detail": "Workshop not found"
}
```

---

## 📊 Tracking de Emociones (`/tracking`)

### `POST /tracking/emotion`
Guarda un registro de emoción del usuario.

**Request Body:**
```json
{
  "userId": "uuid-del-usuario",
  "result": {
    "level": "high",
    "score": 0.85,
    "emotion": "stressed"
  }
}
```

**Campos:**
- `userId` (string, requerido): ID del usuario
- `result` (object, requerido): Resultado del análisis emocional
  - Puede contener cualquier estructura (level, score, emotion, etc.)

**Response:**
```json
{
  "id": "uuid-generado",
  "user_id": "uuid-del-usuario",
  "result": {
    "level": "high",
    "score": 0.85,
    "emotion": "stressed"
  },
  "created_at": "2025-11-18T18:30:00"
}
```

---

### `GET /tracking/user/{id}`
Obtiene todos los registros emocionales de un usuario.

**Parámetros de ruta:**
- `id` (string): ID del usuario

**Response:**
```json
{
  "records": [
    {
      "id": "uuid",
      "user_id": "uuid-del-usuario",
      "result": {
        "level": "high",
        "score": 0.85
      },
      "created_at": "2025-11-18T18:30:00"
    },
    {
      "id": "uuid",
      "user_id": "uuid-del-usuario",
      "result": {
        "level": "medium",
        "score": 0.55
      },
      "created_at": "2025-11-17T14:20:00"
    }
  ]
}
```

---

## 💡 Recomendaciones (`/recommendations`)

### `GET /recommendations/{level}`
Obtiene recomendaciones según el nivel de estrés/emoción.

**Parámetros de ruta:**
- `level` (string): Nivel (ej: "low", "medium", "high")

**Ejemplo:**
```bash
GET /recommendations/high
```

**Response:**
```json
{
  "recommendations": [
    "Realiza ejercicios de respiración profunda",
    "Toma un descanso de 10 minutos",
    "Practica meditación guiada",
    "Contacta con un profesional si persiste"
  ]
}
```

---

## 🎤 Análisis de Voz (`/voice`)

### `POST /voice/analyze`
Analiza características de audio de voz para detectar emociones.

**Content-Type:** `multipart/form-data`

**Request Body:**
- `file` (file): Archivo de audio (formato .wav, .mp3, etc.)

**Ejemplo con curl:**
```bash
curl -X POST \
  https://tu-app.ondigitalocean.app/voice/analyze \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio.wav"
```

**Response:**
```json
{
  "features": {
    "pitch": 220.5,
    "energy": 0.75,
    "mfcc": [12.3, 8.9, ...],
    "emotion_detected": "calm"
  }
}
```

---

## 🤖 Modelo de Predicción (`/model`)

### `POST /model/predict_audio`
Envía audio al microservicio del modelo SVM para predicción de emociones.

**Content-Type:** `multipart/form-data`

**Request Body:**
- `file` (file): Archivo de audio .wav

**Ejemplo:**
```bash
curl -X POST \
  https://tu-app.ondigitalocean.app/model/predict_audio \
  -F "file=@recording.wav"
```

**Response:**
```json
{
  "prediction": "stressed",
  "confidence": 0.87,
  "features": {
    "mfcc_mean": [10.2, 5.3, ...],
    "spectral_centroid": 1850.5
  }
}
```

---

## 👨‍💼 Admin (`/admin`)

### `GET /admin/summary`
Obtiene un resumen del dashboard administrativo.

**Response:**
```json
{
  "total_users": 150,
  "total_workshops": 25,
  "active_workshops": 20,
  "total_emotion_records": 3420,
  "users_by_role": {
    "student": 130,
    "teacher": 18,
    "admin": 2
  }
}
```

---

## 🔒 Autenticación en Swagger UI

1. Ve a `/docs`
2. Click en el botón **"Authorize"** (candado verde arriba a la derecha)
3. Ingresa: `Bearer tu_token_aqui`
4. Click en **"Authorize"**
5. Ahora puedes probar endpoints protegidos

---

## 🚨 Códigos de Error Comunes

| Código | Significado |
|--------|-------------|
| 200    | OK - Operación exitosa |
| 401    | Unauthorized - Token inválido o faltante |
| 404    | Not Found - Recurso no encontrado |
| 422    | Validation Error - Datos inválidos en el request |
| 500    | Internal Server Error - Error del servidor |

---

## 📝 Ejemplos de uso completo

### Flujo de registro y creación de taller:

```bash
# 1. Registrar usuario
curl -X POST https://tu-app.ondigitalocean.app/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "instructor@example.com",
    "password": "pass123",
    "role": "teacher",
    "nombre": "María",
    "apellido": "García"
  }'

# Response: {"user": {...}, "token": "eyJhbG..."}

# 2. Crear taller (usando el token)
curl -X POST https://tu-app.ondigitalocean.app/workshops/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbG..." \
  -d '{
    "title": "Mindfulness Avanzado",
    "ciudad": "Bogotá",
    "direccion": "Calle 100 #15-20",
    "schedules": [
      {"dia": "Sábado", "hora_inicio": "10:00", "hora_fin": "12:00"}
    ]
  }'

# 3. Listar todos los talleres
curl https://tu-app.ondigitalocean.app/workshops/
```

---

## 🌐 CORS

La API tiene CORS habilitado para todos los orígenes (`*`) en desarrollo. 

En producción, actualiza `app/main.py` línea 18 con tu dominio específico:
```python
allow_origins=["https://tu-frontend.com"]
```

---

## 📞 Soporte

- **Documentación interactiva:** `/docs` (Swagger UI)
- **Documentación alternativa:** `/redoc` (ReDoc)
- **Health check:** `/`

---

¡Listo para usar! 🚀
