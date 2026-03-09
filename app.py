from flask import Flask, render_template, request, redirect
from database import get_connection

app = Flask(__name__)

# Home Page
@app.route('/')
def home():
    return render_template("index.html")


# Show Employee List
@app.route('/employees')
def employees():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("employees.html", employees=employees)


# Add Employee
@app.route('/add_employee', methods=['POST'])
def add_employee():

    name = request.form['emp_name']
    team = request.form['team']
    doj = request.form['date_of_joining']

    connection = get_connection()
    cursor = connection.cursor()

    query = "INSERT INTO employees (emp_name, team, date_of_joining) VALUES (%s,%s,%s)"
    cursor.execute(query, (name, team, doj))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect('/employees')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
