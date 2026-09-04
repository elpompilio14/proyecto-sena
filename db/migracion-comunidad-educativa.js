// Migracion puntual: agrega columnas para clasificar y enriquecer comunidad_educativa
// (rectoria/coordinacion/docente, area para filtros, materia, anios de experiencia, bio).
require('dotenv').config();
const pool = require('../src/config/db');

async function migrar() {
    await pool.query(`
        ALTER TABLE comunidad_educativa
            ADD COLUMN IF NOT EXISTS categoria VARCHAR(20) NOT NULL DEFAULT 'docente',
            ADD COLUMN IF NOT EXISTS area VARCHAR(50),
            ADD COLUMN IF NOT EXISTS materia VARCHAR(100),
            ADD COLUMN IF NOT EXISTS anios_experiencia INTEGER,
            ADD COLUMN IF NOT EXISTS descripcion TEXT
    `);

    console.log('Migracion aplicada correctamente.');
    await pool.end();
}

migrar().catch((err) => {
    console.error('Error en la migracion:', err);
    process.exit(1);
});
