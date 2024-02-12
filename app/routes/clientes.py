from flask import Blueprint, g, render_template
from flask import request, redirect, url_for
from ..utils.User import User
from flask_login import login_user, login_required, current_user
from ..utils import auditter


client_routes = Blueprint('client_routes', __name__)


# nos dirigira a la pagina que seleccionamos , acceso a cliente
@client_routes.route('/')
def clientes():
    return render_template("clientes.html")

# Aca se hace la validacion de inicio de sesion de el cliente



@client_routes.route('/inicio', methods=['POST'])
def login_clientes():
    usuario = request.form.get('Usuario')
    contra = request.form.get('Contrasena')
    cursor = g.conexion.cursor()
    sql = "SELECT * FROM usuarios WHERE usuario=%s AND tipo_usuario=%s"
    valores = (usuario, 2)
    cursor.execute(sql, valores)
    datos = cursor.fetchall()
    numero_filas = len(datos)

    if numero_filas > 0:
        contrasena_hash = datos[0][4]
        if g.bcrypt.check_password_hash(contrasena_hash, contra):
            cursor.close()
            user = User(datos[0][0])  # assuming the first column is the user id
            login_user(user)  # log the user in
            return render_template('acceso_cliente.html')
        else:
            cursor.close()
            mensaje_alerta = "Contraseña incorrecta!"
            return redirect(url_for('client_routes.clientes', mensaje_alerta=mensaje_alerta))
    else:
        cursor.close()
        mensaje_alerta = "Usuario Erroneo!"
        return redirect(url_for('client_routes.clientes', mensaje_alerta=mensaje_alerta))


@client_routes.route('/acceso')
def acceso_clientes():
    return render_template('acceso_cliente.html')

# Aca se hara el registro del cliente
@client_routes.route('/', methods=['POST'])
def registro_clientes():
    
    cursor = g.conexion.cursor()
    nombre_completo = request.form.get('nombre_completo')
    documento = request.form.get('documento')
    usuario = request.form.get('usuario')
    contrasena = request.form.get('contrasena')
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

    if con == 4:
        hashed_password = g.bcrypt.generate_password_hash(contrasena)
        query = "INSERT INTO usuarios(nombre_completo,documento,usuario,contrasena,tipo_usuario) VALUES (%s, %s, %s, %s, %s)"
        valores = (nombre_completo, documento, usuario, hashed_password, tipoUsuario)
        cursor.execute(query, valores)
        g.conexion.commit()
        cursor.close()
        auditter.success_log(f'El usuario {usuario} se ha registrado', 0)
        return render_template('clientes.html')
    else:
        cursor.close()
        mensaje_alerta = "Complete todos los campos!"
        return redirect(url_for('client_routes.clientes', mensaje_alerta=mensaje_alerta))


def get_ruc():
    cursor = g.conexion.cursor()
    cursor.execute(f'SELECT * FROM usuarios WHERE id_usuario={current_user.get_id()}')
    
    usuario = cursor.fetchall()
    documento = usuario[0][2]
   
    return documento

@client_routes.route('/gestion')
def gestion_empleados():
    cursor = g.conexion.cursor()

    ruc = get_ruc()
    
    print(ruc)

    # Aca extraemos los datos que hay en la seccion de empleados
    cursor.execute("""
        SELECT e.idEmpleados,e.nombre_completo,e.apellido_completo,e.documento,e.contrato,n.Nacionalidad,p.Categoria,e.idEstado,e.telefono,c.razon_social,tip.descripcion_tipo,Fecha_de_ingreso	
        FROM `empleados` AS e INNER JOIN `nacionalidad` AS n ON e.idNacionalidad=n.idNacionalidad 
        INNER JOIN `puesto` AS p ON p.idPuesto=e.idPuesto INNER JOIN `clientes` as c ON e.id_cliente=c.id_cliente 
        INNER JOIN `tipo_empleado` AS tip ON tip.id_tipo_empleado=e.id_tipo_empleado
        WHERE c.ruc=%s """, (ruc,))
    data = cursor.fetchall()

    cursor.execute("""SELECT * FROM clientes WHERE ruc=%s""", (ruc,))
    data2 = cursor.fetchall()
    cursor.execute(f"""SELECT * FROM `nacionalidad`;""")
    nacionalidad = cursor.fetchall()
    cursor.execute(f"""SELECT * FROM `puesto`;""")
    puestos = cursor.fetchall()
    cursor.execute(f"""SELECT * FROM `tipo_empleado`;""")
    tipos = cursor.fetchall()

    return render_template('cliente_gestion_empleados.html', infos=data, dato=data2, nacionalidades=nacionalidad, puestos=puestos, tipos=tipos)

@client_routes.route('/vacaciones')
def gestion_vacaciones():
    cursor = g.conexion.cursor()
    cursor.execute("""
    SELECT * FROM vacaciones""")
    data = cursor.fetchall()
    return render_template('gestion_vacaciones.html', info=data)

@client_routes.route('/vacaciones/accept/<int:id>')
def accept_vacation(id):
    cursor = g.conexion.cursor()
    cursor.execute(f"""
    UPDATE vacaciones SET estado='Aceptado' WHERE idVacacion={id}""")
    g.conexion.commit()
    return redirect(url_for('client_routes.gestion_vacaciones'))

@client_routes.route('/vacaciones/reject/<int:id>')
def reject_vacation(id):
    cursor = g.conexion.cursor()
    cursor.execute(f"""
    UPDATE vacaciones SET estado='Rechazado' WHERE idVacacion={id}""")
    g.conexion.commit()
    return redirect(url_for('client_routes.gestion_vacaciones'))