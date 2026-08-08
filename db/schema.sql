-- Esquema de base de datos - Pagina web del colegio (Proyecto SENA)
-- PostgreSQL

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'usuario' CHECK (rol IN ('admin', 'usuario')),
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE institucion_info (
    id SERIAL PRIMARY KEY,
    historia TEXT,
    mision TEXT,
    vision TEXT,
    principios TEXT,
    valores TEXT,
    escudo_texto TEXT,
    escudo_url TEXT,
    bandera_texto TEXT,
    bandera_url TEXT,
    ubicacion TEXT,
    himno_url TEXT,
    himno_letra TEXT,
    actualizado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE grados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL UNIQUE, -- ej: "11-1", "10-2"
    nivel INTEGER NOT NULL              -- ej: 11, 10
);

CREATE TABLE estudiantes (
    id SERIAL PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    grado_id INTEGER REFERENCES grados(id) ON DELETE SET NULL,
    foto_url VARCHAR(255),
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE noticias (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    contenido TEXT,
    fecha DATE NOT NULL,
    imagen_url VARCHAR(255),
    creado_por INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE eventos (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    fecha DATE NOT NULL,
    imagen_url VARCHAR(255),
    creado_por INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE deportes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE -- ej: "Futbol", "Voleibol", "Baloncesto"
);

CREATE TABLE equipos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    deporte_id INTEGER NOT NULL REFERENCES deportes(id) ON DELETE CASCADE,
    categoria VARCHAR(50),   -- ej: "Sub-15", "Mayores"
    entrenador VARCHAR(100),
    foto_url VARCHAR(255),
    descripcion TEXT
);

-- Relacion N:M entre estudiantes y equipos
CREATE TABLE integrantes_equipo (
    id SERIAL PRIMARY KEY,
    equipo_id INTEGER NOT NULL REFERENCES equipos(id) ON DELETE CASCADE,
    estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    UNIQUE (equipo_id, estudiante_id)
);

CREATE TABLE campeonatos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL, -- ej: "Intercursos 2026-1"
    deporte_id INTEGER NOT NULL REFERENCES deportes(id) ON DELETE CASCADE,
    fecha_inicio DATE,
    fecha_fin DATE,
    descripcion TEXT
);

-- Relacion N:M entre campeonatos y equipos, con resultado del enfrentamiento
CREATE TABLE resultados (
    id SERIAL PRIMARY KEY,
    campeonato_id INTEGER NOT NULL REFERENCES campeonatos(id) ON DELETE CASCADE,
    equipo_local_id INTEGER NOT NULL REFERENCES equipos(id) ON DELETE CASCADE,
    equipo_visitante_id INTEGER NOT NULL REFERENCES equipos(id) ON DELETE CASCADE,
    marcador_local INTEGER NOT NULL DEFAULT 0,
    marcador_visitante INTEGER NOT NULL DEFAULT 0,
    fecha DATE NOT NULL
);

CREATE TABLE mejores_puestos (
    id SERIAL PRIMARY KEY,
    estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    grado_id INTEGER NOT NULL REFERENCES grados(id) ON DELETE CASCADE,
    periodo VARCHAR(20) NOT NULL, -- ej: "2026-1"
    puesto INTEGER NOT NULL,      -- 1, 2, 3
    promedio NUMERIC(4,2),
    UNIQUE (grado_id, periodo, puesto)
);

CREATE TABLE galeria_fotos (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(150),
    url VARCHAR(255) NOT NULL,
    evento_id INTEGER REFERENCES eventos(id) ON DELETE SET NULL,
    noticia_id INTEGER REFERENCES noticias(id) ON DELETE SET NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE mensajes_contacto (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    mensaje TEXT NOT NULL,
    leido BOOLEAN NOT NULL DEFAULT FALSE,
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Datos de ejemplo minimos para poder ver la pagina funcionando
INSERT INTO grados (nombre, nivel) VALUES
    ('6-A', 6), ('6-B', 6),
    ('7-A', 7), ('7-B', 7),
    ('8-A', 8), ('8-B', 8),
    ('9-A', 9), ('9-B', 9),
    ('10-A', 10), ('10-B', 10),
    ('11-A', 11), ('11-B', 11);

INSERT INTO deportes (nombre) VALUES
    ('Futbol'), ('Voleibol'), ('Baloncesto'), ('Bádminton');

INSERT INTO institucion_info (historia, mision, vision, principios, valores, ubicacion) VALUES (
    'La Institución Educativa Distrital Técnica para el Desarrollo del Talento Humano fue creada para brindar formación académica y técnica a la comunidad, en convenio con el SENA.',
    'Formar personas integras, competentes y con proyección técnica, comprometidas con el desarrollo de su comunidad.',
    'Ser reconocida como una institución líder en formación técnica y humana en la región.',
    'Formación integral, mejoramiento continuo y compromiso con la comunidad educativa.',
    'Respeto, responsabilidad, honestidad, trabajo en equipo y sentido de pertenencia.',
    'Colombia'
);
