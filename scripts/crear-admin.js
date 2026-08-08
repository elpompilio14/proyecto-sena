// Uso: node scripts/crear-admin.js "Nombre Admin" correo@colegio.edu.co miPassword123
require('dotenv').config();
const bcrypt = require('bcryptjs');
const pool = require('../src/config/db');

async function main() {
    const [nombre, email, password] = process.argv.slice(2);

    if (!nombre || !email || !password) {
        console.log('Uso: node scripts/crear-admin.js "Nombre Admin" correo@colegio.edu.co miPassword123');
        process.exit(1);
    }

    const password_hash = await bcrypt.hash(password, 10);

    await pool.query(
        `INSERT INTO usuarios (nombre, email, password_hash, rol)
         VALUES ($1, $2, $3, 'admin')
         ON CONFLICT (email) DO UPDATE SET password_hash = EXCLUDED.password_hash, rol = 'admin'`,
        [nombre, email, password_hash]
    );

    console.log(`Usuario admin creado/actualizado: ${email}`);
    await pool.end();
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});
