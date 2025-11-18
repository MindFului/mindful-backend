-- Migración para agregar campos adicionales a usuarios y workshops
-- Ejecuta este script si ya tienes las tablas creadas

-- Agregar campos de perfil a la tabla users
ALTER TABLE users ADD COLUMN IF NOT EXISTS nombre VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS apellido VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS telefono VARCHAR(20);
ALTER TABLE users ADD COLUMN IF NOT EXISTS documento_identidad VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS direccion TEXT;

-- Agregar índice por role
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- Agregar campos extendidos a la tabla workshops
ALTER TABLE workshops ADD COLUMN IF NOT EXISTS image_url TEXT;
ALTER TABLE workshops ADD COLUMN IF NOT EXISTS ciudad VARCHAR(100);
ALTER TABLE workshops ADD COLUMN IF NOT EXISTS direccion TEXT;
ALTER TABLE workshops ADD COLUMN IF NOT EXISTS referencia TEXT;
ALTER TABLE workshops ADD COLUMN IF NOT EXISTS schedules JSONB DEFAULT '[]'::jsonb;
ALTER TABLE workshops ADD COLUMN IF NOT EXISTS owner_id UUID;

-- Agregar foreign key si no existe (puede fallar si ya existe)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'workshops_owner_id_fkey'
    ) THEN
        ALTER TABLE workshops 
        ADD CONSTRAINT workshops_owner_id_fkey 
        FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE;
    END IF;
END $$;

-- Agregar índices adicionales
CREATE INDEX IF NOT EXISTS idx_workshops_ciudad ON workshops(ciudad);
CREATE INDEX IF NOT EXISTS idx_workshops_owner_id ON workshops(owner_id);
CREATE INDEX IF NOT EXISTS idx_workshops_active ON workshops(active);

-- Si necesitas actualizar workshops existentes con un owner_id por defecto:
-- UPDATE workshops SET owner_id = (SELECT id FROM users WHERE role = 'ownerWorkshop' LIMIT 1) WHERE owner_id IS NULL;

-- Hacer owner_id NOT NULL después de asignar valores (descomentar si aplica)
-- ALTER TABLE workshops ALTER COLUMN owner_id SET NOT NULL;
-- ALTER TABLE workshops ALTER COLUMN ciudad SET NOT NULL;
-- ALTER TABLE workshops ALTER COLUMN direccion SET NOT NULL;
