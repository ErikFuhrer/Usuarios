# Gestor de Usuarios MySQL con Python y Tkinter

Este es un programa simple con interfaz gráfica (Tkinter) para gestionar usuarios y bases de datos en un servidor **MariaDB / MySQL**. Permite:

- Crear usuarios nuevos con su base de datos.
- Asignar permisos solo sobre su base de datos.
- Ver usuarios existentes.
- Eliminar usuarios y sus bases de datos.
- Evita crear duplicados y valida errores comunes.

---

## Requisitos

- Python 3.x
- MariaDB o MySQL corriendo localmente
- Paquetes:

```bash
pip install pymysql
