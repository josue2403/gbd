from flask import Flask, render_template, request, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de la conexión a la base de datos
def get_db_connection():
    conn = psycopg2.connect(
        dbname="bd1",
        user="postgres",
        password="DC123",
        host="localhost",
        port="5432"
    )
    return conn

@app.route('/tables')
def tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('tables.html', tables=tables)

@app.route('/', methods=['GET', 'POST'])
def query():
    results = None
    columns = None
    query = ""
    if request.method == 'POST':
        query = request.form['query']
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            if query.strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
            else:
                conn.commit()
                flash('Query executed successfully', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'ERROR: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()
    return render_template('query.html', query=query, results=results, columns=columns)

if __name__ == '__main__':
    app.run(debug=True)
