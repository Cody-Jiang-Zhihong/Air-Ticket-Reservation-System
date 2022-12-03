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

# Define route for register
@app.route('/register/')
def register():
    return render_template('register.html')

# Define route for login
@app.route('/login/')
def login():
    return render_template('login.html')

# Authenticates the view flights
@app.route('/', methods=['GET', 'POST'])
def viewFlightsAuth():
    # grabs information from the forms
    source_city = request.form['source_city']
    airport_name1 = request.form['airport_name1']

    destination_city = request.form['destination_city']
    airport_name2 = request.form['airport_name2']

    departure_date1 = request.form['departure_date1']

    departure_date2 = request.form['departure_date2']
    arrival_date = request.form['arrival_date']

    # cursor used to send queries
    cursor = conn.cursor()
    queried = False

    # If first part is filled
    if source_city != "" and airport_name1 != "":
        # executes query
        query = "SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, " \
                "arrival_date_and_time, base_price, ID_num FROM flight natural join airport WHERE departure_airport = " \
                "%s AND city = %s"
        cursor.execute(query, (airport_name1, source_city))
        queried = True
    # If second part is filled
    elif destination_city != "" and airport_name2 != "":
        # executes query
        query = "SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, " \
                "arrival_date_and_time, base_price, ID_num FROM flight natural join airport WHERE arrival_airport = " \
                "%s AND city = %s"
        cursor.execute(query, (airport_name2, destination_city))
        queried = True
    # If last part of one way is filled
    elif departure_date1 != "":
        # executes query
        query = 'SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, " \
                "arrival_date_and_time, base_price, ID_num FROM flight WHERE departure_date_and_time = %s'
        cursor.execute(query, departure_date1)
        queried = True
    # If last part of round trip is filled
    elif departure_date2 != "" and arrival_date != "":
        # executes query
        query = 'SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, ' \
                '" \ "arrival_date_and_time, base_price, ID_num FROM flight WHERE departure_date_and_time = %s AND ' \
                'arrival_date_and_time = %s '
        cursor.execute(query, (departure_date2, arrival_date))
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

    customer = -1
    if "" not in [username, password]:
        # If the username is an email
        if "@" in username:
            customer = 1
        else:
            customer = 0

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    if customer == 1:
        query = 'SELECT * FROM customer WHERE email = %s and password = MD5(%s)'
        cursor.execute(query, (username, password))

    if customer == 0:
        query = 'SELECT * FROM airline_staff WHERE username = %s and password = MD5(%s)'
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
        return redirect(url_for('customer'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)


# Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    # grabs information from the forms
    username1 = request.form['username1']
    password1 = request.form['password1']
    email = request.form['email']
    building_name = request.form['building_name']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone_number = request.form['phone_number']
    passport_num = request.form['passport_num']
    passport_expiration = request.form['passport_expiration']
    passport_country = request.form['passport_country']
    date_of_birth1 = request.form['date_of_birth1']

    username2 = request.form['username2']
    password2 = request.form['password2']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth2 = request.form['date_of_birth2']
    airline_name = request.form['airline_name']

    customer_data = [username1, email, password1, building_name, street, city, state, phone_number, passport_num,
                     passport_expiration, passport_country, date_of_birth1]
    staff_data = [username2, password2, first_name, last_name, date_of_birth2, airline_name]

    customer = -1
    if "" not in customer_data:
        customer = 1
    elif "" not in staff_data:
        customer = 0

    if customer and "@" not in email:
        error = "Please enter a valid email"
        return render_template('register.html', error=error)

    if customer == -1:
        error = "Please fill in all fields for the section you're signing up for"
        return render_template('register.html', error=error)

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    if customer == 1:
        query = 'SELECT * FROM customer WHERE name = %s'
        cursor.execute(query, (username1))
    if customer == 0:
        query = 'SELECT * FROM airline_staff WHERE username = %s'
        cursor.execute(query, (username2))

    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    if data:
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error=error)
    else:
        if customer == 1:
            query = 'INSERT INTO customer VALUES(%s, %s, MD5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(query, (username1, email, password1, building_name, street, city, state, phone_number, passport_num, passport_expiration, passport_country, date_of_birth1))
            conn.commit()
            cursor.close()
            return render_template('index.html', register="You've been successfully registered as a Customer")
        if customer == 0:
            query = 'INSERT INTO airline_staff VALUES(%s, MD5(%s), %s, %s, %s, %s)'
            cursor.execute(query, (username2, password2, first_name, last_name, date_of_birth2, airline_name))
            conn.commit()
            cursor.close()
            return render_template('index.html', register="You've been successfully registered as an Airline Staff")

@app.route('/customer', methods=['GET', 'POST'])
def customer():
    username = session['username']
    # cursor = conn.cursor();
    # query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    # cursor.execute(query, (username))
    # data1 = cursor.fetchall()
    # for each in data1:
    #     print(each['blog_post'])
    # cursor.close()
    return render_template('customer.html', username=username)

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
