from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'contacts'

mysql = MySQL(app)

#Settings
app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    sql = mysql.connection.cursor()
    sql.execute('SELECT * FROM contact')
    data = sql.fetchall()

    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_Contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contact (fullname, phone, email) VALUES (%s, %s, %s)',
                    (fullname, phone, email))
        mysql.connection.commit()
        flash('Contact Added successfully')

        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_Contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contact WHERE id = %s', [id])
    data = cur.fetchall()
    
    return render_template('edit_contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_Contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        sql = mysql.connection.cursor()
        sql.execute(""" 
            UPDATE contact
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        mysql.connection.commit()
        flash('Contact updated Sucessfully')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_Contact(id):
    sql = mysql.connection.cursor()
    sql.execute('DELETE FROM contact WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Deleted')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug=True)

