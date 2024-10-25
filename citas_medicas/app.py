from flask import Flask, request, jsonify, render_template, redirect, url_for
# Importa las clases y funciones necesarias de Flask:
# - Flask: Clase principal para crear la aplicación web.
# - request: Objeto que maneja las solicitudes HTTP recibidas por la aplicación.
# - jsonify: Función para convertir datos en formato JSON y devolverlos en una respuesta HTTP.
# - render_template: Función para renderizar archivos de plantilla HTML.
# - redirect: Función para redirigir al usuario a una URL diferente.
# - url_for: Función para construir URLs basadas en el nombre de una función de vista.

import json
# Importa el módulo json, que proporciona funciones para trabajar con datos en formato JSON.
# Utilizado para leer y escribir archivos JSON que almacenan los datos de la aplicación.

import os
# Importa el módulo os, que proporciona una forma de interactuar con el sistema operativo.
# Se utiliza para manejar rutas de archivos y verificar la existencia de archivos en el sistema.


app = Flask(__name__)  # Crea una instancia de la aplicación Flask.

# Archivos JSON para almacenar datos
PACIENTES_FILE = os.path.join('models', 'pacientes.json')  # Ruta del archivo JSON para almacenar pacientes.
CITAS_FILE = os.path.join('models', 'citas.json')  # Ruta del archivo JSON para almacenar citas.

# Funciones para verificar y crear archivos JSON si no existen
def inicializar_archivo(archivo):
    if not os.path.exists(archivo):  # Verifica si el archivo no existe.
        with open(archivo, 'w') as f:  # Crea el archivo si no existe.
            json.dump([], f)  # Inicializa el archivo con una lista vacía en formato JSON.

# Funciones para leer y escribir en los archivos JSON
def leer_json(archivo):
    with open(archivo, 'r') as f:  # Abre el archivo en modo lectura.
        try:
            return json.load(f)  # Intenta cargar los datos JSON del archivo.
        except json.JSONDecodeError:
            return []  # Retorna una lista vacía si ocurre un error al decodificar JSON.

def escribir_json(archivo, data):
    with open(archivo, 'w') as f:  # Abre el archivo en modo escritura.
        json.dump(data, f, indent=4)  # Guarda los datos JSON en el archivo con indentación para legibilidad.

# Inicializamos los archivos al iniciar la aplicación
inicializar_archivo(PACIENTES_FILE)  # Inicializa el archivo de pacientes.
inicializar_archivo(CITAS_FILE)  # Inicializa el archivo de citas.

# ---- Rutas para la Interfaz Web ----

@app.route('/')
def index():
    return render_template('index.html')  # Renderiza la plantilla 'index.html' para la ruta raíz.

# ---- Rutas Web para Pacientes ----
@app.route('/pacientes', methods=['GET', 'POST'])
def pacientes_web():
    if request.method == 'POST':  # Si la solicitud es POST, se crea un nuevo paciente.
        pacientes = leer_json(PACIENTES_FILE)  # Lee la lista de pacientes del archivo JSON.
        nombre = request.form.get('nombre')  # Obtiene el nombre del formulario.
        edad = request.form.get('edad')  # Obtiene la edad del formulario.
        telefono = request.form.get('telefono')  # Obtiene el teléfono del formulario.
        email = request.form.get('email')
        direccion = request.form.get('direccion')
        

        nuevo_paciente = {
            'id': len(pacientes) + 1,  # Asigna un nuevo ID al paciente.
            'nombre': nombre,
            'edad': int(edad),  # Convierte la edad a entero.
            'telefono': telefono,
            'email': email,
            'direccion': direccion
            
        }
        pacientes.append(nuevo_paciente)  # Agrega el nuevo paciente a la lista.
        escribir_json(PACIENTES_FILE, pacientes)  # Guarda la lista actualizada en el archivo JSON.
        return redirect(url_for('pacientes_web'))  # Redirige a la página de pacientes.

    # Método GET: mostrar la lista de pacientes
    pacientes = leer_json(PACIENTES_FILE)  # Lee la lista de pacientes del archivo JSON.
    return render_template('pacientes.html', pacientes=pacientes)  # Renderiza la plantilla 'pacientes.html' con la lista de pacientes.

@app.route('/pacientes/eliminar/<int:id>', methods=['POST'])
def eliminar_paciente_web(id):
    pacientes = leer_json(PACIENTES_FILE)  # Lee la lista de pacientes del archivo JSON.
    citas = leer_json(CITAS_FILE)  # Lee la lista de citas del archivo JSON.

    # Verificar si el paciente tiene citas asociadas
    tiene_citas = any(cita['paciente_id'] == id for cita in citas)  # Verifica si el paciente tiene citas asociadas.

    if tiene_citas:
        # Si tiene citas asociadas, redirigir con un mensaje de error
        return redirect(url_for('pacientes_web', mensaje='No se puede eliminar el paciente porque tiene citas asociadas'))

    # Si no tiene citas, proceder a eliminar el paciente
    pacientes_filtrados = [p for p in pacientes if p['id'] != id]  # Filtra la lista de pacientes para excluir al paciente con el ID dado.
    escribir_json(PACIENTES_FILE, pacientes_filtrados)  # Guarda la lista actualizada en el archivo JSON.
    return redirect(url_for('pacientes_web'))  # Redirige a la página de pacientes.

# ---- Rutas Web para Citas Médicas ----
@app.route('/citas', methods=['GET', 'POST'])
def citas_web():
    if request.method == 'POST':  # Si la solicitud es POST, se crea una nueva cita.
        citas = leer_json(CITAS_FILE)  # Lee la lista de citas del archivo JSON.
        paciente_id = request.form.get('paciente_id')  # Obtiene el ID del paciente del formulario.
        fecha = request.form.get('fecha')  # Obtiene la fecha de la cita del formulario.
        hora = request.form.get('hora')  # Obtiene la hora de la cita del formulario.
        motivo = request.form.get('motivo')  # Obtiene el motivo de la cita del formulario.
        acompa = request.form.get('acompa')
        obser = request.form.get('obser')

        nueva_cita = {
            'id': len(citas) + 1,  # Asigna un nuevo ID a la cita.
            'paciente_id': int(paciente_id),  # Convierte el ID del paciente a entero.
            'fecha': fecha,
            'hora': hora,
            'motivo': motivo,
            'acompa': acompa,
            'obser':obser
        }
        citas.append(nueva_cita)  # Agrega la nueva cita a la lista.
        escribir_json(CITAS_FILE, citas)  # Guarda la lista actualizada en el archivo JSON.
        return redirect(url_for('citas_web'))  # Redirige a la página de citas.

    # Método GET: mostrar la lista de citas
    citas = leer_json(CITAS_FILE)  # Lee la lista de citas del archivo JSON.
    pacientes = leer_json(PACIENTES_FILE)  # Lee la lista de pacientes del archivo JSON.
    return render_template('citas.html', citas=citas, pacientes=pacientes)  # Renderiza la plantilla 'citas.html' con la lista de citas y pacientes.

@app.route('/citas/eliminar/<int:id>', methods=['POST'])
def eliminar_cita_web(id):
    citas = leer_json(CITAS_FILE)  # Lee la lista de citas del archivo JSON.
    citas_filtradas = [c for c in citas if c['id'] != id]  # Filtra la lista de citas para excluir la cita con el ID dado.
    escribir_json(CITAS_FILE, citas_filtradas)  # Guarda la lista actualizada en el archivo JSON.
    return redirect(url_for('citas_web'))  # Redirige a la página de citas.

# ---- Rutas API RESTful ----
# Todas las rutas API estarán prefijadas con /api

# ----- API Pacientes -----
@app.route('/api/pacientes', methods=['GET'])
def api_obtener_pacientes():
    pacientes = leer_json(PACIENTES_FILE)  # Lee la lista de pacientes del archivo JSON.
    return jsonify(pacientes), 200  # Retorna la lista de pacientes en formato JSON con código de estado 200 (OK).

@app.route('/api/pacientes', methods=['POST'])
def api_crear_paciente():
    if not request.is_json:
        return jsonify({'error': 'Content-Type debe ser application/json'}), 415  # Retorna error si el contenido no es JSON.

    datos = request.get_json()  # Obtiene los datos JSON de la solicitud.
    pacientes = leer_json(PACIENTES_FILE)  # Lee la lista de pacientes del archivo JSON.

    nuevo_paciente = {
        'id': len(pacientes) + 1,  # Asigna un nuevo ID al paciente.
        'nombre': datos.get('nombre'),
        'edad': datos.get('edad'),
        'telefono': datos.get('telefono'),
        'email': datos.get('email'),
        'direccion': datos.get('direccion')
    }
    pacientes.append(nuevo_paciente)  # Agrega el nuevo paciente a la lista.
    escribir_json(PACIENTES_FILE, pacientes)  # Guarda la lista actualizada en el archivo JSON.
    return jsonify(nuevo_paciente), 201  # Retorna el nuevo paciente en formato JSON con código de estado 201 (Creado).

@app.route('/api/pacientes/<int:id>', methods=['PUT'])
def api_actualizar_paciente(id):
    if not request.is_json:
        return jsonify({'error': 'Content-Type debe ser application/json'}), 415  # Retorna error si el contenido no es JSON.

    datos = request.get_json()  # Obtiene los datos JSON de la solicitud.
    pacientes = leer_json(PACIENTES_FILE)  # Lee la lista de pacientes del archivo JSON.

    for paciente in pacientes:
        if paciente['id'] == id:  # Busca al paciente con el ID dado.
            paciente['nombre'] = datos.get('nombre', paciente['nombre'])
            paciente['edad'] = datos.get('edad', paciente['edad'])
            paciente['telefono'] = datos.get('telefono', paciente['telefono'])
            paciente['email'] = datos.get('email', paciente['email'])
            paciente['direccion'] = datos.get('direccion', paciente['direccion'])
            
            escribir_json(PACIENTES_FILE, pacientes)  # Guarda la lista actualizada en el archivo JSON.
            return jsonify(paciente), 200  # Retorna el paciente actualizado en formato JSON con código de estado 200 (OK).

    return jsonify({'error': 'Paciente no encontrado'}), 404  # Retorna error si el paciente no se encuentra.

@app.route('/api/pacientes/<int:id>', methods=['DELETE'])
def api_eliminar_paciente(id):
    pacientes = leer_json(PACIENTES_FILE)  # Lee la lista de pacientes del archivo JSON.
    pacientes_filtrados = [p for p in pacientes if p['id'] != id]  # Filtra la lista para excluir al paciente con el ID dado.

    if len(pacientes_filtrados) == len(pacientes):
        return jsonify({'error': 'Paciente no encontrado'}), 404  # Retorna error si el paciente no se encuentra.

    escribir_json(PACIENTES_FILE, pacientes_filtrados)  # Guarda la lista actualizada en el archivo JSON.
    return jsonify({'mensaje': 'Paciente eliminado exitosamente'}), 200  # Retorna mensaje de éxito con código de estado 200 (OK).

# ----- API Citas -----
@app.route('/api/citas', methods=['GET'])
def api_obtener_citas():
    citas = leer_json(CITAS_FILE)  # Lee la lista de citas del archivo JSON.
    return jsonify(citas), 200  # Retorna la lista de citas en formato JSON con código de estado 200 (OK).

@app.route('/api/citas', methods=['POST'])
def api_crear_cita():
    if not request.is_json:
        return jsonify({'error': 'Content-Type debe ser application/json'}), 415  # Retorna error si el contenido no es JSON.

    datos = request.get_json()  # Obtiene los datos JSON de la solicitud.
    citas = leer_json(CITAS_FILE)  # Lee la lista de citas del archivo JSON.

    nueva_cita = {
        'id': len(citas) + 1,  # Asigna un nuevo ID a la cita.
        'paciente_id': datos.get('paciente_id'),
        'fecha': datos.get('fecha'),
        'hora': datos.get('hora'),
        'motivo': datos.get('motivo'),
        'acompa': datos.get('acompa'),
        'obser':datos.get('obser')
    }
    citas.append(nueva_cita)  # Agrega la nueva cita a la lista.
    escribir_json(CITAS_FILE, citas)  # Guarda la lista actualizada en el archivo JSON.
    return jsonify(nueva_cita), 201  # Retorna la nueva cita en formato JSON con código de estado 201 (Creado).

@app.route('/api/citas/<int:id>', methods=['PUT'])
def api_actualizar_cita(id):
    if not request.is_json:
        return jsonify({'error': 'Content-Type debe ser application/json'}), 415  # Retorna error si el contenido no es JSON.

    datos = request.get_json()  # Obtiene los datos JSON de la solicitud.
    citas = leer_json(CITAS_FILE)  # Lee la lista de citas del archivo JSON.

    for cita in citas:
        if cita['id'] == id:  # Busca la cita con el ID dado.
            cita['paciente_id'] = datos.get('paciente_id', cita['paciente_id'])
            cita['fecha'] = datos.get('fecha', cita['fecha'])
            cita['hora'] = datos.get('hora', cita['hora'])
            cita['motivo'] = datos.get('motivo', cita['motivo'])
            cita['acompa'] = datos.get('acompa', cita['acompa'])
            cita['obser'] = datos.get('obser', cita['obser'])
            
            escribir_json(CITAS_FILE, citas)  # Guarda la lista actualizada en el archivo JSON.
            return jsonify(cita), 200  # Retorna la cita actualizada en formato JSON con código de estado 200 (OK).

    return jsonify({'error': 'Cita no encontrada'}), 404  # Retorna error si la cita no se encuentra.

@app.route('/api/citas/<int:id>', methods=['DELETE'])
def api_eliminar_cita(id):
    citas = leer_json(CITAS_FILE)  # Lee la lista de citas del archivo JSON.
    citas_filtradas = [c for c in citas if c['id'] != id]  # Filtra la lista para excluir la cita con el ID dado.

    if len(citas_filtradas) == len(citas):
        return jsonify({'error': 'Cita no encontrada'}), 404  # Retorna error si la cita no se encuentra.

    escribir_json(CITAS_FILE, citas_filtradas)  # Guarda la lista actualizada en el archivo JSON.
    return jsonify({'mensaje': 'Cita eliminada exitosamente'}), 200  # Retorna mensaje de éxito con código de estado 200 (OK).

if __name__ == '__main__':
    app.run(debug=True)  # Ejecuta la aplicación Flask en modo de depuración.
