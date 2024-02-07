from flask import g
import datetime
# aca dibuja los empleados y demas que trabajan para los clientes
def dibujar(razon):
    cursor = g.conexion.cursor()
    # Aca extraemos los datos que hay en la seccion de empleados
    cursor.execute(f"""
    SELECT e.idEmpleados,e.documento,e.nombre_completo,e.apellido_completo,e.documento,e.contrato,n.Nacionalidad,p.Categoria,e.idEstado,e.telefono,c.razon_social,c.id_cliente	
    FROM `empleados` AS e INNER JOIN `nacionalidad` AS n ON e.idNacionalidad=n.idNacionalidad 
    INNER JOIN `puesto` AS p ON p.idPuesto=e.idPuesto INNER JOIN `clientes` as c ON e.id_cliente=c.id_cliente
    WHERE e.id_cliente={razon};""")
    data = cursor.fetchall()

    cursor.execute(f"""SELECT * FROM clientes WHERE id_cliente={razon}""")
    data2 = cursor.fetchall()

    fecha_actual = datetime.now()
    nombre_mes = fecha_actual.strftime("%B")
    dias_del_mes = [fecha_actual.replace(day=day)
                    for day in range(1, fecha_actual.day + 1)]

    # Días de la semana
    dias_semana = ["Lunes", "Martes", "Miércoles",
                   "Jueves", "Viernes", "Sábado", "Domingo"]

    # Obtenemos el día de la semana actual
    dia_semana = dias_semana[fecha_actual.weekday()]

    fecha_actual = fecha_actual.strftime('%Y-%m-%d')
    return data, data2, fecha_actual, dia_semana, nombre_mes
