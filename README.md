# Página web del colegio — versión Python + Flask

Proyecto SENA — IED Técnica para el Desarrollo del Talento Humano.

Esta es la versión en **Python + Flask** de la página (antes estaba en Node.js).
El diseño (CSS, JS, imágenes) es exactamente el mismo — solo cambió lo que
corre "por detrás", en el servidor.

## Estructura del proyecto

```
app.py                 # arranca la aplicacion
db.py                  # conexion a PostgreSQL
mailer.py               # envio de correos (verificacion, recuperar contraseña)
uploads.py               # manejo de subida de archivos
decorators.py            # protege rutas que necesitan estar logueado / ser admin
requirements.txt         # librerias que necesita el proyecto

blueprints/               # rutas y logica (equivalente a controllers+routes)
    public.py             # inicio, noticias, eventos, etc.
    auth.py               # login, registro, Google, recuperar contraseña
    admin/                 # las 15 secciones del panel de administrador

utils/                    # funciones de apoyo (formatear texto, fechas, etc.)

templates/                # las paginas (.html), usando Jinja2
    base.html              # encabezado + pie de pagina (se repite en todas)
    admin/                 # plantillas del panel admin

static/                   # CSS, JS e imagenes (identico al proyecto en Node)

db/schema.sql              # estructura de la base de datos (igual que antes)
```

## Cómo correrlo en tu computador

### 1. Instala Python
Si no lo tienes, descárgalo de [python.org](https://www.python.org/downloads/) (marca la opción "Add Python to PATH" al instalar).

### 2. Crea y activa el entorno virtual (venv)
El venv guarda las librerías de este proyecto separadas del resto de tu computador.

```bash
python -m venv venv
```

Actívalo:
- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **Windows (Git Bash):** `source venv/Scripts/activate`

Vas a ver que el nombre `(venv)` aparece al inicio de tu terminal cuando está activo.

### 3. Instala las librerías
```bash
pip install -r requirements.txt
```

### 4. Configura las variables de entorno
Copia `.env.example` a un archivo nuevo llamado `.env`, y completa tus datos reales
(usuario/contraseña de PostgreSQL, credenciales de Gmail y de Google que ya tenías
configuradas en la versión de Node — son las mismas).

### 5. Crea la base de datos (si aún no existe)
```bash
psql -U postgres -c "CREATE DATABASE colegio_web"
psql -U postgres -d colegio_web -f db/schema.sql
```
*(Si ya tienes la base de datos de la versión en Node con toda tu información, no hace
falta este paso — este proyecto usa exactamente la misma base de datos.)*

### 6. Corre el servidor
```bash
python app.py
```

Abre tu navegador en **http://localhost:5000** (o el puerto que hayas puesto en `PORT`
dentro de tu `.env`).

## Notas

- La base de datos es la misma que usaba la versión en Node — no se pierde nada de lo
  que ya habías cargado (noticias, eventos, fotos, usuarios, contraseñas, etc.).
- Las contraseñas de los usuarios siguen funcionando igual (ambas versiones usan el
  mismo algoritmo, bcrypt).
- Para el login con Google, la URL de redirección (`GOOGLE_CALLBACK_URL`) debe coincidir
  con la que tengas registrada en [Google Cloud Console](https://console.cloud.google.com/).
  Si vas a correr esta versión en un puerto distinto a 3000, agrega esa URL nueva como
  "URI de redireccionamiento autorizado" en tu proyecto de Google Cloud.
