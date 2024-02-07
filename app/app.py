import calendar
import locale
from datetime import datetime, timedelta
from MySQLdb import Date
from flask import Flask, g, Blueprint, render_template, redirect, send_file, url_for, request, flash, jsonify, send_from_directory, session, Response
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from datetime import datetime
import os  # Nos permite guardar donde queramos el archivo
from flask_bcrypt import Bcrypt  # para encriptar contra
from reportlab.pdfgen import canvas
import json
import tempfile
from routes.clientes import client_routes
from routes.admin import admin_routes


app = Flask(__name__)
app.register_blueprint(client_routes, url_prefix='/clientes')
app.register_blueprint(admin_routes, url_prefix='/admin')

app.config["UPLOAD_FOLDER"] = "app/static/empleados"  # especifica la ruta
EXTENCIONES_PERMITIDAS = set(
    ['png', 'jpg', 'jpeg', 'gif', 'pdf'])  # como el nombre lo dice

bcrypt = Bcrypt(app)  # Asegúrate de que 'app' sea tu instancia de Flask




def extensiones(file):
    file = file.split('.')
    if file[1] in EXTENCIONES_PERMITIDAS:
        return True

    return False


# conexion a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'astil'

conexion = MySQL(app)


# Configurar una conexion global para los blueprints
@app.before_request
def before_request():
    g.conexion = conexion.connection
    g.bcrypt = bcrypt
# servicios este es para que funcione el flashed
app.secret_key = 'mysecretkey'
 
# ruta principal

# templates = Jinja2Templates(directory="templates")
app.template_folder = 'templates'


@app.route('/')
def index():
    return render_template("index.html")

# si no encuentra pagina redirege a la parte principal


def pagina_no_encontrada(error):
    # return render_template('404.html'),404
    # en caso que no queremos que nos mande a ese render
    # y queremos que nos devuelva directamente a la pagina
    # index ponemos entonces
    return redirect(url_for('index'))





# nos dirigira a la pagina que seleccionamos , acceso a empleado
@app.route('/empleados')
def empleados():
    return render_template("empleados.html")

# Aca se hace la validacion de inicio de sesion de el admin

# Para cerrar sesion


@app.route('/cerrar_sesion')
def cerrar_sesion():
    # Elimina la información de la sesión al cerrar sesión
    # 'usuario' es el nombre de la clave que almacena la información del usuario
    session.pop('usuario', None)
    # Usar código 303 para indicar "See Other"
    return redirect(url_for('index'), code=303)

# Fin parte cerrar sesion

# Aca se hace la validacion de inicio de sesion de el empleado
@app.route('/empleados/inicio', methods=['POST'])
def login_empleados():
    usuario = request.form.get('Usuario')
    contra = request.form.get('Contrasena')
   
    cursor = conexion.connection.cursor()
    sql = "SELECT * FROM usuarios WHERE usuario=%s AND tipo_usuario=%s"
    valores = (usuario, 3)
    cursor.execute(sql, valores)
    datos = cursor.fetchall()
    numero_filas = len(datos)

    if numero_filas > 0:
        for dato in datos:
            contrasena_hash = dato[4]
            if bcrypt.check_password_hash(contrasena_hash, contra):
                cursor.close()
                return render_template('acceso_empleado.html')
        cursor.close()
        mensaje_alerta = "Usuario o contraseña incorrectos!"
        return redirect(url_for('empleados', mensaje_alerta=mensaje_alerta))
    else:
        cursor.close()
        mensaje_alerta = "Usuario no encontrado!"
        return redirect(url_for('empleados', mensaje_alerta=mensaje_alerta))


@app.route('/empleados', methods=['POST'])
def registro_empleados():
    cursor = conexion.connection.cursor()
    nombre_completo = request.form.get('nombre_completo')
    documento = request.form.get('documento')
    usuario = request.form.get('usuario')
    contrasena = request.form.get('contrasena')
    constrasena_hash = bcrypt.generate_password_hash(contrasena)
    print(constrasena_hash)
    tipoUsuario = request.form.get('tipo')
    con = 0

    if len(nombre_completo) > 0:
        con += 1
    if len(documento) > 0:
        con += 1
    if len(usuario) > 0:
        con += 1
    if len(contrasena) > 0:
        con += 1

    if (con == 4):
        query = "INSERT INTO usuarios(nombre_completo,documento,usuario,contrasena,tipo_usuario) VALUES (%s, %s, %s, %s, %s)"
        valores = (nombre_completo, documento,
                   usuario, constrasena_hash, tipoUsuario)
        cursor.execute(query, valores)
        conexion.connection.commit()
        cursor.close()
        return render_template('empleados.html')
    else:
        cursor.close()
        mensaje_alerta = "Complete todos los campos!"
        return redirect(url_for('empleados', mensaje_alerta=mensaje_alerta))

# Crud Gestion de empleados (cierre conexion)
#
@app.route('/agregar_empleado', methods=['POST'])
def agregarE():
    if request.method == 'POST':

        file = request.files["subir"]
        # Para obtener el nombre del archivo
        # La ruta donde se encuentra el archivo actual
        basepath = os.path.dirname(__file__)
        nombreArchivo = secure_filename(file.filename)
    # print(file ,file.filename)
        print(nombreArchivo)
        if extensiones(nombreArchivo):
            extension = os.path.splitext(nombreArchivo)[1]
            # nuevoNombreFile = (nombreArchivo + extension) #No hace falta agregar extension

            nuevoNombreFile = (nombreArchivo)
            print('Permitido!')
            upload_path = os.path.join(
                basepath, 'static/empleados', nuevoNombreFile)
            file.save(upload_path)
        #   #este codigo hace que se guarde la imagen en la configuracion que hicimos
            # file.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreArchivo))
        else:
            # Agregar parte de mensaje que el archivo es incorrecto
            print('No permitido')

        # Hata aqui parte imagen#

        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        documento = request.form.get('documento')
    #    contrato=request.form.get('contrato')
        pais = request.form.get('pais')  # Obtiene el valor del primer select
        puesto = request.form.get('puesto')
        cliente = request.form.get('cliente')
        estado = 1
        telefono = request.form.get('telefono')
        fecha_ingreso = request.form.get('ingreso')
        tipo_em = request.form.get('tip_em')
    #    print(nombre,apellido)
        cursor = conexion.connection.cursor()
        query = "INSERT INTO empleados(nombre_completo,apellido_completo,documento,contrato,idNacionalidad,idPuesto ,idEstado,telefono,id_cliente,id_tipo_empleado,Fecha_de_ingreso) VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)"
        valores = (nombre, apellido, documento, nombreArchivo,
                   pais, puesto, estado, telefono, cliente, tipo_em, fecha_ingreso)
        cursor.execute(query, valores)
        conexion.connection.commit()
        flash('Contacto Agregado!')

    #    return render_template('gestionEmpleados.html',data=nombreArchivo)
        return redirect(url_for('admin_routes.gestion_empleados'))

# Para editar empleados


@app.route('/edit/<id>')
def modificarE(id):
    cursor = conexion.connection.cursor()
    cursor.execute(f'SELECT * FROM empleados WHERE idEmpleados={id}')
    dato = cursor.fetchall()
    cursor.execute("""SELECT * FROM clientes """)
    data2 = cursor.fetchall()
    cursor.execute(f"""SELECT * FROM `nacionalidad`;""")
    nacionalidad = cursor.fetchall()  # Move this line here
    cursor.execute(f"""SELECT * FROM `puesto`;""")
    puestos = cursor.fetchall()  # Move this line here
    cursor.execute(f"""SELECT * FROM `tipo_empleado`;""")
    tipos = cursor.fetchall()
    return render_template('editar_empleado.html', dato=dato[0], datodos=data2, nacionalidades=nacionalidad, puestos=puestos, tipos=tipos)

# aca actualiza los empleados


@app.route('/actualizarE/<id>/<archivo_a_eliminar>', methods=['POST'])
def actualizar_empleados(id, archivo_a_eliminar):
    if request.method == 'POST':
        # Hacer un select de empleados y traer la url para que en el update no cargue vacio
        # porque estamos capturando el file y aveces no se cambia la imagen

        cursor = conexion.connection.cursor()
        cursor.execute(f'SELECT * FROM empleados WHERE idEmpleados={id}')
        dato = cursor.fetchall()
        contrato = ''
        file = request.files["subir"]

        # Verifica si se proporciona un nuevo archivo
        if file:
            # Elimina el archivo anterior solo si se proporciona un nuevo archivo
            os.remove(os.path.join(app.root_path, 'static',
                      'empleados', archivo_a_eliminar))

            # Obtén el nombre del nuevo archivo
            basepath = os.path.dirname(__file__)
            nombreArchivo = secure_filename(file.filename)

            if extensiones(nombreArchivo):
                contrato = nombreArchivo
                print('Permitido!')
                upload_path = os.path.join(
                    basepath, 'static/empleados', contrato)
                file.save(upload_path)
        else:
            # Si no se proporciona un nuevo archivo, conserva el nombre del archivo existente
            contrato = archivo_a_eliminar

        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        documento = request.form.get('documento')
        pais = request.form.get('pais')
        puesto = request.form.get('puesto')
        telefono = request.form.get('telefono')
        cliente = request.form.get('cliente')
        id_tipo = request.form.get('tip_em')
        fecha_ingreso = request.form.get('ingreso')
        estado = 1

        cursor.execute("""
            UPDATE empleados 
            SET nombre_completo=%s,
            apellido_completo=%s,
            documento=%s,
            contrato=%s,
            idNacionalidad=%s,
            idPuesto=%s,
            idEstado=%s,
            telefono=%s,
            id_cliente=%s,
            id_tipo_empleado=%s,
            Fecha_de_ingreso=%s
            WHERE idEmpleados=%s
            """, (nombre, apellido, documento, contrato, pais, puesto, estado, telefono, cliente, id_tipo, fecha_ingreso, id))
        conexion.connection.commit()
        flash('Contacto actualizado!')
        return redirect(url_for('admin_routes.gestion_empleados'))

# Para eliminar empleados


@app.route('/delet/<id>/<archivo_a_eliminar>')
def borrarE(id, archivo_a_eliminar):
    cursor = conexion.connection.cursor()
    cursor.execute(f'DELETE FROM empleados WHERE idEmpleados={id}')
    conexion.connection.commit()
    flash('Contacto Removido!')
    os.remove(os.path.join(app.root_path, 'static',
                           'empleados', archivo_a_eliminar))
    return redirect(url_for('admin_routes.gestion_empleados'))

@app.route('/agregar_Clientes', methods=['POST'])
def agregar_Clientes():
    if request.method == 'POST':
        file = request.files["subir"]
        # Para obtener el nombre del archivo
        # La ruta donde se encuentra el archivo actual
        basepath = os.path.dirname(__file__)
        nombreArchivo = secure_filename(file.filename)

        if extensiones(nombreArchivo):
            extension = os.path.splitext(nombreArchivo)[1]
            # nuevoNombreFile = (nombreArchivo + extension) #No hace falta agregar extension

            nuevoNombreFile = (nombreArchivo)
            print('Permitido!')
            upload_path = os.path.join(
                basepath, 'static/clientes', nuevoNombreFile)
            file.save(upload_path)
        # Parte imagen
        razon = request.form.get('razon')
        ruc = request.form.get('ruc')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        # contrato = request.form.get('contrato')
    #    print(nombre,apellido)
        cursor = conexion.connection.cursor()
        query = "INSERT INTO clientes(razon_social,ruc,email,contrato,telefono) VALUES (%s, %s, %s, %s,%s)"
        valores = (razon, ruc, email, nombreArchivo, telefono)
        cursor.execute(query, valores)
        # Tambien se le agrega a caja con monto 0
        query = "INSERT INTO caja(monto,ruc_cliente) VALUES (%s, %s)"
        valores = (0, ruc)
        cursor.execute(query, valores)
        conexion.connection.commit()
        flash('Contacto Agregado!')

        return redirect(url_for('admin_routes.gestion_clientes'))


# Para editar Clientes


@app.route('/editC/<id>')
def modificarC(id):
    cursor = conexion.connection.cursor()
    cursor.execute(f'SELECT * FROM clientes WHERE id_cliente={id}')
    dato = cursor.fetchall()
    return render_template('editar_cliente.html', dato=dato[0])


@app.route('/actualizarC/<id>/<archivo_a_eliminar>', methods=['POST'])
def actualizar_clientes(id, archivo_a_eliminar):
    if request.method == 'POST':
        cursor = conexion.connection.cursor()
        razon = request.form.get('razon')
        ruc = request.form.get('ruc')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        contrato = ''
        file = request.files["subir"]

        # Verifica si se proporciona un nuevo archivo
        if file:
            # Elimina el archivo anterior solo si se proporciona un nuevo archivo
            os.remove(os.path.join(app.root_path, 'static',
                      'clientes', archivo_a_eliminar))

            # Obtén el nombre del nuevo archivo
            basepath = os.path.dirname(__file__)
            nombreArchivo = secure_filename(file.filename)

            if extensiones(nombreArchivo):
                contrato = nombreArchivo
                print('Permitido!')
                upload_path = os.path.join(
                    basepath, 'static/clientes', contrato)
                file.save(upload_path)
        else:
            # Si no se proporciona un nuevo archivo, conserva el nombre del archivo existente
            contrato = archivo_a_eliminar

        cursor.execute("""
            UPDATE clientes 
            SET razon_social=%s,
            ruc=%s,
            email=%s,
            contrato=%s,
            telefono=%s
            WHERE id_cliente=%s
            """, (razon, ruc, email, contrato, telefono, id))
        conexion.connection.commit()
        flash('Contacto actualizado!')
        return redirect(url_for('admin_routes.gestion_clientes'))


# Para eliminar clientes


@app.route('/deletC/<id>/<archivo_a_eliminar>')
def borrarC(id, archivo_a_eliminar):
    cursor = conexion.connection.cursor()
    cursor.execute(f'DELETE FROM clientes WHERE id_cliente={id}')
    conexion.connection.commit()
    flash('Contacto Removido!')
    os.remove(os.path.join(app.root_path, 'static',
                           'clientes', archivo_a_eliminar))
    return redirect(url_for('admin_routes.gestion_clientes'))

# Ver empleados del cliente


@app.route('/verEmpleados/<id_c>')
def verEmpleados(id_c):
    cursor = conexion.connection.cursor()
    # Aca extraemos los datos que hay en la seccion de empleados
    cursor.execute(f"""
    SELECT e.idEmpleados,e.nombre_completo,e.apellido_completo,e.documento,e.contrato,n.Nacionalidad,p.Categoria,e.idEstado,e.telefono,c.razon_social	
    FROM `empleados` AS e INNER JOIN `nacionalidad` AS n ON e.idNacionalidad=n.idNacionalidad 
    INNER JOIN `puesto` AS p ON p.idPuesto=e.idPuesto INNER JOIN `clientes` as c ON e.id_cliente=c.id_cliente
    WHERE e.id_cliente={id_c};""")
    data = cursor.fetchall()

    cursor.execute(f"""SELECT * FROM clientes WHERE id_cliente={id_c}""")
    data2 = cursor.fetchall()
    cursor.execute(f"""SELECT * FROM `nacionalidad`;""")
    nacionalidad = cursor.fetchall()  # Move this line here
    cursor.execute(f"""SELECT * FROM `puesto`;""")
    puestos = cursor.fetchall()  # Move this line here

    return render_template('gestion_empleados.html', infos=data, dato=data2, nacionalidades=nacionalidad, puestos=puestos)
    # Fin Crud clientes



# La parte de filtrar hay que arreglar porque da error


@app.route('/filtrarAsistencias/<id_empleado>', methods=['POST'])
def filtrar_asistencias(id_empleado):
    # Obtenemos los datos del formulario
    selected_month = int(request.form.get('mes'))
    selected_year = int(request.form.get('ano'))

    cursor = conexion.connection.cursor()
    cursor.execute(f"""SELECT asis.dia,e.documento,e.nombre_completo,e.apellido_completo,asis.fecha,asis.primer_turno_E,asis.primer_turno_S,asis.segundo_turno_E,asis.segundo_turno_S,e.idEmpleados,asis.id_asistencia
    FROM `empleados` AS e INNER JOIN `asistencias` AS asis ON e.idEmpleados=asis.id_empleado
    WHERE e.idEmpleados={id_empleado}
    AND MONTH(asis.fecha) = {selected_month}
    AND YEAR(asis.fecha) = {selected_year};""")
    infos = cursor.fetchall()

    month_name = calendar.month_name
    if infos:
        return render_template('editar_asistencias.html', infos=infos, current_month=selected_month, current_year=selected_year,   month_name=month_name)
    else:
        return redirect(url_for('admin_routes.editar_Pasistencia', id=id_empleado))
# Borrar asistencia


@app.route('/borrarAsistencia/<int:id>/<id_asistencia>')
def borrarAsistencia(id, id_asistencia):
    cursor = conexion.connection.cursor()

    # Utiliza placeholders en la consulta SQL para evitar la inyección de SQL
    query = 'DELETE FROM asistencias WHERE id_empleado=%s AND id_asistencia=%s'
    cursor.execute(query, (id, id_asistencia))

    conexion.connection.commit()
    # flash('Asistencia Removida!')
    return redirect(url_for('admin_routes.editar_Pasistencia', id=id))


# Aca Ira cuando actualicemos asistencia
@app.route('/actualizarAsistencia/<int:id>', methods=['POST'])
def actualizarAsistencia(id):
    cursor = conexion.connection.cursor()

    # Obtenemos los datos nuevos o que no fueron tocados
    dia = request.form.get('dia')
    fecha = request.form.get('fecha')
    nuevoEntrada1 = request.form.get('entrada_primer_turno1')
    nuevoSalida1 = request.form.get('salida_primer_turno1')
    nuevoEntrada2 = request.form.get('entrada_segundo_turno2')
    nuevoSalida2 = request.form.get('salida_segundo_turno2')

    # Convierte las cadenas en objetos de tiempo
    entrada_manana = datetime.strptime(nuevoEntrada1, "%H:%M")
    salida_manana = datetime.strptime(nuevoSalida1, "%H:%M")
    entrada_tarde = datetime.strptime(nuevoEntrada2, "%H:%M")
    salida_tarde = datetime.strptime(nuevoSalida2, "%H:%M")

    # Calcula las diferencias de tiempo
    duracion_manana = salida_manana - entrada_manana
    duracion_tarde = salida_tarde - entrada_tarde

    # Suma las duraciones de ambos turnos para obtener el total de horas trabajadas en el día
    total_horas_trabajadas = duracion_manana + duracion_tarde

    # Obtenemos el asistencia_id del formulario
    asistencia_id = request.form.get('asistencia_id')
    print("Hola"+asistencia_id)
    # Actualizamos solo la asistencia que corresponde al asistencia_id
    cursor.execute("""
            UPDATE asistencias 
            SET dia=%s,
            fecha=%s,
            primer_turno_E=%s,
            primer_turno_S=%s,
            segundo_turno_E=%s,
            segundo_turno_S=%s,
            horas_tot_dia=%s
            WHERE id_empleado=%s AND id_asistencia=%s
            """, (dia, fecha, nuevoEntrada1, nuevoSalida1, nuevoEntrada2, nuevoSalida2, total_horas_trabajadas, id, asistencia_id))

    conexion.connection.commit()
    ano, mes, _ = fecha.split('-')

    # Convertir las partes a variables numéricas
    ano = int(ano)
    mes = int(mes)
    current_month = mes
    current_year = ano

    # Obtenemos el nombre de los meses
    month_name = calendar.month_name

    # lógica para obtener los datos del empleado
    cursor = conexion.connection.cursor()
    cursor.execute(f"""SELECT asis.dia,e.documento,e.nombre_completo,e.apellido_completo,asis.fecha,asis.primer_turno_E,asis.primer_turno_S,asis.segundo_turno_E,asis.segundo_turno_S,e.idEmpleados,asis.id_asistencia
    FROM `empleados` AS e INNER JOIN `asistencias` AS asis ON e.idEmpleados=asis.id_empleado
    WHERE e.idEmpleados={id}
    AND MONTH(asis.fecha) = {current_month}
    AND YEAR(asis.fecha) = {current_year};""")
    infos = cursor.fetchall()

    return render_template('editar_asistencias.html', infos=infos, current_month=current_month, current_year=current_year, month_name=month_name)


# Parte de la caja


@app.route('/caja')
def cargar_caja():
    cursor = conexion.connection.cursor()
    cursor.execute(f"""
        SELECT ci.id_cliente, ci.razon_social, ca.id_caja, ca.monto, ca.ruc_cliente
        FROM `clientes` AS ci INNER JOIN `caja` AS ca ON ca.ruc_cliente = ci.ruc;""")
    data = cursor.fetchall()
    return render_template('caja.html', datos=data)

# Actualizamos el monto porque solo una caja por cliente puede haber


@app.route('/caja/guardar/<ruc>/<id_caja>', methods=['POST'])
def guardar_caja(ruc, id_caja):  # Fix the parameter name
    cursor = conexion.connection.cursor()

    # Obtener el monto del formulario utilizando request.form
    monto = float(request.form.get('monto'))

    # Asegúrate de usar comillas simples alrededor del valor de ruc en la consulta SQL
    cursor.execute(f"""
        SELECT ci.id_cliente, ci.razon_social, ca.id_caja, ca.monto, ca.ruc_cliente
        FROM `clientes` AS ci INNER JOIN `caja` AS ca
        WHERE ca.ruc_cliente = '{ruc}';
    """)

    data = cursor.fetchall()  # Move this line here

    monto += float(data[0][3])

    cursor.execute("""
        UPDATE caja 
        SET monto=%s
        WHERE id_caja =%s
    """, (monto, id_caja))

    conexion.connection.commit()

    return redirect(url_for('cargar_caja'))

# Aca borraremos el monto en caso de que este mal algo


@app.route('/borrarCaja/<id>')
def borrarCaja(id):
    cursor = conexion.connection.cursor()
    cursor.execute("""
        UPDATE caja 
        SET monto=%s
        WHERE id_caja =%s
        """, (0, id))

    conexion.connection.commit()

    return redirect(url_for('cargar_caja'))
# Fin Parte de la caja

# Parte de archivos


@app.route('/archivos')
def archivos():
    return render_template('cargarArchivos.html')


@app.route('/registrar-archivo', methods=['GET', 'POST'])
def registarArchivo():
    if request.method == 'POST':

        # Script para archivo
        file = request.files['archivo']
        # La ruta donde se encuentra el archivo actual
        basepath = os.path.dirname(__file__)
        # Nombre original del archivo
        filename = secure_filename(file.filename)

        # capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
        extension = os.path.splitext(filename)[1]
        nuevoNombreFile = (filename + extension)

        upload_path = os.path.join(
            basepath, 'static/archivos', nuevoNombreFile)
        file.save(upload_path)
        flash('El Registro fue un Exito &#x270c;&#xfe0f;')
        return render_template('cargarArchivos.html')
    return render_template('cargarArchivos.html')


@app.route('/verArchivos')
def verArchivos():
    # Obtener la lista de archivos en la carpeta 'static/archivos'
    archivos = os.listdir(os.path.join(app.root_path, 'static', 'archivos'))

    # Obtener el término de búsqueda del parámetro de la URL
    searchTerm = request.args.get('search')

    # Filtrar archivos si hay un término de búsqueda
    if searchTerm:
        archivos = [archivo for archivo in archivos if searchTerm.lower()
                    in archivo.lower()]

    return render_template('verArchivos.html', files=archivos)
# Ruta para eliminar archivo


@app.route('/eliminar-archivo', methods=['POST'])
def eliminar_archivo():
    archivo_a_eliminar = request.form.get('archivo')

    # Asegúrate de manejar la lógica de eliminación aquí
    # Puedes utilizar os.remove para eliminar el archivo del sistema de archivos
    # Ten en cuenta que este es un ejemplo básico y debes implementar manejo de errores y seguridad adicional.
    print(archivo_a_eliminar)
    try:
        os.remove(os.path.join(app.root_path, 'static',
                  'archivos', archivo_a_eliminar))
        return jsonify({'mensaje': f'Archivo {archivo_a_eliminar} eliminado correctamente.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# Fin parte de archivos

# Parte Configuracion para cargar los Paises y Puestos


@app.route('/Configuracion')
def Configuracion():
    cursor = conexion.connection.cursor()
    # Asegúrate de usar comillas simples alrededor del valor de ruc en la consulta SQL
    cursor.execute(f"""SELECT * FROM `nacionalidad`;""")
    nacionalidad = cursor.fetchall()  # Move this line here
    cursor.execute(f"""SELECT * FROM `puesto`;""")
    puestos = cursor.fetchall()  # Move this line here
    return render_template('configuracion.html', nacionalidades=nacionalidad, puestos=puestos)

# CRUD DE NACIONALIDAD


@app.route('/Agregar_Nacionalidad', methods=['POST'])
def Agregar_Nacionalidad():
    if request.method == 'POST':
        cursor = conexion.connection.cursor()
        nacionalidad = request.form.get('nac')
        query = "INSERT INTO nacionalidad(Nacionalidad) VALUES (%s)"
        valores = (nacionalidad,)
        cursor.execute(query, valores)
        conexion.connection.commit()
        # flash('Nacionalidad Agregada!')
        return redirect(url_for('Configuracion'))


@app.route('/deletN/<id>')
def deletN(id):
    cursor = conexion.connection.cursor()
    cursor.execute(f'DELETE FROM nacionalidad WHERE idNacionalidad={id}')
    conexion.connection.commit()
    return redirect(url_for('Configuracion'))


@app.route('/editN/<id>')
def editN(id):
    cursor = conexion.connection.cursor()
    cursor.execute(f'SELECT * FROM nacionalidad WHERE idNacionalidad={id}')
    nacionalidad = cursor.fetchall()
    return render_template('editar_nacionalidad.html', dato=nacionalidad[0])


@app.route('/actualizarN/<id>', methods=['POST'])
def actualizarN(id):
    if request.method == 'POST':
        cursor = conexion.connection.cursor()
        nac = request.form.get('nac')

        cursor.execute("""
            UPDATE nacionalidad 
            SET Nacionalidad=%s
            WHERE idNacionalidad=%s
            """, (nac, id))
        conexion.connection.commit()
        return redirect(url_for('Configuracion'))
# FIN CRUD DE NACIONALIDAD

# CRUD DE PUESTOS


@app.route('/Agregar_Puesto', methods=['POST'])
def Agregar_Puesto():
    if request.method == 'POST':
        cursor = conexion.connection.cursor()
        puesto = request.form.get('puesto')
        preciojornal = request.form.get('preciojornal')
        preciomensual = request.form.get('preciomensual')
        mensual = request.form.get('mensual')
        query = "INSERT INTO puesto(Categoria,jornaldiario_para_mensualeros,jornaldiario_para_jornaleros,mensual) VALUES (%s,%s,%s,%s)"
        valores = (puesto, preciomensual, preciojornal, mensual)
        cursor.execute(query, valores)
        conexion.connection.commit()
        # flash('Nacionalidad Agregada!')
        return redirect(url_for('Configuracion'))


@app.route('/deletP/<id>')
def deletP(id):
    cursor = conexion.connection.cursor()
    cursor.execute(f'DELETE FROM puesto WHERE idPuesto={id}')
    conexion.connection.commit()
    return redirect(url_for('Configuracion'))


@app.route('/editP/<id>')
def editP(id):
    cursor = conexion.connection.cursor()
    cursor.execute(f'SELECT * FROM puesto WHERE idPuesto={id}')
    puesto = cursor.fetchall()
    return render_template('editar_puesto.html', dato=puesto[0])


@app.route('/actualizarP/<id>', methods=['POST'])
def actualizarP(id):
    if request.method == 'POST':
        cursor = conexion.connection.cursor()
        puesto = request.form.get('puesto')
        preciojornal = request.form.get('preciojornal')
        preciomensual = request.form.get('preciomensual')
        mensual = request.form.get('mensual')
        cursor.execute("""
            UPDATE puesto 
            SET Categoria=%s,
            jornaldiario_para_mensualeros=%s,
            jornaldiario_para_jornaleros=%s,
            mensual=%s
            WHERE idPuesto=%s
            """, (puesto, preciomensual, preciojornal, mensual, id))
        conexion.connection.commit()
        return redirect(url_for('Configuracion'))

# FIN CRUD DE PUESTOS

#Faltas Mensualeros
@app.route('/Faltas_Mensualeros')
def Faltas_Mensualeros():
    cursor = conexion.connection.cursor()
    cursor.execute('SELECT * FROM faltas_mensualeros')
    empleados= cursor.fetchall()
    cursor.execute("""
            SELECT em.nombre_completo, em.apellido_completo, em.documento,fm.fecha
            FROM faltas_mensualeros AS fm   
            INNER JOIN `empleados` AS em ON fm.documento = em.documento
        """)
    faltas = cursor.fetchall()
    return render_template('Faltas.html',faltas=faltas)

@app.route('/agregar_Falta', methods=['POST'])
def agregar_Falta():
    cursor = conexion.connection.cursor()
    fecha = request.form.get('fecha')
    documento = request.form.get('doc')
    cursor.execute(
                "INSERT INTO faltas_mensualeros (documento, fecha) VALUES (%s, %s)", (documento, fecha))
    conexion.connection.commit()
    return redirect(url_for('Faltas_Mensualeros'))
   

#Borrar Faltas
@app.route('/borrar_falta/<documento>/<fecha>')
def borrar_falta(documento, fecha):
    cursor = conexion.connection.cursor()

    # Utiliza comillas simples alrededor de los valores en la consulta SQL
    cursor.execute(f"DELETE FROM faltas_mensualeros WHERE documento='{documento}' AND fecha='{fecha}'")

    conexion.connection.commit()

    return redirect(url_for('Faltas_Mensualeros'))

#Fin Faltas
# Crud Nomina de salarios


@app.route('/ElegirC_Nomina')
def ElegirC_Nomina():
    cursor = conexion.connection.cursor()
    cursor.execute('SELECT * FROM clientes')
    dato = cursor.fetchall()
    cursor.execute('SELECT * FROM tipo_empleado')
    tipos = cursor.fetchall()
    return render_template('elegirC_Nomina.html', datos=dato, tipos=tipos)




@app.route('/Clientenomina', methods=['POST'])
def Nomina_buscar():
    # Falta la parte de la entrada por ruc
    id_cliente = request.form.get('selectCliente')
    if not id_cliente:
        ruc = request.form['RUC_C']
        cursor.execute(
            f"SELECT id_cliente FROM clientes WHERE ruc={ruc}")
        id_clientereq = cursor.fetchone()
        id_cliente=id_clientereq[0]

    cursor = conexion.connection.cursor()
    # Aca traere los jornaleros para el calculo respectivo de sus salarios
    cursor.execute(
        f"""SELECT em.idEmpleados,em.nombre_completo,em.apellido_completo,em.documento,em.idPuesto,nom.id_nomina,em.id_tipo_empleado,
        nom.id_empleado,nom.sueldo,nom.fecha,nom.Deducciones,nom.Retiros,nom.Salario_Neto 
        FROM empleados AS em INNER JOIN  `nominas_salario` AS nom ON em.idEmpleados=nom.id_empleado  
        WHERE em.id_cliente={id_cliente} """
    )
    empleados = cursor.fetchall()

    meses_en_espanol = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    for empleado in empleados:
        id_empleado = empleado[0]
        nombre_completo = empleado[1]
        apellido_completo = empleado[2]
        documento = empleado[3]
        id_puesto = empleado[4]
        id_nomina = empleado[5]
        id_tipo_empleado = empleado[6]
        sueldo = empleado[8]
        fecha = empleado[9]
        deducciones = empleado[10]
        retiros = empleado[11]
        salario_neto = empleado[12]

        # Esta parte sería para sacar la cantidad de horas trabajadas hasta el momento y la cantidad de asistencias
        mes_fecha = fecha.month
        ano_fecha = fecha.year
        cursor.execute(f"""
            SELECT 
                id_empleado,
                MONTH(fecha) AS mes,
                YEAR(fecha) AS ano,
                SEC_TO_TIME(SUM(TIME_TO_SEC(horas_tot_dia))) AS total_segundos_trabajados,
                COUNT(*) AS cantidad_registros
            FROM asistencias
            WHERE id_empleado = {id_empleado} AND MONTH(fecha) = {mes_fecha} AND YEAR(fecha) = {ano_fecha}
            GROUP BY id_empleado, MONTH(fecha), YEAR(fecha);
        """)

        # Obtener la información para salarios específica para el empleado
        informacion_para_salarios = cursor.fetchall()
        # Obtener las horas trabajadas en formato de horas
        total_segundos = informacion_para_salarios[0][3]
        # Convertir de segundos a horas
        total_horas_trabajadas = (total_segundos.total_seconds() / 3600)

        # Aca vamos a traer los puestos con sus tarifas
        cursor.execute(
            f"""SELECT * FROM puesto WHERE idPuesto={id_puesto}""")
        puestos = cursor.fetchall()

        precio_hora_jornalero = (puestos[0][3]/8)
        precio_hora_mensualero = (puestos[0][2]/8)
        pago_mensual_mensualero = puestos[0][4]
        print(precio_hora_jornalero, precio_hora_mensualero,
              pago_mensual_mensualero)

        if id_tipo_empleado == 3:
            # Esta parte el cálculo de sueldo para los empleados jornaleros
            sueldoBruto = int(total_horas_trabajadas*precio_hora_jornalero)
            deducciones = int(sueldoBruto-(sueldoBruto*0.9))
            sueldoNeto = int(sueldoBruto-deducciones-retiros)
            print(sueldoBruto, deducciones, sueldoNeto)
            cursor.execute("""
                UPDATE nominas_salario 
                SET sueldo=%s,
                Deducciones=%s,
                Salario_Neto=%s
                WHERE id_empleado=%s
                AND MONTH(fecha) = %s
                AND YEAR(fecha) = %s;
            """, (sueldoBruto, deducciones, sueldoNeto, id_empleado, mes_fecha, ano_fecha))
            conexion.connection.commit()
        else:
            # Esta parte es para los empleados mensualeros
            cursor.execute(f"""
                SELECT COUNT(*) AS cantidad_registros
                FROM faltas_mensualeros AS fm   
                WHERE fm.documento = {documento} AND MONTH(fecha)={mes_fecha};
            """)

            faltas = cursor.fetchone()
            monto_faltas = faltas[0]* puestos[0][2]

            sueldoBruto = int(pago_mensual_mensualero)
            deducciones = int(sueldoBruto-(sueldoBruto*0.9))
            sueldoNeto = int(sueldoBruto-deducciones-retiros-monto_faltas)
            cursor.execute("""
                UPDATE nominas_salario 
                SET sueldo=%s,
                Deducciones=%s,
                Salario_Neto=%s
                WHERE id_empleado=%s
                AND MONTH(fecha) = %s
                AND YEAR(fecha) = %s;
            """, (sueldoBruto, deducciones, sueldoNeto, id_empleado, mes_fecha, ano_fecha))
            conexion.connection.commit()

    # Resto del código...
    # MES (movido fuera del bucle)
    mes_numero = empleado[9].month
    ano=empleado[9].year
    mes_nombre = meses_en_espanol[mes_numero - 1]

    return render_template('Nomina_salarios.html', empleados=empleados,mes_nombre=mes_nombre,ano=ano)

# Fin Crud nomina de salarios

# Aca sera la creacion del pdf

@app.route('/generar_pdf/<empleado_id>/<fecha>')
def generar_pdf(empleado_id, fecha):
    cursor = conexion.connection.cursor()

    # Convierte 'fecha' a un objeto de tipo datetime si no lo es
    if not isinstance(fecha, datetime):
        fecha = datetime.strptime(fecha, "%Y-%m-%d")

    mes_numero = fecha.month
    ano = fecha.year
    # Realiza la consulta para obtener los datos del salario
    cursor.execute(
        f"SELECT * FROM nominas_salario WHERE id_empleado={empleado_id} AND MONTH(fecha)={mes_numero}")
    empleado = cursor.fetchone()

    # Realiza la consulta para obtener los datos del empleado
    cursor.execute(
        f"SELECT nombre_completo, apellido_completo,id_tipo_empleado,documento,idPuesto FROM empleados WHERE idEmpleados={empleado_id}")
    datosempleado = cursor.fetchone()

    # Configura el formato de moneda local
    locale.setlocale(locale.LC_ALL, 'es_PY.UTF-8')

    # Verifica si se encontraron datos del salario y del empleado
    if empleado and datosempleado:
        # Obtén el nombre del mes en español
        meses_en_espanol = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        mes_nombre = meses_en_espanol[mes_numero - 1]

        if datosempleado[2]==3:
        # Generar PDF en un archivo temporal
            with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
                pdf_filename = f"recibo_pago_{datosempleado[0]}_{mes_nombre}.pdf"

                # Crear PDF
                pdf = canvas.Canvas(temp_pdf.name)
                pdf.drawString(100, 820, f"Astil Group")
                pdf.drawString(100, 800, f"Recibo de Pago - {mes_nombre} - {ano}")
                pdf.drawString(
                    100, 780, f"Nombre:  {datosempleado[0]} {datosempleado[1]}")
                pdf.drawString(
                    100, 760, f"Sueldo Bruto: GS {locale.format_string('%.0f', empleado[2], grouping=True)}")
                pdf.drawString(
                    100, 740, f"Deduccion IPS: GS {locale.format_string('%.0f', empleado[4], grouping=True)}")
                pdf.drawString(
                    100, 720, f"Retiros: GS {locale.format_string('%.0f', empleado[5], grouping=True)}")
                pdf.drawString(
                    100, 700, f"Sueldo Neto: GS {locale.format_string('%.0f', empleado[6], grouping=True)}")

                # Guardar el contenido del PDF
                pdf.save()

            # Leer el contenido del PDF desde el archivo temporal
            with open(temp_pdf.name, 'rb') as pdf_file:
                response = Response(
                    pdf_file.read(), content_type='application/pdf')
                response.headers['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'

            return response
        else:
            documento=datosempleado[3]
            id_puesto=datosempleado[4]
            cursor.execute(f"""
            SELECT COUNT(*) AS cantidad_registros
            FROM faltas_mensualeros AS fm   
            Where fm.documento = {documento} AND MONTH(fecha)={mes_numero}
        """)
            
            faltas = cursor.fetchone()
            cursor.execute(
            f"""SELECT * FROM puesto WHERE idPuesto={id_puesto}""")
            puestos = cursor.fetchall()
            monto_faltas=faltas[0]*puestos[0][2]
            
            with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
                pdf_filename = f"recibo_pago_{datosempleado[0]}_{mes_nombre}.pdf"

                # Crear PDF
                pdf = canvas.Canvas(temp_pdf.name)
                pdf.drawString(100, 820, f"Astil Group")
                pdf.drawString(100, 800, f"Recibo de Pago - {mes_nombre}- 2024")
                pdf.drawString(
                    100, 780, f"Nombre:  {datosempleado[0]} {datosempleado[1]}")
                pdf.drawString(
                    100, 760, f"Sueldo Bruto: GS {locale.format_string('%.0f', empleado[2], grouping=True)}")
                pdf.drawString(
                    100, 740, f"Deduccion IPS: GS {locale.format_string('%.0f', empleado[4], grouping=True)}")
                pdf.drawString(
                    100, 720, f"Retiros: GS {locale.format_string('%.0f', empleado[5], grouping=True)}")
                pdf.drawString(
                    100, 700, f"Faltas:  {faltas[0]}")
                pdf.drawString(
                    100, 680, f"Deduccion Faltas: GS {locale.format_string('%.0f', monto_faltas, grouping=True)}")
                pdf.drawString(
                    100, 660, f"Sueldo Neto: GS {locale.format_string('%.0f', empleado[6], grouping=True)}")

                # Guardar el contenido del PDF
                pdf.save()

            # Leer el contenido del PDF desde el archivo temporal
            with open(temp_pdf.name, 'rb') as pdf_file:
                response = Response(
                    pdf_file.read(), content_type='application/pdf')
                response.headers['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'

            return response
            
            
            
    else:
        return "Empleado no encontrado", 404

#Fin creacion de PDF

# Decucciones


@app.route('/deducciones')
def deducciones():
    try:
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT * FROM deductions")
        deductions = cursor.fetchall()
        return render_template('deducciones.html', deductions=deductions)
    finally:
        cursor.close()


@app.route('/agregar_deduccion', methods=['POST'])
def agregar_deduccion():
    try:
        cursor = conexion.connection.cursor()
        if request.method == 'POST':
            description = request.form['description']
            amount = float(request.form['amount'])

            cursor.execute(
                "INSERT INTO deductions (description, amount) VALUES (%s, %s)", (description, amount))
            conexion.connection.commit()

            cursor.execute("SELECT * FROM deductions")
            deductions = cursor.fetchall()

            return jsonify({'message': 'Deducción agregada correctamente', 'deductions': deductions})
    finally:
        cursor.close()

# Ruta para editar una deducción


@app.route('/editar_deducion/<id>')
def editar_deduccion(id):
    cursor = conexion.connection.cursor()
    cursor.execute(f"SELECT * FROM deductions where id={id}")
    deductions = cursor.fetchall()
    cursor.close()
    return render_template('editar_deduccion.html', deductions=deductions[0])


@app.route('/Guardar_deduccion/<id>', methods=['POST'])
def Guardar_deduccion(id):
    if request.method == 'POST':
        cursor = conexion.connection.cursor()
        description = request.form['edit_description']
        amount = request.form['edit_amount']

        cursor.execute("""
            UPDATE deductions 
            SET description=%s,
            amount=%s
            WHERE id=%s
            """, (description, amount, id))
        conexion.connection.commit()
        return redirect(url_for('deducciones'))
# Ruta para eliminar una deducción


@app.route('/borrar_deducion/<id>')
def borrar_deducion(id):
    cursor = conexion.connection.cursor()
    cursor.execute(f'DELETE FROM deductions WHERE id={id}')
    conexion.connection.commit()
    return redirect(url_for('deducciones'))
# Fin deducciones

# Adelantos de efectivo


@app.route('/Adelantos')
def Adelantos():
    cursor = conexion.connection.cursor()

    try:
        # Obtener datos de adelantos y empleados
        cursor.execute("""
            SELECT ade.id, ade.date_advance, ade.employee_id, ade.amount, em.nombre_completo, em.apellido_completo
            FROM cashadvance AS ade
            INNER JOIN `empleados` AS em ON ade.employee_id = em.idEmpleados
        """)
        adelantos = cursor.fetchall()

        # Iterar sobre los adelantos
        for adelanto in adelantos:
            id_adelanto, fecha_adelanto, id_empleado, monto_adelanto, _, _ = adelanto

            # Obtener mes y año del adelanto
            mes_adelanto = fecha_adelanto.month
            ano_adelanto = fecha_adelanto.year

            # Verificar si ya se actualizó este adelanto en la nomina_salario
            cursor.execute("""
                SELECT 1 FROM adelantos_actualizados
                WHERE id_adelanto = %s
            """, (id_adelanto,))

            # Si no se ha actualizado, realizar la actualización y marcar como actualizado
            if not cursor.fetchone():
                cursor.execute("""
                    UPDATE nominas_salario 
                    SET Retiros = Retiros + %s
                    WHERE id_empleado = %s AND MONTH(fecha) = %s AND YEAR(fecha) = %s
                """, (monto_adelanto, id_empleado, mes_adelanto, ano_adelanto))

                # Marcar como actualizado en la tabla de seguimiento
                cursor.execute("""
                    INSERT INTO adelantos_actualizados (id_adelanto)
                    VALUES (%s)
                """, (id_adelanto,))

        # Confirmar la transacción
        conexion.connection.commit()

    finally:
        # Cerrar el cursor
        cursor.close()

    return render_template('adelantos.html', adelantos=adelantos)


@app.route('/agregar_adelanto', methods=['POST'])
def agregar_adelanto():
    try:
        cursor = conexion.connection.cursor()
        if request.method == 'POST':
            fecha = request.form['fecha']
            id_empleado = request.form['id_empleado']
            monto = request.form['monto']

            # Convertir la fecha a un objeto datetime
            fecha_adelanto = datetime.strptime(fecha, '%Y-%m-%d')

            # Verificar si ya existe un adelanto para la misma fecha, año e ID de empleado
            cursor.execute("""
                SELECT 1 FROM cashadvance
                WHERE employee_id = %s AND DAY(date_advance) = %s AND MONTH(date_advance) = %s AND YEAR(date_advance) = %s
            """, (id_empleado, fecha_adelanto.day, fecha_adelanto.month, fecha_adelanto.year))

            if not cursor.fetchone():
                # Si no existe, realizar la inserción
                cursor.execute(
                    "INSERT INTO cashadvance (date_advance, employee_id, amount) VALUES (%s, %s, %s)",
                    (fecha, id_empleado, monto))
                conexion.connection.commit()
                return redirect(url_for('Adelantos'))
            else:
                flash('Ya existe un adelanto para este día, mes y año.')
                return redirect(url_for('Adelantos'))

    finally:
        # Cerrar el cursor
        cursor.close()


@app.route('/borrar_adelanto/<id>')
def borrar_adelanto(id):
    cursor = conexion.connection.cursor()
    try:
        # Obtener información del adelanto antes de eliminarlo
        cursor.execute("""
            SELECT a.employee_id, a.date_advance, a.amount, n.id_nomina
            FROM cashadvance a
            INNER JOIN nominas_salario n ON a.employee_id = n.id_empleado
            WHERE a.id = %s
        """, (id,))
        adelanto_info = cursor.fetchone()

        if adelanto_info:
            id_empleado, fecha_adelanto, monto_adelanto, id_nomina = adelanto_info

            # Agrega esta línea para imprimir el monto antes de la actualización
            print("Monto Adelanto:", monto_adelanto)

            # Eliminar registros de adelantos_actualizados relacionados
            cursor.execute("""
                DELETE FROM adelantos_actualizados
                WHERE id_adelanto = %s
            """, (id,))

            # Eliminar el adelanto en cashadvance
            cursor.execute("""
                DELETE FROM cashadvance
                WHERE id = %s
            """, (id,))

            # Restar el monto de adelanto a la nomina_salario
            cursor.execute("""
    UPDATE nominas_salario 
    SET Retiros = Retiros - %s
    WHERE id_nomina = %s
""", (monto_adelanto, id_nomina))

            conexion.connection.commit()

    finally:
        cursor.close()

    return redirect(url_for('Adelantos'))


# Fin adelantos
if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)
