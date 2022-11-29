# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

# Initialize the app from Flask
app = Flask(__name__)

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='final_project',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


# Define a route to hello function
@app.route('/')
def hello():
    cursor = conn.cursor();
    query = 'SELECT * FROM flight'
    cursor.execute(query)
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.close()
    return render_template('index.html', flights=data1)


# Define route for login
@app.route('/login')
def login():
    return render_template('login.html')


# Define route for register
@app.route('/register')
def register():
    return render_template('register.html')


# Authenticates the view flights
@app.route('/', methods=['GET', 'POST'])
def viewFlightsAuth():
    # grabs information from the forms
    source_city = request.form['source_city']
    airport_name1 = request.form['airport_name1']

    destination_city = request.form['destination_city']
    airport_name2 = request.form['airport_name2']

    departure_date = request.form['departure_date']

    # cursor used to send queries
    cursor = conn.cursor()
    queried = False

    # If first part is filled
    if source_city != "" and airport_name1 != "":
        # executes query
        query = "SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, " \
                "arrival_date_and_time, base_price, ID_num FROM flight natural join airport WHERE departure_airport = " \
                "%s and city = %s"
        cursor.execute(query, (airport_name1, source_city))
        queried = True
    # If second part is filled
    elif destination_city != "" and airport_name2 != "":
        # executes query
        query = "SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, " \
                "arrival_date_and_time, base_price, ID_num FROM flight natural join airport WHERE arrival_airport = " \
                "%s and city = %s"
        cursor.execute(query, (airport_name2, destination_city))
        queried = True
    # If last part is filled
    elif departure_date != "":
        # executes query
        query = 'SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, " \
                "arrival_date_and_time, base_price, ID_num FROM flight WHERE departure_date_and_time = %s'
        cursor.execute(query, departure_date)
        queried = True

    if queried:
        # stores the results in a variable
        data = cursor.fetchall()
        for d in data:
            print(d)
        # use fetchall() if you are expecting more than 1 data row
        cursor.close()
        error = None
        if data:
            return render_template('index.html', flights=data)
        else:
            # returns an error message to the html page
            cursor = conn.cursor();
            query = 'SELECT * FROM flight'
            cursor.execute(query)
            data1 = cursor.fetchall()
            for each in data1:
                print(each)
            cursor.close()
            error = 'Incomplete or incorrect data provided'
            return render_template('index.html', error=error, flights=data1)
    else:
        # returns an error message to the html page
        cursor = conn.cursor();
        query = 'SELECT * FROM flight'
        cursor.execute(query)
        data1 = cursor.fetchall()
        for each in data1:
            print(each)
        cursor.close()
        error = 'Incomplete or incorrect data provided'
        return render_template('index.html', error=error, flights=data1)


# Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM user WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if data:
        # creates a session for the user
        # session is a built in
        session['username'] = username
        return redirect(url_for('home'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)


# Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM user WHERE username = %s'
    cursor.execute(query, (username))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    if data:
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error=error)
    else:
        ins = 'INSERT INTO user VALUES(%s, %s)'
        cursor.execute(ins, (username, password))
        conn.commit()
        cursor.close()
        return render_template('index.html')


@app.route('/home')
def home():
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall()
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)


@app.route('/post', methods=['GET', 'POST'])
def post():
    username = session['username']
    cursor = conn.cursor();
    blog = request.form['blog']
    query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
    cursor.execute(query, (blog, username))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')


app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
