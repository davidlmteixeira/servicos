from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para criar a tabela de serviços no banco de dados
def create_table():
    conn = sqlite3.connect('services.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS services 
              (id INTEGER PRIMARY KEY, data TEXT, placa TEXT, description TEXT)''')
    conn.commit()
    conn.close()

# Rota para a página inicial
@app.route('/')
def index():
    create_table()
    conn = sqlite3.connect('services.db')
    c = conn.cursor()
    c.execute("SELECT * FROM services")
    services = c.fetchall()
    conn.close()
    return render_template('index.html', services=services)

# Rota para adicionar um novo serviço
@app.route('/add', methods=['POST'])
def add():
    data = request.form.get('data')
    placa = request.form.get('placa')
    description = request.form.get('description')
    
    conn = sqlite3.connect('services.db')
    c = conn.cursor()
    
    try:
        c.execute("INSERT INTO services (data, placa, description) VALUES (?, ?, ?)", (data, placa, description))
        conn.commit()
    except sqlite3.Error as e:
        print("Erro ao adicionar serviço:", e)
    finally:
        conn.close()
    
    return redirect(url_for('index'))

# Rota para a página de pesquisa
@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search_query')
    if search_query:
        conn = sqlite3.connect('services.db')
        c = conn.cursor()
        c.execute("SELECT * FROM services WHERE data LIKE ? OR placa LIKE ? OR description LIKE ?", 
                  ('%'+search_query+'%', '%'+search_query+'%', '%'+search_query+'%'))
        search_results = c.fetchall()
        conn.close()
        return render_template('index.html', search_results=search_results)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
