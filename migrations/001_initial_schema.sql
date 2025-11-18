-- Script de migración para crear las tablas en Supabase
-- Ejecuta este script en el SQL Editor de Supabase

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'student',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para búsqueda por email
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Tabla de workshops
CREATE TABLE IF NOT EXISTS workshops (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    tags TEXT[], -- Array de strings para tags
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para búsqueda por tags
CREATE INDEX IF NOT EXISTS idx_workshops_tags ON workshops USING GIN(tags);

-- Tabla de registros de emociones (tracking)
CREATE TABLE IF NOT EXISTS emotion_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    result JSONB NOT NULL, -- {level, score} almacenado como JSON
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para búsqueda por usuario
CREATE INDEX IF NOT EXISTS idx_emotion_records_user_id ON emotion_records(user_id);

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers para actualizar updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workshops_updated_at
    BEFORE UPDATE ON workshops
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Deshabilitar Row Level Security (RLS) temporalmente para desarrollo
-- Para producción, habilitar RLS y ajustar políticas según necesidades
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE workshops DISABLE ROW LEVEL SECURITY;
ALTER TABLE emotion_records DISABLE ROW LEVEL SECURITY;

-- IMPORTANTE: En producción, habilita RLS y configura políticas apropiadas
-- Ejemplo de políticas para producción (comentadas por ahora):
/*
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE workshops ENABLE ROW LEVEL SECURITY;
ALTER TABLE emotion_records ENABLE ROW LEVEL SECURITY;

-- Permitir registro público de usuarios
CREATE POLICY "Anyone can insert users" 
    ON users FOR INSERT 
    WITH CHECK (true);

-- Permitir lectura/actualización de propios datos
CREATE POLICY "Users can view their own data" 
    ON users FOR SELECT 
    USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update their own data" 
    ON users FOR UPDATE 
    USING (auth.uid()::text = id::text);

-- Workshops públicos visibles para todos
CREATE POLICY "Public workshops are viewable" 
    ON workshops FOR SELECT 
    USING (active = TRUE);

-- Emotion records - usuarios pueden crear y ver sus propios registros
CREATE POLICY "Users can insert their emotion records" 
    ON emotion_records FOR INSERT 
    WITH CHECK (true);

CREATE POLICY "Users can view their emotion records" 
    ON emotion_records FOR SELECT 
    USING (true);
*/
