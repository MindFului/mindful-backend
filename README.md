# Mindful Backend - Integración con Supabase

Backend FastAPI integrado con Supabase para gestión de usuarios, talleres y seguimiento emocional.

## 🚀 Configuración Inicial

### 1. Crear las tablas en Supabase

1. Ve a tu proyecto en Supabase: https://rjhpthtxbvbctholyiff.supabase.co
2. Navega a **SQL Editor** en el panel lateral
3. Copia y pega todo el contenido del archivo `migrations/001_initial_schema.sql`
4. Ejecuta el script (botón "Run")

Esto creará las siguientes tablas:
- `users` - Usuarios del sistema
- `workshops` - Talleres disponibles
- `emotion_records` - Registros de seguimiento emocional

### 2. Instalar dependencias

```bash
# Si aún no tienes Python 3.11, instálalo
brew install python@3.11

# Crear entorno virtual con Python 3.11
/opt/homebrew/opt/python@3.11/bin/python3.11 -m venv .venv311

# Activar el entorno virtual
source .venv311/bin/activate

# Actualizar pip
python -m pip install --upgrade pip setuptools

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Verificar configuración

El archivo `.env.local` ya contiene tus credenciales de Supabase:
- URL: https://rjhpthtxbvbctholyiff.supabase.co
- API Key: (anon key configurada)

## 🏃 Ejecutar la aplicación

```bash
# Asegúrate de tener el venv activado
source .venv311/bin/activate

# Ejecutar el servidor
python run.py
```

El servidor arrancará en: http://localhost:8000

## 📚 Documentación de la API

Una vez que el servidor esté corriendo, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 Endpoints principales

### Auth
- `POST /auth/register` - Registrar nuevo usuario
- `POST /auth/login` - Login (retorna JWT)

### Users
- `GET /users/{user_id}` - Obtener usuario por ID
- `GET /users/all` - Listar todos los usuarios
- `PATCH /users/{user_id}` - Actualizar usuario

### Workshops
- `GET /workshops/` - Listar todos los talleres
- `POST /workshops/` - Crear nuevo taller
- `GET /workshops/by-tags?tags=...` - Buscar por tags
- `PATCH /workshops/{workshop_id}` - Actualizar taller
- `DELETE /workshops/{workshop_id}` - Eliminar taller

### Tracking
- `POST /tracking/emotion` - Guardar registro emocional
- `GET /tracking/{user_id}` - Obtener registros de un usuario

## 🗄️ Estructura de la base de datos

### Tabla: users
```sql
id          UUID        (PK)
email       VARCHAR     (UNIQUE)
password    VARCHAR     (hash bcrypt)
role        VARCHAR     (default: 'student')
created_at  TIMESTAMP
updated_at  TIMESTAMP
```

### Tabla: workshops
```sql
id          UUID        (PK)
title       VARCHAR
description TEXT
tags        TEXT[]      (array)
active      BOOLEAN
created_at  TIMESTAMP
updated_at  TIMESTAMP
```

### Tabla: emotion_records
```sql
id          UUID        (PK)
user_id     UUID        (FK -> users)
result      JSONB       ({level, score})
created_at  TIMESTAMP
```

## 🔐 Seguridad

- Row Level Security (RLS) habilitado en todas las tablas
- Políticas de acceso configuradas para usuarios autenticados
- JWT para autenticación con expiración de 7 días
- Passwords hasheados con bcrypt

## 🛠️ Archivos modificados/creados

### Nuevos archivos:
- `.env.local` - Variables de entorno con credenciales
- `.env.example` - Template de variables de entorno
- `app/core/config.py` - Configuración centralizada
- `app/core/database.py` - Cliente Supabase singleton
- `migrations/001_initial_schema.sql` - Script SQL de migración

### Archivos actualizados:
- `requirements.txt` - Agregadas dependencias: supabase, python-dotenv
- `app/core/security.py` - Usa configuración centralizada
- `app/modules/auth/service.py` - Integración con Supabase
- `app/modules/users/service.py` - Integración con Supabase
- `app/modules/workshops/service.py` - Integración con Supabase
- `app/modules/tracking/service.py` - Integración con Supabase

## 📝 Notas importantes

1. **Python 3.11 requerido**: FastAPI 0.95.2 con Pydantic v1 no es compatible con Python 3.12
2. **Migrations**: Ejecuta el script SQL en Supabase antes de arrancar la app
3. **RLS Policies**: Las políticas actuales permiten:
   - Lectura pública de workshops activos
   - Los usuarios pueden ver/editar solo sus propios datos
   - Para operaciones de admin, considera usar `service_role` key

## 🚨 Troubleshooting

### Error: "relation 'users' does not exist"
→ Ejecuta el script SQL de migración en Supabase

### Error: "ForwardRef._evaluate() missing argument"
→ Verifica que estás usando Python 3.11 (no 3.12):
```bash
python --version  # Debe mostrar Python 3.11.x
```

### Error de conexión a Supabase
→ Verifica que las credenciales en `.env.local` sean correctas
→ Verifica que tu proyecto de Supabase esté activo

## 📞 Próximos pasos

1. ✅ Ejecutar script SQL en Supabase
2. ✅ Instalar dependencias con Python 3.11
3. ✅ Arrancar la aplicación
4. 🔄 Probar endpoints con la documentación Swagger
5. 🔄 Ajustar políticas RLS según necesidades
