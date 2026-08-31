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

ALTER TABLE gobierno_escolar ADD COLUMN IF NOT EXISTS nivel VARCHAR(10) NOT NULL DEFAULT 'base';
ALTER TABLE equipo_desarrollo ADD COLUMN IF NOT EXISTS nivel VARCHAR(10) NOT NULL DEFAULT 'base';
ALTER TABLE comite_ecologico ADD COLUMN IF NOT EXISTS nivel VARCHAR(10) NOT NULL DEFAULT 'base';
ALTER TABLE comunidad_educativa ADD COLUMN IF NOT EXISTS nivel VARCHAR(10) NOT NULL DEFAULT 'base';

CREATE TABLE IF NOT EXISTS equipo_drones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    rol VARCHAR(150),
    foto_url TEXT,
    orden INTEGER NOT NULL DEFAULT 0,
    nivel VARCHAR(10) NOT NULL DEFAULT 'base',
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS coheteria (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    rol VARCHAR(150),
    foto_url TEXT,
    orden INTEGER NOT NULL DEFAULT 0,
    nivel VARCHAR(10) NOT NULL DEFAULT 'base',
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

ALTER TABLE institucion_info ADD COLUMN IF NOT EXISTS articulado_texto TEXT;
ALTER TABLE institucion_info ADD COLUMN IF NOT EXISTS investigacion_texto TEXT;

ALTER TABLE deportes ADD COLUMN IF NOT EXISTS imagen_url TEXT;
ALTER TABLE deportes ADD COLUMN IF NOT EXISTS descripcion TEXT;

CREATE TABLE IF NOT EXISTS media_tecnica_categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    imagen_url TEXT,
    descripcion TEXT,
    orden INTEGER NOT NULL DEFAULT 0,
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO media_tecnica_categorias (nombre, orden)
SELECT * FROM (VALUES
    ('Sistemas Teleinformáticos', 1),
    ('Internet de las Cosas', 2),
    ('Programación de Software', 3)
) AS datos(nombre, orden)
WHERE NOT EXISTS (SELECT 1 FROM media_tecnica_categorias);

CREATE TABLE IF NOT EXISTS comite_ecologico (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    rol VARCHAR(150),
    foto_url TEXT,
    orden INTEGER NOT NULL DEFAULT 0,
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS grupos_estudiantiles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    encargado VARCHAR(100),
    foto_url VARCHAR(255),
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO grupos_estudiantiles (nombre)
SELECT * FROM (VALUES
    ('Comité Ecológico'),
    ('Equipo de Desarrollo'),
    ('Equipo de Drones'),
    ('Cohetería')
) AS datos(nombre)
WHERE NOT EXISTS (SELECT 1 FROM grupos_estudiantiles);

ALTER TABLE grupos_estudiantiles ADD COLUMN IF NOT EXISTS enlace_url VARCHAR(255);

UPDATE grupos_estudiantiles SET enlace_url = '/comite-ecologico' WHERE nombre = 'Comité Ecológico' AND enlace_url IS NULL;
UPDATE grupos_estudiantiles SET enlace_url = '/equipo-desarrollo' WHERE nombre = 'Equipo de Desarrollo' AND enlace_url IS NULL;
UPDATE grupos_estudiantiles SET enlace_url = '/equipo-drones' WHERE nombre = 'Equipo de Drones' AND enlace_url IS NULL;
UPDATE grupos_estudiantiles SET enlace_url = '/coheteria' WHERE nombre = 'Cohetería' AND enlace_url IS NULL;
