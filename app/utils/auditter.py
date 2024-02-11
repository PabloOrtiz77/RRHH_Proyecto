from flask import g

def error_log(error, user):
    cursor = g.conexion.cursor()
    cursor.execute(f"""
    INSERT INTO `auditoria`(`id_usuario`, `descripcion`, `fecha`) 
    VALUES ({user},'{error}',NOW());
    """)
    g.conexion.commit()
    cursor.close()

def success_log(success, user):
    cursor = g.conexion.cursor()
    cursor.execute(f"""
    INSERT INTO `auditoria`(`id_usuario`, `descripcion`, `fecha`) 
    VALUES ({user},'{success}',NOW());
    """)
    g.conexion.commit()
    cursor.close()

def login_log(user):
    cursor = g.conexion.cursor()
    cursor.execute(f"""
    INSERT INTO `auditoria`(`id_usuario`, `descripcion`, `fecha`) 
    VALUES ({user},'Inicio de sesión',NOW());
    """)
    g.conexion.commit()
    cursor.close()

def logout_log(user):
    cursor = g.conexion.cursor()
    cursor.execute(f"""
    INSERT INTO `auditoria`(`id_usuario`, `descripcion`, `fecha`) 
    VALUES ({user},'Cierre de sesión',NOW());
    """)
    g.conexion.commit()
    cursor.close()

def register_log(user):
    cursor = g.conexion.cursor()
    cursor.execute(f"""
    INSERT INTO `auditoria`(`id_usuario`, `descripcion`, `fecha`) 
    VALUES ({user},'Registro de usuario',NOW());
    """)
    g.conexion.commit()
    cursor.close()

def delete_log(user):
    cursor = g.conexion.cursor()
    cursor.execute(f"""
    INSERT INTO `auditoria`(`id_usuario`, `descripcion`, `fecha`) 
    VALUES ({user},'Eliminación de usuario',NOW());
    """)
    g.conexion.commit()
    cursor.close()

def update_log(user):
    cursor = g.conexion.cursor()
    cursor.execute(f"""
    INSERT INTO `auditoria`(`id_usuario`, `descripcion`, `fecha`) 
    VALUES ({user},'Actualización de usuario',NOW());
    """)
    g.conexion.commit()
    cursor.close()

