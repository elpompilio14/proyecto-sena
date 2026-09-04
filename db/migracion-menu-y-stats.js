// Migracion puntual: agrega columnas nuevas a institucion_info y crea icfes_resultados
// sin borrar nada de lo que ya existe. Se ejecuta una sola vez.
require('dotenv').config();
const pool = require('../src/config/db');

async function migrar() {
    await pool.query(`
        ALTER TABLE institucion_info
            ADD COLUMN IF NOT EXISTS logo_url TEXT,
            ADD COLUMN IF NOT EXISTS anios_fundacion INTEGER,
            ADD COLUMN IF NOT EXISTS num_estudiantes INTEGER,
            ADD COLUMN IF NOT EXISTS num_profesores INTEGER,
            ADD COLUMN IF NOT EXISTS whatsapp_numero TEXT,
            ADD COLUMN IF NOT EXISTS instagram_url TEXT,
            ADD COLUMN IF NOT EXISTS instagram_imagen_url TEXT,
            ADD COLUMN IF NOT EXISTS facebook_url TEXT,
            ADD COLUMN IF NOT EXISTS facebook_imagen_url TEXT
    `);

    await pool.query(`
        ALTER TABLE mensajes_contacto
            ADD COLUMN IF NOT EXISTS apellido VARCHAR(100)
    `);

    await pool.query(`
        CREATE TABLE IF NOT EXISTS icfes_resultados (
            id SERIAL PRIMARY KEY,
            estudiante_nombre VARCHAR(150) NOT NULL,
            puntaje INTEGER NOT NULL,
            anio INTEGER NOT NULL,
            foto_url TEXT,
            descripcion TEXT,
            creado_en TIMESTAMP NOT NULL DEFAULT NOW()
        )
    `);

    console.log('Migracion aplicada correctamente.');
    await pool.end();
}

migrar().catch((err) => {
    console.error('Error en la migracion:', err);
    process.exit(1);
});
