import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import pymysql

# --- Configuración base ---
host = "localhost"
usuario = "usuario"
contrasena = "contraseña"

# --- Funciones de base de datos ---
def obtener_usuarios():
    try:
        conn = pymysql.connect(host=host, user=usuario, password=contrasena)
        cursor = conn.cursor()
        cursor.execute("SELECT `User` FROM mysql.`user` u WHERE u.`User` like 'db_%'")
        usuarios = [user[0] for user in cursor.fetchall()]
        conn.close()
        return usuarios
    except pymysql.MySQLError as error:
        messagebox.showerror("Error", f"No se pudieron obtener los usuarios: {error}")
        return []

def actualizar_lista_usuarios():
    usuarios = obtener_usuarios()
    listausuarios['values'] = usuarios
    if usuarios:
        listausuarios.current(0)
    else:
        listausuarios.set("")

def crear_usuario():
    usu = "db_" + tbusuario.get().strip()
    contr = tbpassword.get().strip()
    nombredb = f"{usu}"

    if not usu or not contr:
        messagebox.showerror("Error", "Debe ingresar nombre de usuario y contraseña.")
        return

    try:
        conn = pymysql.connect(host=host, user=usuario, password=contrasena, autocommit=True)
        cursor = conn.cursor()

        # Verificar existencia
        cursor.execute("SELECT COUNT(*) FROM mysql.user WHERE user = %s", (usu,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Error", f"El usuario '{usu}' ya existe.")
            return

        cursor.execute("SHOW DATABASES LIKE %s", (nombredb,))
        if cursor.fetchone():
            messagebox.showerror("Error", f"La base de datos '{nombredb}' ya existe.")
            return

        # Crear usuario y base
        cursor.execute(f"CREATE DATABASE `{nombredb}`")
        cursor.execute(f"CREATE USER %s@'%%' IDENTIFIED BY %s", (usu, contr))
        cursor.execute(f"GRANT ALL PRIVILEGES ON `{nombredb}`.* TO %s@'%%'", (usu,))

        messagebox.showinfo("Éxito", f"Usuario '{usu}' y base de datos '{nombredb}' creados con éxito.")
        actualizar_lista_usuarios()
    except pymysql.MySQLError as error:
        messagebox.showerror("Error MySQL", f"Ocurrió un error: {error}")
    finally:
        conn.close()

def eliminar_usuario():
    nombreusuario = listausuarios.get()
    if not nombreusuario:
        messagebox.showerror("Error", "Debes seleccionar un usuario para eliminar.")
        return

    confirm = messagebox.askyesno("Confirmar", f"¿Eliminar usuario '{nombreusuario}' y su base de datos?")
    if not confirm:
        return

    try:
        conn = pymysql.connect(host=host, user=usuario, password=contrasena, autocommit=True)
        cursor = conn.cursor()

        cursor.execute(f"DROP USER IF EXISTS %s@'%%'", (nombreusuario,))
        cursor.execute(f"DROP DATABASE IF EXISTS `{nombreusuario}`")

        messagebox.showinfo("Eliminado", f"Usuario y base de datos '{nombreusuario}' eliminados correctamente.")
        actualizar_lista_usuarios()
    except pymysql.MySQLError as error:
        messagebox.showerror("Error", f"No se pudo eliminar: {error}")
    finally:
        conn.close()

# --- Interfaz gráfica con ttkbootstrap ---
ventana = tb.Window(themename="solar")
ventana.title("Gestor de Usuarios MySQL")
ventana.geometry("400x400")
ventana.resizable(False, False)

frm = tb.Frame(ventana, padding=20)
frm.pack(fill=BOTH, expand=True)

# --- Widgets ---
tb.Label(frm, text="Nombre de usuario:", anchor="w").pack(fill=X, pady=(0, 5))
tbusuario = tb.Entry(frm)
tbusuario.pack(fill=X, pady=(0, 10))

tb.Label(frm, text="Contraseña:", anchor="w").pack(fill=X, pady=(0, 5))
tbpassword = tb.Entry(frm, show="*")
tbpassword.pack(fill=X, pady=(0, 15))

tb.Button(frm, text="Crear Usuario y BD", command=crear_usuario, bootstyle=SUCCESS).pack(fill=X, pady=5)

tb.Label(frm, text="Usuarios existentes:", anchor="w").pack(fill=X, pady=(15, 5))
listausuarios = tb.Combobox(frm, state="readonly")
listausuarios.pack(fill=X, pady=5)
actualizar_lista_usuarios()

tb.Button(frm, text="Eliminar Usuario Seleccionado", command=eliminar_usuario, bootstyle=DANGER).pack(fill=X, pady=10)

ventana.mainloop()
