-- Migración: Cambiar campo 'active' por 'status' con valores: active, inactive, pending
-- Ejecuta este script en el SQL Editor de Supabase

-- Paso 1: Agregar nueva columna 'status'
ALTER TABLE workshops 
ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'pending';

-- Paso 2: Migrar datos existentes (active=true -> 'active', active=false -> 'inactive')
UPDATE workshops 
SET status = CASE 
    WHEN active = true THEN 'active'
    WHEN active = false THEN 'inactive'
    ELSE 'pending'
END
WHERE status = 'pending'; -- Solo actualizar los que aún no tienen status definido

-- Paso 3: Eliminar la columna antigua 'active' (opcional, comentado por seguridad)
-- Descomenta la siguiente línea solo si estás seguro de eliminar el campo 'active'
-- ALTER TABLE workshops DROP COLUMN IF EXISTS active;

-- Paso 4: Agregar constraint para validar valores
ALTER TABLE workshops
ADD CONSTRAINT workshops_status_check 
CHECK (status IN ('active', 'inactive', 'pending'));

-- Paso 5: Crear índice para búsquedas por status
CREATE INDEX IF NOT EXISTS idx_workshops_status ON workshops(status);

-- Paso 6: Eliminar índice antiguo de 'active' si ya no se usa
-- Descomenta la siguiente línea si eliminaste la columna 'active'
-- DROP INDEX IF EXISTS idx_workshops_active;

-- Nota: Mantener ambas columnas temporalmente permite rollback fácil si hay problemas
