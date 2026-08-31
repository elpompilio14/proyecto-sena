-- Actualiza una base de datos existente con los cambios agregados en esta sesion
-- (Gobierno Escolar, Equipo de Desarrollo, Plataforma Virtual, Manual de Convivencia,
-- fecha editable en galeria de fotos). Seguro de correr varias veces, no borra nada.

ALTER TABLE institucion_info ADD COLUMN IF NOT EXISTS plataforma_virtual_url TEXT;
ALTER TABLE institucion_info ADD COLUMN IF NOT EXISTS plataforma_virtual_logo_url TEXT;
ALTER TABLE institucion_info ADD COLUMN IF NOT EXISTS manual_convivencia_url TEXT;
ALTER TABLE institucion_info ADD COLUMN IF NOT EXISTS manual_convivencia_imagen_url TEXT;

CREATE TABLE IF NOT EXISTS gobierno_escolar (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    rol VARCHAR(150),
    foto_url TEXT,
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS equipo_desarrollo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    rol VARCHAR(150),
    foto_url TEXT,
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

ALTER TABLE galeria_fotos ADD COLUMN IF NOT EXISTS fecha DATE;
UPDATE galeria_fotos SET fecha = creado_en::date WHERE fecha IS NULL;
ALTER TABLE galeria_fotos ALTER COLUMN fecha SET DEFAULT CURRENT_DATE;
ALTER TABLE galeria_fotos ALTER COLUMN fecha SET NOT NULL;

ALTER TABLE comunidad_educativa ADD COLUMN IF NOT EXISTS orden INTEGER NOT NULL DEFAULT 0;
ALTER TABLE gobierno_escolar ADD COLUMN IF NOT EXISTS orden INTEGER NOT NULL DEFAULT 0;
ALTER TABLE equipo_desarrollo ADD COLUMN IF NOT EXISTS orden INTEGER NOT NULL DEFAULT 0;

ALTER TABLE galeria_fotos ADD COLUMN IF NOT EXISTS orden INTEGER NOT NULL DEFAULT 1;
ALTER TABLE galeria_fotos ALTER COLUMN orden SET DEFAULT 1;

ALTER TABLE institucion_info ADD COLUMN IF NOT EXISTS articulado_texto TEXT;
ALTER TABLE institucion_info ADD COLUMN IF NOT EXISTS investigacion_texto TEXT;

CREATE TABLE IF NOT EXISTS comite_ecologico (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    rol VARCHAR(150),
    foto_url TEXT,
    orden INTEGER NOT NULL DEFAULT 0,
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);
