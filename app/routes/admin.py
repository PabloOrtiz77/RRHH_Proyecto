from flask import Blueprint, g, render_template
from flask import request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from datetime import datetime
from ..utils.utils import dibujar
import calendar
from ..utils.User import User




admin_routes = Blueprint('admin_routes', __name__)



@admin_routes.route('/inicio', methods=['POST'])
def login_admin():
    usuario = request.form.get('Usuario')
    contra = request.form.get('Contrasena')
    cursor = g.conexion.cursor()
    sql = "SELECT * FROM usuarios WHERE usuario=%s AND contrasena=%s AND tipo_usuario=%s"
    valores = (usuario, contra, 1)
    cursor.execute(sql, valores)
    datos = cursor.fetchall()
    numero_filas = len(datos)

    if numero_filas > 0:
        user = User(datos[0])
        login_user(user) 
        cursor.close()
        return render_template('acceso_admin.html')
    else:
        cursor.close()
        mensaje_alerta = "Usuario Erroneo!"
        return redirect(url_for('index', mensaje_alerta=mensaje_alerta))
    
@admin_routes.route('/inicio')
def volver_admin():
    return render_template('acceso_admin.html')


#ruta principal Para la gestion de empleados

@admin_routes.route('/gestion')
def gestion_empleados():
    cursor = g.conexion.cursor()
    # Aca extraemos los datos que hay en la seccion de empleados
    cursor.execute("""
        SELECT e.idEmpleados,e.nombre_completo,e.apellido_completo,e.documento,e.contrato,n.Nacionalidad,p.Categoria,e.idEstado,e.telefono,c.razon_social,tip.descripcion_tipo,Fecha_de_ingreso	
        FROM `empleados` AS e INNER JOIN `nacionalidad` AS n ON e.idNacionalidad=n.idNacionalidad 
        INNER JOIN `puesto` AS p ON p.idPuesto=e.idPuesto INNER JOIN `clientes` as c ON e.id_cliente=c.id_cliente 
        INNER JOIN `tipo_empleado` AS tip ON tip.id_tipo_empleado=e.id_tipo_empleado
        ;""")
    data = cursor.fetchall()

    cursor.execute("""SELECT * FROM clientes """)
    data2 = cursor.fetchall()
    cursor.execute(f"""SELECT * FROM `nacionalidad`;""")
    nacionalidad = cursor.fetchall()
    cursor.execute(f"""SELECT * FROM `puesto`;""")
    puestos = cursor.fetchall()
    cursor.execute(f"""SELECT * FROM `tipo_empleado`;""")
    tipos = cursor.fetchall()

    return render_template('gestion_empleados.html', infos=data, dato=data2, nacionalidades=nacionalidad, puestos=puestos, tipos=tipos)


# Para BUSCAR empleados
@admin_routes.route('/gestion/buscar', methods=['POST'])
def buscar():
    buscar = request.form.get('buscar')
    if buscar:
        cursor = g.conexion.cursor()

        cursor.execute(f"""
        SELECT e.idEmpleados,e.nombre_completo,e.apellido_completo,e.documento,e.contrato,n.Nacionalidad,p.Categoria,e.idEstado,e.telefono,c.razon_social,tip.descripcion_tipo,Fecha_de_ingreso,e.id_cliente	
        FROM `empleados` AS e INNER JOIN `nacionalidad` AS n ON e.idNacionalidad=n.idNacionalidad 
        INNER JOIN `puesto` AS p ON p.idPuesto=e.idPuesto INNER JOIN `clientes` as c ON e.id_cliente=c.id_cliente 
        INNER JOIN `tipo_empleado` AS tip ON tip.id_tipo_empleado=e.id_tipo_empleado
            WHERE e.documento={buscar};
        """)

        data = cursor.fetchall()

        if data:
            id_cliente = data[0][12]
            cursor.execute(
                f"""SELECT * FROM clientes WHERE id_cliente={id_cliente}""")
            data2 = cursor.fetchall()
            cursor.execute(f"""SELECT * FROM `nacionalidad`;""")
            nacionalidad = cursor.fetchall()
            cursor.execute(f"""SELECT * FROM `puesto`;""")
            puestos = cursor.fetchall()
            cursor.execute(f"""SELECT * FROM `tipo_empleado`;""")
            tipos = cursor.fetchall()

            return render_template('gestion_empleados.html', infos=data, dato=data2, nacionalidades=nacionalidad, puestos=puestos, tipos=tipos)
        else:
            flash(
                'No se encontraron resultados para el empleado con el documento proporcionado.', 'error')

    return redirect(url_for('admin_routes.gestion_empleados'))


# Crud Para Clientes


@admin_routes.route('/gestionclientes')
def gestion_clientes():
    cursor = g.conexion.cursor()
    # Aca extraemos los datos que hay en la seccion de clientes
    cursor.execute("""
    SELECT * FROM clientes""")
    data = cursor.fetchall()

    return render_template('gestion_clientes.html', infos=data)


@admin_routes.route('/gestionclientes/buscar', methods=['POST'])
def buscarC():
    buscar = request.form.get('buscar')
    print(buscar)
    if buscar:
        cursor = g.conexion.cursor()

        cursor.execute(f"""SELECT * FROM clientes
                        WHERE ruc='{buscar}'
                        """)
        data = cursor.fetchall()

        if data:
            return render_template('gestion_clientes.html', infos=data)
        else:
            flash(
                'No se encontraron resultados para el cliente con el RUC proporcionado.', 'error')

    return redirect(url_for('admin_routes.gestion_clientes'))


# Planilla de Asistencia

@admin_routes.route('/planilla/elegir')
def ElegirC():
    cursor = g.conexion.cursor()
    cursor.execute(f'SELECT * FROM clientes')
    dato = cursor.fetchall()
    return render_template('elegirC.html', datos=dato)



@admin_routes.route('/planilla/asistencia', methods=['GET', 'POST'])
def Planilla():
    # aca el ruc asi que tengo que hacer una  modificacion para que sea solo uno de los dos
    resultado = 0
    ruc = request.form.get('RUC_C')
    #print("hola"+ruc)
    # este es para el nav de la barra de busqueda por ruc
    if ruc != None:
        cursor = g.conexion.cursor()
        cursor.execute("SELECT id_cliente FROM clientes WHERE ruc = %s", (ruc,))
        data2 = cursor.fetchall()    
        if data2:
            resultado = dibujar(data2[0][0])
    else:
        razon = request.form.get('cliente')
        resultado = dibujar(razon)
    # aca estoy trayendo el id
    if resultado == 0 :
        flash('No se encontraron resultados para el cliente seleccionado.', 'error')
        return redirect(url_for('admin_routes.ElegirC'))
    return render_template('planilla_asistencia.html', dia_mes=resultado[4], dia=resultado[3], fecha_actual=resultado[2], infos=resultado[0], dato=resultado[1])


@admin_routes.route('/asistencia/guardar/<int:id>/<int:id_c>', methods=['POST'])
def guardar_asistencia(id, id_c):
    cursor = g.conexion.cursor()
    dia = request.form.get('dia')
    fecha = request.form.get('fecha')
    print(fecha)
    ep1 = request.form.get('entrada_primer_turno1')
    sp1 = request.form.get('salida_primer_turno1')
    ep2 = request.form.get('entrada_segundo_turno2')
    sp2 = request.form.get('salida_segundo_turno2')

    # 07:00 12:00 13:00 17:00 20
    # Convierte las cadenas en objetos de tiempo
    entrada_manana = datetime.strptime(ep1, "%H:%M")
    salida_manana = datetime.strptime(sp1, "%H:%M")
    entrada_tarde = datetime.strptime(ep2, "%H:%M")
    salida_tarde = datetime.strptime(sp2, "%H:%M")

    # Calcula las diferencias de tiempo
    duracion_manana = salida_manana - entrada_manana
    duracion_tarde = salida_tarde - entrada_tarde

    # Suma las duraciones de ambos turnos para obtener el total de horas trabajadas en el día
    total_horas_trabajadas = duracion_manana + duracion_tarde

    query = "INSERT INTO asistencias(dia,fecha,primer_turno_E,primer_turno_S,segundo_turno_E,segundo_turno_S,horas_tot_dia,id_empleado,id_cliente) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s)"
    valores = (dia, fecha, ep1, sp1, ep2, sp2,
               total_horas_trabajadas, id, id_c)
    cursor.execute(query, valores)
    g.conexion.commit()

    # Aca iniciara la parte de las nominas para dejar en 0 luego actualizar a medida que pasan los dias del mes

    # Ver temas de la fecha que recupera mal y el tema de la logica de las fechas diferentes
    cursor.execute(f"""SELECT * FROM nominas_salario WHERE id_empleado={id}""")
    nomina_emopleado = cursor.fetchall()
    fecha_guardado = datetime.strptime(fecha, '%Y-%m-%d')
    mes_guardado = fecha_guardado.month
    ano_guardado = fecha_guardado.year

    # Fin

    if nomina_emopleado:
        print(nomina_emopleado[0][3])
        fecha_actual = nomina_emopleado[0][3]
        mes_actual = fecha_actual.month
        ano_actual = fecha_actual.year
        print(ano_actual, mes_actual)
        # Convertir ambos meses a cadenas con dos dígitos
        mes_actual_str = "{:02d}".format(mes_actual)
        mes_guardado_str = "{:02d}".format(mes_guardado)
        print(mes_actual_str, mes_guardado_str)
        # Aca si el mes y ano son diferentes insertar
        if mes_actual_str != mes_guardado_str or ano_actual != ano_guardado:
            # ver si el empleado es jornalero
            query = "INSERT INTO nominas_salario(id_empleado, sueldo, fecha, Deducciones, Retiros, Salario_Neto) VALUES (%s, %s, %s, %s, %s, %s)"
            valores = (id, 0, fecha, 0, 0, 0)
            cursor.execute(query, valores)
            g.conexion.commit()
    else:
        query = "INSERT INTO nominas_salario(id_empleado,sueldo,fecha,Deducciones,Retiros,Salario_Neto) VALUES (%s, %s, %s, %s, %s,%s)"
        valores = (id, 0, fecha, 0, 0, 0)
        cursor.execute(query, valores)
        g.conexion.commit()
    # Fin inicio Nominas

    cursor.close()
    flash('Asistencia Agregada!')
    resultado = dibujar(id_c)
    return render_template('planilla_asistencia.html', dia_mes=resultado[4], dia=resultado[3], fecha_actual=resultado[2], infos=resultado[0], dato=resultado[1])

# aca estare editando los dias correspondientes del mes


@admin_routes.route('/planilla/editar/<id>')
def editar_Pasistencia(id):
    # lógica para obtener el mes y el año actual
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Obtenemos el nombre de los meses
    month_name = calendar.month_name

    # lógica para obtener los datos del empleado
    cursor = g.conexion.cursor()
    cursor.execute(f"""SELECT asis.dia,e.documento,e.nombre_completo,e.apellido_completo,asis.fecha,asis.primer_turno_E,asis.primer_turno_S,asis.segundo_turno_E,asis.segundo_turno_S,e.idEmpleados,asis.id_asistencia,asis.id_cliente
    FROM `empleados` AS e INNER JOIN `asistencias` AS asis ON e.idEmpleados=asis.id_empleado
    WHERE e.idEmpleados={id}
    AND MONTH(asis.fecha) = {current_month}
    AND YEAR(asis.fecha) = {current_year};""")
    infos = cursor.fetchall()
    # aca modifique
    if infos:
        return render_template('editar_asistencias.html', infos=infos, current_month=current_month, current_year=current_year, month_name=month_name)
    else:
        return render_template("error.html")


@admin_routes.route('/vacaciones')
def gestion_vacaciones():
    cursor = g.conexion.cursor()
    cursor.execute("""
    SELECT * FROM vacaciones""")
    data = cursor.fetchall()
    return render_template('gestion_vacaciones.html', infos=data)