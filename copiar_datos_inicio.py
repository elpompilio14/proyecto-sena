"""Copia los profesores (comunidad educativa), los deportes y los deportistas
de un computador a otro SIN borrar nada de lo que ya tenga el otro computador.

Uso (dentro de la carpeta del proyecto):

  1) En el computador que SI tiene los datos (PC1):
         python copiar_datos_inicio.py exportar
     -> crea el archivo datos_inicio.json en esta misma carpeta.

  2) Copia datos_inicio.json a la carpeta del proyecto del otro computador
     y alli ejecuta:
         python copiar_datos_inicio.py importar

Las fotos (static/images) se copian aparte; al final el script avisa si falta alguna.
"""
import json
import os
import sys

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(CARPETA, 'datos_inicio.json')
load_dotenv(os.path.join(CARPETA, '.env'))

# tabla -> (columnas que identifican la fila, columnas con FK que se traducen por nombre)
TABLAS = {
    'deportes': (['nombre'], {}),
    'comunidad_educativa': (['nombre', 'categoria'], {}),
    'deportistas': (['nombre', 'deporte_nombre'], {'deporte_id': 'deportes', 'grado_id': 'grados'}),
    'equipos': (['nombre', 'deporte_nombre', 'categoria'], {'deporte_id': 'deportes'}),
}
IGNORAR = {'id', 'creado_en'}


def conectar():
    return psycopg.connect(
        host=os.environ.get('PGHOST'), port=os.environ.get('PGPORT'),
        user=os.environ.get('PGUSER'), password=os.environ.get('PGPASSWORD'),
        dbname=os.environ.get('PGDATABASE'), row_factory=dict_row,
    )


def columnas(cur, tabla):
    cur.execute(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_schema = 'public' AND table_name = %s", (tabla,))
    return {f['column_name'] for f in cur.fetchall()}


def exportar():
    datos = {}
    with conectar() as con, con.cursor() as cur:
        cur.execute('SELECT * FROM grados ORDER BY id')
        datos['grados'] = [{'nombre': g['nombre'], 'nivel': g['nivel']} for g in cur.fetchall()]
        for tabla, (_, fks) in TABLAS.items():
            if not columnas(cur, tabla):
                print(f'  {tabla}: no existe, se omite')
                continue
            cur.execute(f'SELECT * FROM {tabla} ORDER BY id')
            filas = []
            for fila in cur.fetchall():
                for col, ref in fks.items():
                    ref_id = fila.get(col)
                    nombre = None
                    if ref_id is not None:
                        cur.execute(f'SELECT nombre FROM {ref} WHERE id = %s', (ref_id,))
                        r = cur.fetchone()
                        nombre = r['nombre'] if r else None
                    fila[ref[:-1] + '_nombre' if ref != 'grados' else 'grado_nombre'] = nombre
                    fila.pop(col, None)
                filas.append({k: v for k, v in fila.items() if k not in IGNORAR})
            datos[tabla] = filas
            print(f'  {tabla}: {len(filas)} filas')
    with open(ARCHIVO, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=1, default=str)
    print('\nLISTO. Se creo:', ARCHIVO)
    print('Copia ese archivo a la carpeta del proyecto del otro computador.')


def importar():
    if not os.path.exists(ARCHIVO):
        print('No encuentro', ARCHIVO)
        print('Pon el archivo datos_inicio.json en la misma carpeta que este script.')
        sys.exit(1)
    with open(ARCHIVO, encoding='utf-8') as f:
        datos = json.load(f)

    fotos = set()
    with conectar() as con, con.cursor() as cur:
        # 1) grados que falten (para los deportistas)
        for g in datos.get('grados', []):
            cur.execute('INSERT INTO grados (nombre, nivel) VALUES (%s, %s) '
                        'ON CONFLICT (nombre) DO NOTHING', (g['nombre'], g['nivel']))

        for tabla, (claves, fks) in TABLAS.items():
            filas = datos.get(tabla)
            cols_destino = columnas(cur, tabla)
            if filas is None or not cols_destino:
                continue
            nuevas = actualizadas = 0
            for fila in filas:
                fila = dict(fila)
                # traducir nombres -> ids de ESTE computador
                ok = True
                for col, ref in fks.items():
                    clave_nombre = 'grado_nombre' if ref == 'grados' else ref[:-1] + '_nombre'
                    nombre = fila.get(clave_nombre)
                    ref_id = None
                    if nombre is not None:
                        cur.execute(f'SELECT id FROM {ref} WHERE nombre = %s', (nombre,))
                        r = cur.fetchone()
                        ref_id = r['id'] if r else None
                    if ref_id is None and col == 'deporte_id':
                        ok = False
                    fila[col] = ref_id
                if not ok:
                    continue
                for k in ('imagen_url', 'foto_url'):
                    if fila.get(k):
                        fotos.add(fila[k])

                datos_fila = {k: v for k, v in fila.items() if k in cols_destino and k not in IGNORAR}
                # condicion para saber si ya existe
                cond, valores = [], []
                for c in claves:
                    real = 'deporte_id' if c == 'deporte_nombre' else c
                    if datos_fila.get(real) is None:
                        cond.append(f'{real} IS NULL')
                    else:
                        cond.append(f'{real} = %s')
                        valores.append(datos_fila[real])
                cur.execute(f'SELECT id FROM {tabla} WHERE {" AND ".join(cond)} LIMIT 1', valores)
                existente = cur.fetchone()
                cols = list(datos_fila)
                if existente:
                    sets = ', '.join(f'{c} = %s' for c in cols)
                    cur.execute(f'UPDATE {tabla} SET {sets} WHERE id = %s',
                                [datos_fila[c] for c in cols] + [existente['id']])
                    actualizadas += 1
                else:
                    cur.execute(f'INSERT INTO {tabla} ({", ".join(cols)}) '
                                f'VALUES ({", ".join(["%s"] * len(cols))})',
                                [datos_fila[c] for c in cols])
                    nuevas += 1
            print(f'  {tabla}: {nuevas} nuevas, {actualizadas} actualizadas')
        con.commit()

    faltan = []
    for url in sorted(fotos):
        if url.startswith('/images/'):
            ruta = os.path.join(CARPETA, 'static', url.lstrip('/').replace('/', os.sep))
            if not os.path.exists(ruta):
                faltan.append(url)
    print('\nLISTO. Recarga la pagina (F5).')
    if faltan:
        print(f'\nOJO: faltan {len(faltan)} fotos en static\\images (copialas desde el PC1):')
        for u in faltan:
            print('  ', u)
    else:
        print('Todas las fotos estan en static\\images.')


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else ''
    if modo == 'exportar':
        exportar()
    elif modo == 'importar':
        importar()
    else:
        print(__doc__)
