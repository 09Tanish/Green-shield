from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import bcrypt

app = Flask(__name__)

# MySQL database connection
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Tanish@123',  # Updated password
    database='test'         # Database name
)

@app.route('/', methods=['GET'])
def form():
    # HTML form for registration
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve form data
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    gender = request.form['gender']
    email = request.form['email']
    password = request.form['password']
    number = request.form['number']

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert data into the database
    cursor = db.cursor()
    sql = "INSERT INTO registration (firstName, lastName, gender, email, password, number) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (first_name, last_name, gender, email, hashed_password, number))
    db.commit()
    cursor.close()

    return redirect(url_for('success'))

@app.route('/success')
def success():
    return "Registration successful!"

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change to a different port like 5001
