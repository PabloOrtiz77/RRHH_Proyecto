#hacer calculo de salarios una vez al mes
from datetime import datetime
import mysql.connector

# Establish a connection to the MySQL database
def establish_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="astil"
        )
        return connection
    except mysql.connector.Error as error:
        print("Failed to connect to MySQL database:", error)




def generar_salarios_mes():
    connection = establish_connection()
    cursor = connection.cursor()
    print("Generando salarios del mes")
    # Fetch all "mensualeros"
    cursor.execute("SELECT idEmpleados FROM empleados WHERE id_tipo_empleado = 4")
    mensualeros = cursor.fetchall()
    print(mensualeros)
    for mensualero in mensualeros:
        id_empleado = mensualero[0]
        print(id_empleado)
        # Calculate initial salary and deductions
        # This is just an example, replace with your own calculations
        sueldo = 2500000
        deducciones = 250000
        retiros = 0
        salario_neto = sueldo - deducciones - retiros

        # Insert a new row in the "nominas_salario" table
        cursor.execute(
            "INSERT INTO nominas_salario (id_empleado, sueldo, fecha, Deducciones, Retiros, Salario_Neto) VALUES (%s, %s, %s, %s, %s, %s)",
            (id_empleado, sueldo, datetime.now(), deducciones, retiros, salario_neto)
        )

    connection.commit()
    cursor.close()


class Config(object):
     SCHEDULER_API_ENABLED = True
     JOBS = [
    {
        'id': 'generar_salarios_mes_job',
        'func': 'app.utils.jobs:generar_salarios_mes',
        'trigger': 'interval',
        'minutes': 1

    }
]
