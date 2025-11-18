# Guía Rápida: Deploy en DigitalOcean

## ⚠️ IMPORTANTE: Python 3.11 requerido

Este proyecto **DEBE usar Python 3.11** (no 3.12 ni 3.13) por compatibilidad con FastAPI 0.95.2 y Pydantic 1.10.12.

El archivo `runtime.txt` asegura que se use Python 3.11.10 en el deploy.

## 📦 Pasos para hacer deploy

### Opción 1: Usando la interfaz web (más fácil)

1. **Preparar el repositorio:**
   ```bash
   # Asegúrate de tener todos los cambios commiteados
   git add .
   git commit -m "Preparar para deploy en DigitalOcean"
   git push origin main
   ```

2. **Crear la app en DigitalOcean:**
   - Ve a: https://cloud.digitalocean.com/apps
   - Click "Create App"
   - Selecciona "GitHub" y conecta tu cuenta
   - Elige el repositorio `MindFului/mindful-backend`
   - Branch: `main`

3. **Configurar el servicio:**
   - **Type:** Web Service
   - **Build Command:** `pip install -r requirements.txt`
   - **Run Command:** `gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
   - **HTTP Port:** 8000

4. **Configurar variables de entorno:**
   ```
   SUPABASE_URL = https://rjhpthtxbvbctholyiff.supabase.co
   SUPABASE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (tu key completa)
   SECRET_KEY = genera-un-secret-key-seguro-aqui
   ALGORITHM = HS256
   ```

5. **Click en "Create Resources"** y espera el deploy (~2-3 minutos)

### Opción 2: Usando el archivo .do/app.yaml (automático)

1. **El archivo ya está configurado** en `.do/app.yaml`

2. **Actualiza los secretos en DigitalOcean:**
   - Ve a tu app creada
   - Settings → App-Level Environment Variables
   - Agrega:
     - `SUPABASE_KEY` (marca como "Encrypt")
     - `SECRET_KEY` (marca como "Encrypt")

3. **DigitalOcean detectará automáticamente** el archivo `.do/app.yaml` y usará esa configuración

### Opción 3: Usando CLI (para usuarios avanzados)

```bash
# 1. Instalar doctl
brew install doctl  # macOS
# sudo snap install doctl  # Linux

# 2. Autenticarse
doctl auth init

# 3. Crear app desde el archivo de configuración
doctl apps create --spec .do/app.yaml

# 4. Ver el progreso
doctl apps list

# 5. Ver logs
doctl apps logs <app-id> --follow
```

## ✅ Verificar el deploy

Una vez deployado, verifica:

1. **Health check:** `https://tu-app.ondigitalocean.app/`
   - Deberías ver: `{"status": "ok", "message": "Mindful Backend API is running"}`

2. **Documentación:** `https://tu-app.ondigitalocean.app/docs`
   - Verás la interfaz Swagger UI

3. **Probar un endpoint:** `GET https://tu-app.ondigitalocean.app/workshops/`

## 🔧 Troubleshooting

**Error: "TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument"**
- ⚠️ **Este es el error más común**: la plataforma está usando Python 3.12 o 3.13
- ✅ **Solución**: Asegúrate de que el archivo `runtime.txt` existe con el contenido `python-3.11.10`
- Haz commit y push del archivo `runtime.txt`
- Fuerza un nuevo deploy

**Error: "Module not found"**
- Verifica que `requirements.txt` esté actualizado
- En el dashboard, ve a "Settings" → "General" → fuerza un nuevo deploy

**Error: "Cannot connect to database"**
- Verifica las variables de entorno `SUPABASE_URL` y `SUPABASE_KEY`
- Asegúrate de ejecutar el script SQL en Supabase (ver `/migrations/002_add_user_profile_workshop_extended.sql`)

**Error 503 / App no arranca**
- Ve a "Runtime Logs" en el dashboard
- Busca el error específico en los logs

## 💰 Costos

- **Basic XXS:** $5/mes (512MB RAM) - Suficiente para desarrollo
- **Basic XS:** $12/mes (1GB RAM) - Recomendado para producción pequeña
- **Basic S:** $24/mes (2GB RAM) - Para producción mediana

## 🚀 Re-deploys automáticos

Cada vez que hagas `git push origin main`, DigitalOcean hará deploy automáticamente.

Para desactivar:
- Settings → General → "Auto Deploy" → Toggle OFF

## 📝 Siguiente paso

Después del deploy, actualiza el frontend para que apunte a:
```
https://tu-app.ondigitalocean.app
```

¡Listo! 🎉
