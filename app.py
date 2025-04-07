from flask import Flask, render_template, request, redirect, flash
import mysql.connector # type: ignore

app = Flask(__name__)
app.secret_key = "clave_secreta"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="proyecto_smorgas"
    )

@app.route('/')
def home():
    conn = None  
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM compra")
        ventas = cursor.fetchall()
    except Exception as e:
        flash(f"Error al obtener registros de ventas: {e}", "danger")
        ventas = []
    finally:
        if conn:  # Verificamos si conn no es None
            conn.close()
    
    return render_template('index.html', ventas=ventas)


#lo añadio shirley
@app.route('/pagina2')
def pagina2():
    return render_template('pagina2.html')

@app.route('/add', methods=['POST'])
def add():
    mesa = request.form['mesa']
    pedido = request.form['pedido'].strip()
    forma_pago = request.form['forma_pago']
    forma_entrega = request.form['forma_entrega']
    precio_pedido = request.form['precio_pedido']
    cuenta = request.form['cuenta']

    if not mesa or not pedido or not forma_pago or not forma_entrega or not precio_pedido or not cuenta:
        flash("Todos los campos son obligatorios", "warning")
        return redirect('/')

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO compra (mesa, pedido, forma_pago, forma_entrega, precio_pedido, cuenta) VALUES (%s, %s, %s, %s, %s, %s)",
            (mesa, pedido, forma_pago, forma_entrega, precio_pedido, cuenta)
        )
        conn.commit()
        flash("Venta registrada con éxito", "success")
    except Exception as e:
        flash(f"Error al registrar venta: {e}", "danger")
    finally:
        if conn:
            conn.close()
    
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM compra WHERE Folio = %s", (id,))
        conn.commit()
        flash("Registro eliminado con éxito", "success")
    except Exception as e:
        flash(f"Error al eliminar registro: {e}", "danger")
    finally:
        if conn:
            conn.close()
    
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    mesa = request.form['mesa']
    pedido = request.form['pedido'].strip()
    forma_pago = request.form['forma_pago']
    forma_entrega = request.form['forma_entrega']
    precio_pedido = request.form['precio_pedido']
    cuenta = request.form['cuenta']

    if not mesa or not pedido or not forma_pago or not forma_entrega or not precio_pedido or not cuenta:
        flash("Todos los campos son obligatorios", "warning")
        return redirect('/')

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE compra SET mesa = %s, pedido = %s, forma_pago = %s, forma_entrega = %s, precio_pedido = %s, cuenta = %s WHERE ID = %s",
            (mesa, pedido, forma_pago, forma_entrega, precio_pedido, cuenta, id)
        )
        conn.commit()
        flash("Registro actualizado con éxito", "success")
    except Exception as e:
        flash(f"Error al actualizar registro: {e}", "danger")
    finally:
        if conn:
            conn.close()
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
