import streamlit as st
import sqlitecloud

# Configuración inicial de la página
st.set_page_config(page_title="Inventario", layout="wide")

# Conexión a SQLite Cloud
conn = sqlitecloud.connect("sqlitecloud://cpxoojbnnk.sqlite.cloud:8860/inventario.db?apikey=KlWlcnawgXjsKrwLiBIGsDIsv0NE07BaI9TE7cmoGLc")
conn.execute("USE DATABASE inventario.db")

# Título de la aplicación
st.title("Inventario")

# Función para cargar datos
def cargar_datos():
    try:
        cursor = conn.execute("SELECT id, nombre, cantidad FROM piezas")
        datos = cursor.fetchall()
        return datos
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return []

# Mostrar datos en una tabla
def mostrar_tabla():
    datos = cargar_datos()
    if datos:
        st.table(
            [{"ID": row[0], "Nombre": row[1], "Cantidad": row[2]} for row in datos]
        )
    else:
        st.warning("No hay datos para mostrar.")

# Función para agregar una pieza
def agregar_pieza(nombre, cantidad):
    try:
        conn.execute("INSERT INTO piezas (nombre, cantidad) VALUES (?, ?)", (nombre, cantidad))
        conn.commit()
        st.success("Pieza agregada correctamente.")
    except Exception as e:
        st.error(f"Error al agregar la pieza: {e}")

# Función para actualizar una pieza
def actualizar_pieza(id_pieza, cantidad, operacion):
    try:
        if operacion == "Sumar":
            conn.execute("UPDATE piezas SET cantidad = cantidad + ? WHERE id = ?", (cantidad, id_pieza))
        elif operacion == "Restar":
            conn.execute("UPDATE piezas SET cantidad = cantidad - ? WHERE id = ?", (cantidad, id_pieza))
        else:
            st.error("Operación no válida. Usa 'Sumar' o 'Restar'.")
            return

        conn.commit()
        st.success("Cantidad actualizada correctamente.")
    except Exception as e:
        st.error(f"Error al actualizar la pieza: {e}")

# Función para eliminar una pieza
def eliminar_pieza(id_pieza):
    try:
        conn.execute("DELETE FROM piezas WHERE id = ?", (id_pieza,))
        conn.commit()
        st.success("Pieza eliminada correctamente.")
    except Exception as e:
        st.error(f"Error al eliminar la pieza: {e}")

# Interfaz principal
st.header("Gestión de Inventario")

# Mostrar la tabla
mostrar_tabla()

# Sección para agregar una nueva pieza
st.subheader("Agregar nueva pieza")
with st.form("agregar_pieza_form"):
    nombre = st.text_input("Nombre de la pieza:")
    cantidad = st.number_input("Cantidad inicial:", min_value=0, step=1)
    agregar_btn = st.form_submit_button("Agregar")
    if agregar_btn:
        if nombre and cantidad >= 0:
            agregar_pieza(nombre, cantidad)
        else:
            st.error("Por favor, complete todos los campos.")

# Sección para actualizar la cantidad de una pieza
st.subheader("Actualizar cantidad de una pieza")
with st.form("actualizar_pieza_form"):
    id_pieza = st.number_input("ID de la pieza:", min_value=1, step=1)
    cantidad_modificar = st.number_input("Cantidad a modificar:", min_value=1, step=1)
    operacion = st.selectbox("Operación:", ["Sumar", "Restar"])
    actualizar_btn = st.form_submit_button("Actualizar")
    if actualizar_btn:
        if id_pieza and cantidad_modificar > 0:
            actualizar_pieza(id_pieza, cantidad_modificar, operacion)
        else:
            st.error("Por favor, complete todos los campos correctamente.")

# Sección para eliminar una pieza
st.subheader("Eliminar una pieza")
with st.form("eliminar_pieza_form"):
    id_eliminar = st.number_input("ID de la pieza a eliminar:", min_value=1, step=1)
    eliminar_btn = st.form_submit_button("Eliminar")
    if eliminar_btn:
        if id_eliminar:
            eliminar_pieza(id_eliminar)
        else:
            st.error("Por favor, complete el campo correctamente.")

# Actualizar la tabla después de las operaciones
mostrar_tabla()

