from flask import Blueprint, g, render_template
from flask import request, redirect, url_for




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
    sql = "SELECT * FROM usuarios WHERE usuario=%s AND contrasena=%s AND tipo_usuario=%s"
    valores = (usuario, contra, 2)
    cursor.execute(sql, valores)
    datos = cursor.fetchall()
    numero_filas = len(datos)

    if numero_filas > 0:
        cursor.close()
        return render_template('acceso_cliente.html')
    else:
        cursor.close()
        mensaje_alerta = "Usuario Erroneo!"
        return redirect(url_for('client_routes.clientes', mensaje_alerta=mensaje_alerta))


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

    if (con == 4):
        query = "INSERT INTO usuarios(nombre_completo,documento,usuario,contrasena,tipo_usuario) VALUES (%s, %s, %s, %s, %s)"
        valores = (nombre_completo, documento,
                   usuario, contrasena, tipoUsuario)
        cursor.execute(query, valores)
        g.conexion.commit()
        cursor.close()
        return render_template('clientes.html')
    else:
        cursor.close()
        mensaje_alerta = "Complete todos los campos!"
        return redirect(url_for('client_routes.clientes', mensaje_alerta=mensaje_alerta))


