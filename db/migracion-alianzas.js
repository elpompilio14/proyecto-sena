// Migracion puntual: crea la tabla de alianzas/convenios del colegio.
require('dotenv').config();
const pool = require('../src/config/db');

async function migrar() {
    await pool.query(`
        CREATE TABLE IF NOT EXISTS alianzas (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(150) NOT NULL,
            logo_url TEXT,
            link_url TEXT,
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
