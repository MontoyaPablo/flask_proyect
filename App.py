from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'flaskplanilla'
mysql = MySQL(app)

#seetting
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/Ingresante', methods=['POST'])
def Ingresante():
    if request.method == 'POST':
        dni=request.form['dni']
        nombreCompleto = request.form['nombreCompleto']
        cur= mysql.connection.cursor()
        cur.execute('INSERT INTO persona (DNI, NombreCompleto) VALUES (%s,%s)', (dni,nombreCompleto))
        mysql.connection.commit()
        flash('Ingresante cargado con exito')
    return redirect(url_for('Index'))

@app.route('/PlanillaDeHerramientas')
def PlanillaDeHerramientas():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM herramientas')
    data = cur.fetchall()
    return render_template('planilla.html', planilla = data)

@app.route('/Consulta', methods=['GET','POST'])
def ConsultaIngresante():
    if request.method == 'POST':
        dni=request.form['dni']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM persona WHERE DNI = '%s'" %(dni))
        datos = cur.fetchall()
        cur.close()
        return render_template('tablaConHerramientas.html', datos = datos, busqueda = dni)
    
    return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def Eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM herramientas WHERE idHerramienta = {0} '.format(id))
    mysql.connection.commit()
    flash('Se elimino correctamente el registro')
    return redirect(url_for('PlanillaDeHerramientas'))

@app.route('/Registro', methods=['POST'])
def Registro():    
    if request.method == 'POST':
        dni=request.form['dni']
        nombreHerramienta = request.form['nombreHerramienta']
        cantidad = request.form['cantidad']
        cur= mysql.connection.cursor()
        cur.execute('INSERT INTO herramientas (nombreHerramienta, cantidad, dueñoHerramientas) VALUES (%s,%s,%s)', (nombreHerramienta, cantidad, dni))
        mysql.connection.commit()
        flash('herramientas cargada con exito')
    return redirect(url_for('PlanillaDeHerramientas'))


if __name__ == '__main__':
    app.run(port = 3000, debug = True)
