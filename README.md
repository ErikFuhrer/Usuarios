# Gestor de Usuarios MySQL con Python y Tkinter

Este es un programa con interfaz gráfica en `ttkbootstrap` que permite gestionar usuarios y bases de datos en un servidor **MySQL/MariaDB**.

## 🎯 Funcionalidades

- Crear usuarios nuevos con prefijo `db_` y su base de datos correspondiente.
- Asignar permisos solo sobre su base de datos.
- Ver usuarios existentes (filtrados con el patrón `db_%`).
- Eliminar usuarios junto con sus bases de datos.
- Validaciones para evitar duplicados y errores comunes.

---

## 📦 Requisitos

- Python 3.x
- Servidor MySQL o MariaDB en local
- Paquete Python necesario:
  ```bash
  pip install pymysql ttkbootstrap
  ```

## 🚀 Cómo usar

Ejecuta el archivo principal del programa:

```bash
python gestor_usuarios.py
```

1. Ingresa un nombre de usuario (sin el prefijo `db_`) y una contraseña.
2. Pulsa **"Crear Usuario y BD"** para generar el usuario y su base de datos.
3. Selecciona un usuario existente del desplegable y pulsa **"Eliminar Usuario Seleccionado"** para eliminarlo junto con su base de datos.

---

## 🛠️ Tecnologías Utilizadas

- **Interfaz gráfica:** `tkinter` y `ttkbootstrap`
- **Conexión a MySQL/MariaDB:** `pymysql`
- Consultas SQL seguras para gestión de usuarios y bases de datos

---

## 🧠 Notas Adicionales

- Este programa busca usuarios que comienzan con `db_`, útil para separar usuarios de bases de datos gestionadas automáticamente.
