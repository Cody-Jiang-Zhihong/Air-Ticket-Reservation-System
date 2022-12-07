# Import Flask Library
import random

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
    cursor = conn.cursor()
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

# Define route for Customer
@app.route('/customer/')
def customer():
    # Gets all available flights
    cursor = conn.cursor()
    query = 'SELECT * FROM flight'
    cursor.execute(query)
    data1 = cursor.fetchall()

    # # View My flights:
    # query = "SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, arrival_date_and_time, base_price, id_num FROM ticket NATURAL JOIN flight WHERE customer_email = (SELECT email \
    #                             FROM customer \
    #                             WHERE email = %s) AND"
    # cursor.execute(query, (session['username']))
    # data2 = cursor.fetchall()
    cursor.close()
    return render_template('customer.html', flights=data1)

# Define route for AirlineStuff
@app.route('/airlinestaff/')
def airlinestaff():
    return render_template('airlinestaff.html')

# Authenticates the view flights
@app.route('/viewFlightsAuth', methods=['GET', 'POST'])
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
            cursor = conn.cursor()
            query = 'SELECT * FROM flight'
            cursor.execute(query)
            data1 = cursor.fetchall()
            cursor.close()
            error = 'Incomplete or incorrect data provided'
            return render_template('index.html', error=error, flights=data1)
    else:
        # returns an error message to the html page
        cursor = conn.cursor()
        query = 'SELECT * FROM flight'
        cursor.execute(query)
        data1 = cursor.fetchall()
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
    if data and customer == 1:
        # creates a session for the user
        # session is a built in
        session['username'] = username
        return redirect(url_for('customer'))
    if data and customer == 0:
        session['username'] = username
        return redirect(url_for('airlinestaff'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        #return redirect(url_for('customerAuth'))
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
    phone_numbers = request.form['phone_numbers']
    email_addresses = request.form['email_addresses']

    customer_data = [username1, email, password1, building_name, street, city, state, phone_number, passport_num,
                     passport_expiration, passport_country, date_of_birth1]
    staff_data = [username2, password2, first_name, last_name, date_of_birth2, airline_name, phone_numbers, email_addresses]

    customer = -1
    if "" not in customer_data:
        customer = 1
    elif "" not in staff_data:
        customer = 0
        email_addresses = email_addresses.replace(" ", "")
        phone_numbers = phone_numbers.replace(" ", "")
        if "@" not in email_addresses:
            error = "Please enter a valid email"
            return render_template('register.html', error=error)

    if customer == 1 and "@" not in email:
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
            # Insert into airline_staff
            query = 'INSERT INTO airline_staff VALUES(%s, MD5(%s), %s, %s, %s, %s)'
            cursor.execute(query, (username2, password2, first_name, last_name, date_of_birth2, airline_name))
            conn.commit()

            # Insert into airline_staff emails
            query = 'INSERT INTO email_address VALUES(%s, %s)'
            cursor.execute(query, (username2, email_addresses))
            conn.commit()

            # Insert into airline_staff phone numbers
            query = 'INSERT INTO phone_number VALUES(%s, %s)'
            cursor.execute(query, (username2, phone_numbers))
            conn.commit()

            cursor.close()
            return render_template('index.html', register="You've been successfully registered as an Airline Staff")

@app.route('/customerAuth', methods=['GET', 'POST'])
def customerAuth():
    username = session['username']
    # cursor used to send queries
    cursor = conn.cursor()
    error = None
    queried = False

    # Generates random ticket_id, will failproof this later
    ticket_id = random.randint(1, 9999999)

    # Search for flights function
    if 'search' in request.form:
        source_city = request.form['source_city']
        airport_name1 = request.form['airport_name1']

        destination_city = request.form['destination_city']
        airport_name2 = request.form['airport_name2']

        departure_date1 = request.form['departure_date1']

        departure_date2 = request.form['departure_date2']
        arrival_date = request.form['arrival_date']

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
        else:
            error = "You're missing information required to search for a flight"

    # Perform action on flight (purchase ticket, cancel trip)
    if 'purchase' in request.form or 'cancel' in request.form:
        airline = request.form['p_airline']
        flight_number = request.form['p_flight_number']
        departure_date = request.form['p_departure_date']
        base_price = request.form['p_base_price']

        if airline != "" and flight_number != "" and departure_date != "":
            # if click purchase:
            if 'purchase' in request.form:
                query = "UPDATE ticket SET customer_email = (SELECT email FROM customer where name = %s) WHERE " \
                        "airline_name = %s AND flight_number = %s AND sold_price = %s AND customer_email IS NULL "
                cursor.execute(query, (username, airline, flight_number, base_price))

            # if click cancel:
            if 'cancel' in request.form:
                query = "DELETE FROM ticket \
                        WHERE airline = %s AND flight_number = %s"
                cursor.execute(query, (airline, flight_number))
                queried = True
        else:
            error = "You're missing information required to perform an action on a ticket"

    # Rate or comment on prev flight
    if 'submit_review' in request.form:
        airline = request.form['p_airline']
        flight_number = request.form['p_flight_number']
        departure_date = request.form['p_departure_date']
        rating = request.form['rating']
        review = request.form['comment']

        if airline != "" and flight_number != "" and departure_date != "":
            # If Give Ratings and Comment on previous flights: is filled
            if rating != "" and review != "" and 'submit_review' in request.form:
                # executes query
                query = "UPDATE review \
                            SET email = (SELECT email FROM customer where name = %s), \
                                airline_name = %s, flight_number = %s, rating = %s, review = %s"
                cursor.execute(query, (username, airline, flight_number, flight_number, rating, review))
            else:
                error = "You're missing information required to submit a review"
        else:
            error = "You're missing information required to submit a review"

    # Track my spending
    if 'track' in request.form:
        start_date = request.form['date_start']
        end_date = request.form['date_end']

        # If Track My Spending: is filled
        if start_date != "" and end_date != "":
            # executes query
            query = 'SELECT SUM(sold_price IN( SELECT sold_price \
                                                    FROM ticket\
                                                    WHERE purchase_date_and_time > start_date \
                                                        AND end_date < end_date))'
            cursor.execute(query, (start_date, end_date))
        else:
            error = "You're missing information required to track your spending"

    if queried:
        # stores the results in a variable
        data = cursor.fetchall()
        cursor.close()
        if data:
            print("Data:", data)
            return render_template('customer.html', flights=data)
        else:
            # Gets all available flights
            cursor = conn.cursor()
            query = 'SELECT * FROM flight'
            cursor.execute(query)
            data1 = cursor.fetchall()

            # View My flights:
            query = "SELECT * FROM ticket WHERE customer_email = (SELECT email \
                                            FROM customer \
                                            WHERE customer_email = %s);"
            cursor.execute(query, (session['username']))
            data2 = cursor.fetchall()
            cursor.close()
            error = "We were unable to perform the operation you've requested due to incorrect or incomplete data, " \
                    "please try again. "
            return render_template('customer.html', error=error, flights=data1, myflights=data2)
    else:
        # Gets all available flights
        cursor = conn.cursor()
        query = 'SELECT * FROM flight'
        cursor.execute(query)
        data1 = cursor.fetchall()

        # View My flights:
        query = "SELECT * FROM ticket WHERE customer_email = (SELECT email \
                                        FROM customer \
                                        WHERE customer_email = %s);"
        cursor.execute(query, (session['username']))
        data2 = cursor.fetchall()
        cursor.close()
        return render_template('customer.html', error=error, flights=data1, myflights=data2)

@app.route('/airlinestaffAuth', methods=['GET', 'POST'])
def airlinestaffAuth():
    username = session['username']

    airline = request.form['airline']
    flight_number = request.form['flight_number']
    departure_date_and_time = request.form['departure_date_and_time']
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    arrival_date_and_time = request.form['arrival_date_and_time']
    base_price = request.form['base_price']
    ID_num = request.form['ID_num']
    number_of_seats = request.form['number_of_seats']
    manufacturing_company = request.form['manufacturing_company']
    age = request.form['age']
    airport_name = request.form['airport_name']
    city = request.form['city']
    country = request.form['country']
    airport_type = request.form['airport_type']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    todays_date = request.form['todays_date']
    status = request.form['status']
    
    # cursor used to send queries
    cursor = conn.cursor()
    queried = False

    #View flights:
    query = "SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, " \
                "arrival_date_and_time, base_price, ID_num FROM ticket, \
            WHERE stuff_email = (SELECT email \
                                    FROM stuff \
                                    WHERE username = %s);"
    cursor.execute(query, (username))


    # If Create new flights: is filled:
    if airline != "" and flight_number != "" and departure_airport != "" and departure_date_and_time != "" \
        and arrival_airport != ""and arrival_date_and_time != ""and base_price != "" \
        and ID_num != "":
        # executes query
        query = "INSERT INTO flight (airline, flight_number, departure_airport, \
                 departure_date_and_time, arrival_airport, arrival_date_and_time, base_price, ID_num) \
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s');"
        cursor.execute(query, (airline, flight_number, departure_airport, departure_date_and_time, \
                                arrival_airport, arrival_date_and_time, base_price, ID_num))
        queried = True


    # If Change Status of flights: is filled:
    if airline != "" and flight_number != "" and status != "":
        # executes query
        query = "UPDATE set_status \
                SET airline = %s, flight_number = %s, departure_date_and_time  = %s, the_status  = %s;"
        cursor.execute(query, (airline, flight_number, status))
        queried = True


    # If Add airplane in the system: is filled:
    if airline != "" and ID_num != "" and number_of_seats != "" and manufacturing_company != "" and age != "":
        # executes query
        query = "INSERT INTO airplane (airline, ID_num, number_of_seats, manufacturing_company, age) \
                VALUES ('%s', '%s', '%s', '%s', '%s');"
        cursor.execute(query, (airline, ID_num, number_of_seats, manufacturing_company, age))
        queried = True


    # If Add new airport in the system: is filled:
    if airport_name != "" and city != "" and country != "":
        # executes query
        query = "INSERT INTO airport (name, city, country) \
                VALUES ('%s', '%s', '%s');"
        cursor.execute(query, (airport_name, city, country))

        query = "INSERT INTO airport_type (name, airport_type) \
                VALUES ('%s', '%s');"
        cursor.execute(query, (airport_name, airport_type))
        queried = True


    # If View flight ratings: is filled:
    if airline != "" and flight_number != "" and departure_date_and_time != "":
        # executes query
        # Airline Staff will be able to see each flight’s average ratings and all the comments
        # and ratings of that flight given by the customers.
        query = "SELECT avg(sum(rating), comment, rating \
                FROM review\
                WHERE airline = %s AND flight_number = %s AND departure_date_and_time = %s"
        cursor.execute(query, (airline, flight_number, departure_date_and_time))
        queried = True


    # If View frequent customers: is filled:
    if airline != "" and flight_number == "" and departure_date_and_time == "": # only airline is not null
        # executes query
        query = "SELECT name \
                FROM customer\
                WHERE email = (SELECT customer_email \
                                FROM ticket \
                                WHERE MAX(COUNT(airline_name = %s)))"
        cursor.execute(query, (airline))
        queried = True


    # If View reports: is filled:
    if start_date != "" and end_date == "":
        # executes query
        query = "SELECT COUNT(ticket_id) \
                FROM tickets\
                WHERE purchase_date_and_time between %s and %s"
        cursor.execute(query, (start_date, end_date))
        queried = True

    # If View Earned Revenue: is filled:
    if todays_date != "":
        # FOR Last year:
        query = "SELECT SUM(sold_price) \
                FROM tickets\
                WHERE purchase_date_and_time between DATEFROMPARTS(YEAR(%s)-1,12,31) and %s;"
                # https://stackoverflow.com/questions/73072586/getting-the-last-day-of-the-previous-year-in-sql
        cursor.execute(query, (todays_date, todays_date)) # SELECT DATEFROMPARTS(YEAR(GETDATE())-1,12,31);
        queried = True

        # FOR Last month:
        query = "SELECT SUM(sold_price) \
                FROM tickets\
                WHERE purchase_date_and_time between DATEADD(MONTH, -1, %s) and %s"
                # https://stackoverflow.com/questions/1424999/get-the-records-of-last-month-in-sql-server
        cursor.execute(query, (todays_date - 365, todays_date)) # DATEADD(MONTH, -1, @startOfCurrentMonth)
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
            return render_template('airlinestaff.html', flights=data)
        else:
            # returns an error message to the html page
            cursor = conn.cursor()
            query = 'SELECT * FROM flight'
            cursor.execute(query)
            data1 = cursor.fetchall()
            for each in data1:
                print(each)
            cursor.close()
            error = 'Incomplete or incorrect data provided'
            return render_template('airlinestaff.html', error=error, flights=data1)
    else:
        # returns an error message to the html page
        cursor = conn.cursor()
        query = 'SELECT * FROM flight'
        cursor.execute(query)
        data1 = cursor.fetchall()
        for each in data1:
            print(each)
        cursor.close()
        error = 'Incomplete or incorrect data provided'
        return render_template('airlinestaff.html', error=error, flights=data1)



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
