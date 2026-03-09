from flask import Flask, render_template, request, redirect
from database import get_connection

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/employees')
def employees():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("employees.html", employees=employees)


@app.route('/add_employee', methods=['POST'])
def add_employee():

    name = request.form['emp_name']
    team = request.form['team']
    doj = request.form['date_of_joining']

    connection = get_connection()
    cursor = connection.cursor()

    query = "INSERT INTO employees (emp_name, team, date_of_joining) VALUES (%s,%s,%s)"
    cursor.execute(query,(name,team,doj))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect('/employees')


@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_employee(id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':

        name = request.form['emp_name']
        team = request.form['team']
        doj = request.form['date_of_joining']

        query = "UPDATE employees SET emp_name=%s, team=%s, date_of_joining=%s WHERE emp_id=%s"
        cursor.execute(query,(name,team,doj,id))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect('/employees')

    cursor.execute("SELECT * FROM employees WHERE emp_id=%s",(id,))
    employee = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("edit_employee.html", employee=employee)


@app.route('/delete/<int:id>')
def delete_employee(id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM employees WHERE emp_id=%s",(id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect('/employees')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
