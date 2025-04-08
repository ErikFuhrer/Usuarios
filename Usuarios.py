import tkinter as tk
from tkinter import messagebox, ttk
import pymysql

host = "localhost"
usuario = "root"
contrasena = "657e.89I"

def obtener_usuarios():
    try:
        conn = pymysql.connect(
            host=host,
            user=usuario,
            password=contrasena
        )
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT `User`FROM mysql.`user` u WHERE u.`User` like 'db_%'")
            usuarios = [user[0] for user in cursor.fetchall()]
        finally:
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
        conn = pymysql.connect(
            host=host,
            user=usuario,
            password=contrasena,
            autocommit=True
        )
        with conn.cursor() as cursor:
            # Verificar si el usuario ya existe
            cursor.execute("SELECT COUNT(*) FROM mysql.user WHERE user = %s", (usu,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", f"El usuario '{usu}' ya existe.")
                return

            # Verificar si la base de datos ya existe
            cursor.execute("SHOW DATABASES LIKE %s", (nombredb,))
            if cursor.fetchone():
                messagebox.showerror("Error", f"La base de datos '{nombredb}' ya existe.")
                return

            # Crear la base de datos
            cursor.execute(f"CREATE DATABASE `{nombredb}`")

            # Crear el usuario
            cursor.execute(f"CREATE USER %s@'%%' IDENTIFIED BY %s", (usu, contr))

            # Dar permisos solo sobre su propia base de datos
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

    confirm = messagebox.askyesno("Confirmar", f"¿Eliminar usuario '{nombreusuario}' y su base de datos '{nombreusuario}'?")
    if not confirm:
        return

    try:
        conn = pymysql.connect(
            host=host,
            user=usuario,
            password=contrasena,
            autocommit=True
        )
        with conn.cursor() as cursor:
            # Eliminar usuario y base de datos
            cursor.execute(f"DROP USER IF EXISTS %s@'%%'", (nombreusuario,))
            cursor.execute(f"DROP DATABASE IF EXISTS `{nombreusuario}`")

            messagebox.showinfo("Eliminado", f"Usuario '{nombreusuario}' y base de datos '{nombreusuario}' eliminados correctamente.")
            actualizar_lista_usuarios()

    except pymysql.MySQLError as error:
        messagebox.showerror("Error", f"No se pudo eliminar: {error}")
    finally:
        conn.close()

# --- Interfaz Gráfica ---
ventana = tk.Tk()
ventana.title("Gestor de Usuarios")
ventana.geometry("300x300")

tk.Label(ventana, text="Nombre de usuario:").pack()
tbusuario = tk.Entry(ventana)
tbusuario.pack()

tk.Label(ventana, text="Contraseña:").pack()
tbpassword = tk.Entry(ventana, show="*")
tbpassword.pack()

tk.Button(ventana, text="Crear Usuario y BD", command=crear_usuario).pack(pady=5)

tk.Label(ventana, text="Usuarios existentes:").pack()
listausuarios = ttk.Combobox(ventana, state="readonly")
listausuarios.pack(pady=5)
actualizar_lista_usuarios()

tk.Button(ventana, text="Eliminar Usuario Seleccionado", command=eliminar_usuario, bg="red", fg="white").pack(pady=5)

ventana.mainloop()
