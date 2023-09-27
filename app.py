import os
import pyodbc

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)

app = Flask(__name__)

server = 'az-aue-au-sql-dev-dpp-001.database.windows.net'
database = 'epc-subaru'
username = 'Neil'
password = '3pFt45KD?&d7XLze'

connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'

def get_db_connection():
    try:
        connection = pyodbc.connect(connection_string)
        return connection
    except pyodbc.Error as e:
        print(f"Error connecting to the database: {str(e)}")
        return None

@app.route('/')
def index():
   print('Request for index page received')
   connection = get_db_connection()
   if connection:
        return render_template('index.html')
   else:
        return jsonify({"error": "Failed to connect to the database."}), 500
   

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
