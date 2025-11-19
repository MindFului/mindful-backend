# 🔄 Cambios: Sistema de Estados para Workshops

## ✅ Cambios Implementados

### 1. **Nuevo campo `status` (reemplaza `active`)**

En lugar de un campo booleano `active` (true/false), ahora los workshops tienen un campo `status` con 3 posibles valores:

- **`"active"`** - Taller activo y visible públicamente
- **`"inactive"`** - Taller inactivo, no visible
- **`"pending"`** - Taller pendiente de aprobación (default al crear)

### 2. **Archivos modificados:**

#### ✅ `app/modules/workshops/schemas.py`
- Agregado enum `WorkshopStatus` con los 3 valores
- `WorkshopCreateDTO.status` ahora es tipo `WorkshopStatus` (default: `"pending"`)
- `WorkshopUpdateDTO.status` ahora es tipo `WorkshopStatus` (opcional)
- `WorkshopResponse.status` ahora es tipo `WorkshopStatus`

#### ✅ `app/modules/workshops/router.py`
- Query parameter cambiado de `active` (bool) a `status` (WorkshopStatus)
- Endpoint `GET /workshops/?status={active|inactive|pending}`

#### ✅ `app/modules/workshops/service.py`
- `list(status=None)` - Filtra por status si se proporciona, sino trae todos
- `create()` - Usa `status` con default `"pending"`
- `find_by_tags()` - Solo busca workshops con `status="active"`
- `find_by_city()` - Solo busca workshops con `status="active"`
- `patch()` - Maneja conversión de enum a string para actualización

#### ✅ `API_GUIDE.md`
- Documentación actualizada con los nuevos valores de `status`
- Ejemplos de filtrado por status
- Campo `status` reemplaza `active` en todos los ejemplos

### 3. **Migración de base de datos:**

**Archivo:** `migrations/003_add_workshop_status.sql`

Este script SQL debe ejecutarse en Supabase para:
1. Agregar columna `status` (VARCHAR)
2. Migrar datos existentes: `active=true` → `"active"`, `active=false` → `"inactive"`
3. Agregar constraint para validar valores
4. Crear índice para búsquedas por status

⚠️ **Nota:** El script mantiene temporalmente ambas columnas (`active` y `status`) para permitir rollback. Puedes eliminar la columna `active` después de verificar que todo funciona.

---

## 📋 Cómo usar el nuevo sistema

### Crear un workshop (default: pending)
```json
POST /workshops/
{
  "title": "Nuevo Taller",
  "ciudad": "Bogotá",
  "direccion": "Calle 123"
  // status será "pending" por defecto
}
```

### Crear un workshop activo
```json
POST /workshops/
{
  "title": "Nuevo Taller",
  "ciudad": "Bogotá",
  "direccion": "Calle 123",
  "status": "active"
}
```

### Aprobar un workshop (pending → active)
```json
PATCH /workshops/{id}
{
  "status": "active"
}
```

### Desactivar un workshop
```json
PATCH /workshops/{id}
{
  "status": "inactive"
}
```

### Filtrar workshops

```bash
# Todos
GET /workshops/

# Solo activos (públicos)
GET /workshops/?status=active

# Solo pendientes (esperando aprobación)
GET /workshops/?status=pending

# Solo inactivos
GET /workshops/?status=inactive
```

---

## 🚀 Pasos siguientes

1. **Ejecutar migración SQL:**
   - Ve a Supabase SQL Editor
   - Ejecuta `migrations/003_add_workshop_status.sql`
   - Verifica que los datos se migraron correctamente

2. **Validar endpoints:**
   - Prueba crear un workshop (debe tener `status: "pending"`)
   - Prueba filtrar por cada status
   - Prueba actualizar el status con PATCH

3. **Opcional - Limpiar código:**
   - Después de validar, puedes ejecutar:
     ```sql
     ALTER TABLE workshops DROP COLUMN IF EXISTS active;
     DROP INDEX IF EXISTS idx_workshops_active;
     ```

---

## 🔄 Flujo de trabajo recomendado

### Para workshops públicos:
1. Usuario crea workshop → `status: "pending"`
2. Admin revisa y aprueba → `PATCH status: "active"`
3. Workshop es visible en `/workshops/?status=active`
4. Usuarios pueden buscarlo por ciudad/tags

### Para moderar workshops:
1. GET `/workshops/?status=pending` → Lista workshops pendientes
2. Revisar cada uno
3. Aprobar: `PATCH {id} {"status": "active"}`
4. Rechazar/Desactivar: `PATCH {id} {"status": "inactive"}`

---

¡Todo listo para usar el nuevo sistema de estados! 🎉
