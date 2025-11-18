# Deployment Guide - Mindful Backend

Este documento contiene las instrucciones para hacer deploy del backend en diferentes plataformas.

## 🚀 Comandos de deployment

### Para Render / Railway / Heroku

**Comando de inicio (Start Command):**

Opción 1 - Simple (uvicorn):
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Opción 2 - Producción con workers (gunicorn + uvicorn):
```bash
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### Para Docker

**Dockerfile básico:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

## 🔐 Variables de entorno necesarias

Configura estas variables en tu plataforma de deployment:

```bash
# Supabase
SUPABASE_URL=https://rjhpthtxbvbctholyiff.supabase.co
SUPABASE_KEY=tu_supabase_anon_key

# JWT
SECRET_KEY=tu-secret-key-seguro-aqui
ALGORITHM=HS256

# Opcional - URL del modelo ML
MODEL_API_URL=http://tu-modelo-api:5000
```

## 📋 Checklist pre-deployment

- [ ] Ejecutar migraciones SQL en Supabase
- [ ] Configurar variables de entorno en la plataforma
- [ ] Actualizar CORS origins en `app/main.py` (línea 18)
- [ ] Verificar que `requirements.txt` está actualizado
- [ ] Cambiar `SECRET_KEY` por uno seguro en producción

## 🧪 Testing local

**Desarrollo (con hot reload):**
```bash
python run.py
```

**Simular producción localmente:**
```bash
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🔗 Endpoints principales

- **Health Check:** `GET /`
- **Docs:** `GET /docs`
- **OpenAPI:** `GET /openapi.json`

## 📝 Notas importantes

1. **No commitear** `.env` o `.env.local` al repositorio
2. La aplicación usa el puerto `$PORT` en producción (variable de entorno)
3. El archivo `run.py` es solo para desarrollo local
4. Para deployment, el entry point es `app.main:app`

## 🛠️ Configuración específica por plataforma

### DigitalOcean App Platform

**Método 1: Usando la interfaz web**
1. Ve a https://cloud.digitalocean.com/apps
2. Click en "Create App"
3. Conecta tu repositorio de GitHub
4. Configuración:
   - **Type:** Web Service
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Run Command:** `gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
   - **HTTP Port:** 8000 (o deja vacío para que use $PORT automáticamente)

5. Variables de entorno (Environment Variables):
   ```
   SUPABASE_URL=https://rjhpthtxbvbctholyiff.supabase.co
   SUPABASE_KEY=tu_supabase_anon_key
   SECRET_KEY=tu-secret-key-seguro
   ALGORITHM=HS256
   ```

**Método 2: Usando archivo de configuración (.do/app.yaml)**

Crea el archivo `.do/app.yaml` en la raíz del proyecto:

```yaml
name: mindful-backend
services:
  - name: api
    github:
      repo: MindFului/mindful-backend
      branch: main
      deploy_on_push: true
    
    source_dir: /
    
    build_command: pip install -r requirements.txt
    
    run_command: gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
    
    http_port: 8000
    
    instance_count: 1
    instance_size_slug: basic-xxs
    
    envs:
      - key: SUPABASE_URL
        value: https://rjhpthtxbvbctholyiff.supabase.co
      - key: SUPABASE_KEY
        scope: RUN_TIME
        type: SECRET
      - key: SECRET_KEY
        scope: RUN_TIME
        type: SECRET
      - key: ALGORITHM
        value: HS256
    
    health_check:
      http_path: /
      initial_delay_seconds: 10
      period_seconds: 10
      timeout_seconds: 3
      success_threshold: 1
      failure_threshold: 3
```

**Método 3: Usando CLI de DigitalOcean**

```bash
# Instalar doctl (CLI de DigitalOcean)
# macOS
brew install doctl

# Autenticarse
doctl auth init

# Crear app desde archivo de configuración
doctl apps create --spec .do/app.yaml

# O crear directamente
doctl apps create --upsert \
  --build-command "pip install -r requirements.txt" \
  --run-command "gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:\$PORT"
```

**Configuración de dominio personalizado:**
1. En el dashboard de tu app, ve a "Settings"
2. Click en "Domains"
3. Agrega tu dominio personalizado
4. Configura los registros DNS según las instrucciones

**Escalado automático (opcional):**
```yaml
# Agregar en .do/app.yaml
    autoscaling:
      min_instance_count: 1
      max_instance_count: 3
      metrics:
        cpu:
          percent: 80
```

### Render
```yaml
# render.yaml
services:
  - type: web
    name: mindful-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### Railway
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

### Heroku (Procfile)
```
web: gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```
