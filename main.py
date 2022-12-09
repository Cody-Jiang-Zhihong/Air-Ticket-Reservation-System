# Import Flask Library
import random

from flask import Flask, render_template, request, session, url_for, redirect
import requests
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
    query = 'SELECT * FROM flight WHERE departure_date_and_time > CURRENT_DATE()'
    cursor.execute(query)
    data1 = cursor.fetchall()
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
    # Get session username
    username = session['username']

    # Gets all available flights
    cursor = conn.cursor()
    query = 'SELECT * FROM flight WHERE departure_date_and_time > CURRENT_DATE()'
    cursor.execute(query)
    all_flights = cursor.fetchall()

    # View My flights:
    query = "SELECT ticket.airline, ticket.flight_number, departure_airport, ticket.departure_date_and_time, arrival_airport, arrival_date_and_time, base_price, ID_num FROM flight, ticket WHERE customer_email = %s AND flight.airline = ticket.airline AND flight.flight_number = ticket.flight_number AND flight.departure_date_and_time = ticket.departure_date_and_time;"
    cursor.execute(query, (username))
    myflights = cursor.fetchall()

    # Get last 6 month spending data
    query = "SELECT SUM(ticket.sold_price) as total_spend, MONTH (ticket.purchase_date_and_time) AS Month FROM " \
            "ticket, customer WHERE customer.email = %s AND customer.email = ticket.customer_email AND " \
            "ticket.purchase_date_and_time between CURRENT_DATE() - INTERVAL 6 MONTH and CURRENT_DATE() GROUP BY " \
            "Month desc; "
    cursor.execute(query, (username))
    monthly_spending = cursor.fetchall()

    # Get last year spending data
    query = "SELECT SUM(ticket.sold_price) AS last_year_spending FROM ticket, customer WHERE customer.email = %s " \
            "AND customer.email = ticket.customer_email AND purchase_date_and_time between CURRENT_DATE() - INTERVAL " \
            "1 YEAR and CURRENT_DATE(); "
    cursor.execute(query, (username))
    last_year_spending = cursor.fetchall()
    if last_year_spending:
        last_year_spending = str(last_year_spending).replace("[{'last_year_spending': Decimal('", "").replace("')}]", "")
    else:
        last_year_spending = 0
    cursor.close()

    return render_template('customer.html', last_year_spending=last_year_spending, monthly_spending=monthly_spending, flights=all_flights, myflights=myflights)

# Define route for AirlineStuff
@app.route('/airlinestaff/')
def airlinestaff():
    # All airplanes owned by
    cursor = conn.cursor()
    query = "SELECT * FROM airplane WHERE airline = (SELECT airline_name FROM airline_staff WHERE username = %s)"
    cursor.execute(query, (session['username']))
    airplanes = cursor.fetchall()

    # All flights operated by x
    query = "SELECT * FROM flight WHERE airline = (SELECT airline_name FROM airline_staff WHERE username = %s)"
    cursor.execute(query, (session['username']))
    myflights = cursor.fetchall()

    # Get last month revenue
    query = "SELECT SUM(sold_price) as Earned_Revenue FROM ticket WHERE purchase_date_and_time between (CURRENT_DATE(" \
            ") - INTERVAL 1 MONTH) and CURRENT_DATE() "
    cursor.execute(query)
    last_month_revenue = cursor.fetchall()

    if last_month_revenue is not None:
        last_month_revenue = str(last_month_revenue).replace("[{'Earned_Revenue': Decimal('", "").replace("')}]", "")
    else:
        last_month_revenue = 0

    # Get last year revenue
    query = "SELECT SUM(sold_price) as Earned_Revenue FROM ticket WHERE purchase_date_and_time between (CURRENT_DATE(" \
            ") - INTERVAL 1 YEAR) and CURRENT_DATE() "
    cursor.execute(query)
    last_year_revenue = cursor.fetchall()

    if last_year_revenue is not None:
        last_year_revenue = str(last_month_revenue).replace("[{'Earned_Revenue': Decimal('", "").replace("')}]", "")
    else:
        last_year_revenue = 0

    cursor.close()
    return render_template('airlinestaff.html', last_year_revenue=last_year_revenue, last_month_revenue=last_month_revenue, myflights=myflights, airplanes=airplanes)

# Authenticates the view flights
@app.route('/viewFlightsAuth', methods=['GET', 'POST'])
def viewFlightsAuth():
    if not 'check_status' in request.form:
        # grabs information from the forms
        source_city = request.form['source_city']
        destination_city = request.form['destination_city']

        airport_name1 = request.form['airport_name1']
        airport_name2 = request.form['airport_name2']

        departure_date = request.form['departure_date']
        arrival_date = request.form['arrival_date']

    # cursor used to send queries
    cursor = conn.cursor()
    queried = False

    # If show all is pressed
    if 'show_all' in request.form:
        query = query = 'SELECT * FROM flight WHERE departure_date_and_time > CURRENT_DATE()'
        cursor.execute(query)
        data1 = cursor.fetchall()
        cursor.close()
        return render_template('index.html', flights=data1)

    # If given 2 cities
    if 'one_way' in request.form:
        if source_city != "" and destination_city != "":
            # executes query
            query = "SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, " \
                    "arrival_date_and_time, base_price, ID_num  FROM flight WHERE departure_airport = (SELECT name FROM " \
                    "airport WHERE city = %s) AND arrival_airport = (SELECT name FROM airport WHERE city = %s) AND departure_date_and_time > CURRENT_DATE()"
            cursor.execute(query, (source_city, destination_city))
            queried = True
        # If given 2 airports
        elif airport_name1 != "" and airport_name2 != "":
            # executes query
            query = "SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, " \
                    "arrival_date_and_time, base_price, ID_num  FROM flight WHERE departure_airport = %s AND " \
                    "arrival_airport = %s AND departure_date_and_time > CURRENT_DATE()";
            cursor.execute(query, (airport_name1, airport_name2))
            queried = True
    # round trip 2 airports
    if 'round_trip' in request.form:
        if airport_name1 != "" and airport_name2 != "" and departure_date != "" and arrival_date != "":
            # executes query
            query = 'SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, ' \
                    'arrival_date_and_time, base_price, ID_num  FROM flight WHERE departure_airport = %s AND ' \
                    'arrival_airport = %s AND departure_date_and_time = %s AND departure_date_and_time > CURRENT_DATE();'
            cursor.execute(query, (airport_name1, airport_name2, departure_date))
            result1 = cursor.fetchall()

            query = 'SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, ' \
                    'arrival_date_and_time, base_price, ID_num  FROM flight WHERE departure_airport = %s AND ' \
                    'arrival_airport = %s AND departure_date_and_time = %s AND departure_date_and_time > CURRENT_DATE();'
            cursor.execute(query, (airport_name2, airport_name1, arrival_date))
            result2 = cursor.fetchall()
            return render_template('index.html', result1=result1, result2=result2)

    if 'check_status' in request.form:
        status_airline_name = request.form['status_airline_name']
        status_flight_number = request.form['status_flight_number']
        status_departure = request.form['status_departure']
        status_arrival = request.form['status_arrival']

        if status_departure:
            query = "SELECT the_status FROM set_status WHERE airline = %s AND flight_number = %s AND departure_date_and_time = %s"
            cursor.execute(query, (status_airline_name, status_flight_number, status_departure))
        else:
            query = "SELECT the_status FROM set_status WHERE airline = %s AND flight_number = %s AND arrival_date_and_time = %s"
            cursor.execute(query, (status_airline_name, status_flight_number, status_arrival))

        status = cursor.fetchall()

        if status:
            status = str(status).replace("[{'the_status': '", "").replace("'}]", "")
        else:
            status = None

        query = 'SELECT * FROM flight WHERE departure_date_and_time > CURRENT_DATE()'
        cursor.execute(query)
        data1 = cursor.fetchall()
        cursor.close()
        return render_template('index.html', flights=data1, status=status)

    if queried:
        # stores the results in a variable
        data = cursor.fetchall()
        # use fetchall() if you are expecting more than 1 data row
        cursor.close()
        error = None
        if data:
            return render_template('index.html', flights=data)
        else:
            # returns an error message to the html page
            cursor = conn.cursor()
            query = 'SELECT * FROM flight WHERE departure_date_and_time > CURRENT_DATE()'
            cursor.execute(query)
            data1 = cursor.fetchall()
            cursor.close()
            error = 'Incomplete or incorrect data provided'
            return render_template('index.html', error=error, flights=data1)
    else:
        # returns an error message to the html page
        cursor = conn.cursor()
        query = 'SELECT * FROM flight WHERE departure_date_and_time > CURRENT_DATE()'
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

# Handles customer use cases
@app.route('/customerAuth', methods=['GET', 'POST'])
def customerAuth():
    username = session['username']
    # cursor used to send queries
    cursor = conn.cursor()
    error = None
    queried = False

    query = 'SELECT * FROM flight WHERE departure_date_and_time > CURRENT_DATE()'
    cursor.execute(query)
    old_ticket_data = cursor.fetchall()
    cursor.close()

    cursor = conn.cursor()

    success = None

    # Search for flights function
    if 'search' in request.form:
        # grabs information from the forms
        source_city = request.form['source_city']
        destination_city = request.form['destination_city']

        airport_name1 = request.form['airport_name1']
        airport_name2 = request.form['airport_name2']

        departure_date = request.form['departure_date']
        arrival_date = request.form['arrival_date']

        # cursor used to send queries
        cursor = conn.cursor()
        queried = False

        # If show all is pressed
        if 'show_all' in request.form:
            query = 'SELECT * FROM flight WHERE departure_date_and_time > CURRENT_DATE()'
            cursor.execute(query)
            data1 = cursor.fetchall()
            cursor.close()
            return render_template('index.html', flights=data1)

        # If given 2 cities
        if 'one_way' in request.form:
            if source_city != "" and destination_city != "":
                # executes query
                query = "SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, " \
                        "arrival_date_and_time, base_price, ID_num  FROM flight WHERE departure_airport = (SELECT name FROM " \
                        "airport WHERE city = %s) AND arrival_airport = (SELECT name FROM airport WHERE city = %s) AND departure_date_and_time > CURRENT_DATE()"
                cursor.execute(query, (source_city, destination_city))
                queried = True
            # If given 2 airports
            elif airport_name1 != "" and airport_name2 != "":
                # executes query
                query = "SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, " \
                        "arrival_date_and_time, base_price, ID_num  FROM flight WHERE departure_airport = %s AND " \
                        "arrival_airport = %s AND departure_date_and_time > CURRENT_DATE()";
                cursor.execute(query, (airport_name1, airport_name2))
                queried = True
        # round trip 2 airports
        if 'round_trip' in request.form:
            if airport_name1 != "" and airport_name2 != "" and departure_date != "" and arrival_date != "":
                # executes query
                query = 'SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, ' \
                        'arrival_date_and_time, base_price, ID_num  FROM flight WHERE departure_airport = %s AND ' \
                        'arrival_airport = %s AND departure_date_and_time = %s AND departure_date_and_time > CURRENT_DATE();'
                cursor.execute(query, (airport_name1, airport_name2, departure_date))
                result1 = cursor.fetchall()

                query = 'SELECT airline, flight_number, departure_airport, departure_date_and_time, arrival_airport, ' \
                        'arrival_date_and_time, base_price, ID_num  FROM flight WHERE departure_airport = %s AND ' \
                        'arrival_airport = %s AND departure_date_and_time = %s AND departure_date_and_time > CURRENT_DATE();'
                cursor.execute(query, (airport_name2, airport_name1, arrival_date))
                result2 = cursor.fetchall()
                return render_template('index.html', result1=result1, result2=result2)

    # Purchasing ticket
    if 'purchase' in request.form:
        airline = request.form['p_airline']
        flight_number = request.form['p_flight_number']
        departure_date = request.form['p_departure_date']

        card_type = request.form['card_type']
        card_num = request.form['card_num']
        card_name = request.form['card_name']
        expiration_date = request.form['expiration_date']
        purchase_data = [airline, flight_number, departure_date, card_type, card_num, card_name, expiration_date]

        if None not in purchase_data:
            # Update the ticket with all this data
            query = "INSERT INTO ticket (ticket_id, customer_email, airline, flight_number, sold_price, departure_date_and_time, card_type, card_num, card_name, expiration_date, purchase_date_and_time) SELECT DISTINCT '', %s, %s, %s, flight.base_price, %s, %s, %s, %s, %s, CURRENT_DATE() FROM flight, airplane, ticket WHERE (SELECT COUNT(ticket.ticket_id) as seats_reserved FROM flight, ticket, airplane WHERE ticket.flight_number = %s AND flight.flight_number = ticket.flight_number AND flight.airplane_id_num = airplane.ID_num) < (0.6 * (SELECT DISTINCT airplane.number_of_seats FROM flight, ticket, airplane WHERE ticket.flight_number = %s AND flight.flight_number = ticket.flight_number AND flight.airplane_id_num = airplane.ID_num)) AND flight.flight_number = %s AND flight.airplane_id_num = airplane.ID_num;"
            cursor.execute(query, (username, airline, flight_number, departure_date, card_type, card_num, card_name,  expiration_date, flight_number, flight_number, flight_number))
            conn.commit()

            # Part 2
            query = "INSERT INTO ticket (ticket_id, customer_email, airline, flight_number, sold_price, departure_date_and_time, card_type, card_num, card_name, expiration_date, purchase_date_and_time) SELECT DISTINCT '', '', %s, %s, 1.25 * flight.base_price, %s, %s, %s, %s, %s, %s FROM flight, airplane, ticket WHERE (SELECT COUNT(ticket.ticket_id) as seats_reserved FROM flight, ticket, airplane WHERE ticket.flight_number = %s AND flight.flight_number = ticket.flight_number AND flight.airplane_id_num = airplane.ID_num) >= (0.6 * (SELECT DISTINCT airplane.number_of_seats FROM flight, ticket, airplane WHERE ticket.flight_number = '123' AND flight.flight_number = ticket.flight_number AND flight.airplane_id_num = airplane.ID_num)) AND flight.flight_number = %s AND flight.airplane_id_num = airplane.ID_num;"
            cursor.execute(query, (username, airline, flight_number, departure_date, card_type, card_num, card_name, expiration_date, flight_number, flight_number, flight_number))
            conn.commit()

        else:
            error = "Missing information to purchase a flight"

    # Canceling ticket
    if 'cancel' in request.form:
        airline = request.form['p_airline']
        flight_number = request.form['p_flight_number']
        departure_date = request.form['p_departure_date']

        if airline != "" and flight_number != "" and departure_date != "":
            query = "DELETE FROM ticket WHERE customer_email = %s AND airline = %s AND flight_number = %s AND departure_date_and_time = %s"
            cursor.execute(query, (username, airline, flight_number, departure_date))
            conn.commit()
            queried = True
        else:
            error = "Missing information to cancel a ticket"

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
                # Checks to see if flight exists
                cursor = conn.cursor()
                query = 'SELECT * FROM flight natural join ticket WHERE customer_email = %s AND flight.airline = ticket.airline AND flight.flight_number = ticket.flight_number AND flight.departure_date_and_time = ticket.departure_date_and_time AND flight.departure_date_and_time < CURRENT_DATE()'
                cursor.execute(query, (airline, flight_number, departure_date))
                flight_data = cursor.fetchall()
                # If the flight exists, we execute the query
                if flight_data:
                    # Checks to see if there's already a review on the flight
                    cursor = conn.cursor()
                    query = 'SELECT * FROM ticket WHERE airline = %s AND flight_number = %s AND departure_date_and_time = %s'
                    cursor.execute(query, (airline, flight_number, departure_date))
                    review_exists = cursor.fetchall()
                    cursor.close()

                    cursor = conn.cursor()
                    if review_exists:
                        query = "UPDATE review SET email=%s, airline=%s, flight_number=%s, " \
                                "departure_date_and_time=%s, rating=%s, comment=%s WHERE airline=%s AND " \
                                "flight_number=%s AND departure_date_and_time=%s "
                        cursor.execute(query, (username, airline, flight_number, departure_date, rating, review, airline, flight_number, departure_date))
                        queried = True
                        success = "Successfully updated a review"
                    else:
                        query = "INSERT INTO review VALUES(%s, %s, %s, %s, %s, %s)"
                        cursor.execute(query, (username, airline, flight_number, departure_date, rating, review))
                        queried = True
                        success = "Successfully submitted a review"
                    conn.commit()
                else:
                    error = "Flight either does not exist or has not happened yet"
            else:
                error = "You're missing either the rating or the comment in order to submit a review"
        else:
            error = "You're missing information required to find the flight in order to submit a review"

    # Track my spending
    if 'track' in request.form:
        start_date = request.form['date_start']
        end_date = request.form['date_end']

        # If Track My Spending: is filled
        if start_date != "" and end_date != "":
            # Get last 6 month spending data
            query = "SELECT SUM(ticket.sold_price) as total_spend, MONTH (ticket.purchase_date_and_time) AS Month FROM " \
                    "ticket, customer WHERE customer.email = %s AND customer.email = ticket.customer_email AND " \
                    "ticket.purchase_date_and_time between %s and %s GROUP BY " \
                    "Month desc; "
            cursor.execute(query, (username, start_date, end_date))
            range_spending = cursor.fetchall()

            # Gets all available flights
            cursor = conn.cursor()
            query = 'SELECT * FROM flight WHERE departure_date_and_time > CURRENT_DATE()'
            cursor.execute(query)
            all_flights = cursor.fetchall()

            # View My flights:
            query = "SELECT ticket.airline, ticket.flight_number, departure_airport, ticket.departure_date_and_time, arrival_airport, arrival_date_and_time, base_price, ID_num FROM flight, ticket WHERE customer_email = %s AND flight.airline = ticket.airline AND flight.flight_number = ticket.flight_number AND flight.departure_date_and_time = ticket.departure_date_and_time;"
            cursor.execute(query, (username))
            myflights = cursor.fetchall()

            # Get last 6 month spending data
            query = "SELECT SUM(ticket.sold_price) as total_spend, MONTH (ticket.purchase_date_and_time) AS Month FROM " \
                    "ticket, customer WHERE customer.email = %s AND customer.email = ticket.customer_email AND " \
                    "ticket.purchase_date_and_time between CURRENT_DATE() - INTERVAL 6 MONTH and CURRENT_DATE() GROUP BY " \
                    "Month desc; "
            cursor.execute(query, (username))
            monthly_spending = cursor.fetchall()

            # Get last year spending data
            query = "SELECT SUM(ticket.sold_price) AS last_year_spending FROM ticket, customer WHERE customer.email = %s " \
                    "AND customer.email = ticket.customer_email AND purchase_date_and_time between CURRENT_DATE() - INTERVAL " \
                    "1 YEAR and CURRENT_DATE(); "
            cursor.execute(query, (username))
            last_year_spending = cursor.fetchall()
            if last_year_spending:
                last_year_spending = str(last_year_spending).replace("[{'last_year_spending': Decimal('", "").replace(
                    "')}]", "")
            else:
                last_year_spending = 0
            cursor.close()

            return render_template('customer.html', range_spending=range_spending, last_year_spending=last_year_spending,
                                   monthly_spending=monthly_spending, flights=all_flights, myflights=myflights)
        else:
            error = "You're missing information required to track your spending"

    if queried:
        # Execute and get data from prev initialized query
        res = requests.get('http://127.0.0.1:5000/', verify=False)
        # stores the results in a variable
        data = cursor.fetchall()
        conn.commit()
        cursor.close()

        # Get new ticket data
        cursor = conn.cursor()
        query = 'SELECT * FROM ticket'
        cursor.execute(query)
        new_ticket_data = cursor.fetchall()
        cursor.close()

        if not data:
            # No more available tickets
            if res.status_code == 200 and old_ticket_data == new_ticket_data:
                if 'cancel' in request.form:
                    error = "You haven't purchased the ticket you're trying to cancel"
        else:
            # Gets all available flights
            cursor = conn.cursor()
            query = 'SELECT * FROM flight WHERE departure_date_and_time > CURRENT_DATE()'
            cursor.execute(query)
            all_flights = cursor.fetchall()

            # View My flights:
            query = "SELECT ticket.airline, ticket.flight_number, departure_airport, ticket.departure_date_and_time, arrival_airport, arrival_date_and_time, base_price, ID_num FROM flight, ticket WHERE customer_email = %s AND flight.airline = ticket.airline AND flight.flight_number = ticket.flight_number AND flight.departure_date_and_time = ticket.departure_date_and_time;"
            cursor.execute(query, (username))
            myflights = cursor.fetchall()

            # Get last 6 month spending data
            query = "SELECT SUM(ticket.sold_price) as total_spend, MONTH (ticket.purchase_date_and_time) AS Month FROM " \
                    "ticket, customer WHERE customer.email = %s AND customer.email = ticket.customer_email AND " \
                    "ticket.purchase_date_and_time between CURRENT_DATE() - INTERVAL 6 MONTH and CURRENT_DATE() GROUP BY " \
                    "Month desc; "
            cursor.execute(query, (username))
            monthly_spending = cursor.fetchall()

            # Get last year spending data
            query = "SELECT SUM(ticket.sold_price) AS last_year_spending FROM ticket, customer WHERE customer.email = %s " \
                    "AND customer.email = ticket.customer_email AND purchase_date_and_time between CURRENT_DATE() - INTERVAL " \
                    "1 YEAR and CURRENT_DATE(); "
            cursor.execute(query, (username))
            last_year_spending = cursor.fetchall()
            if last_year_spending:
                last_year_spending = str(last_year_spending).replace("[{'last_year_spending': Decimal('", "").replace(
                    "')}]", "")
            else:
                last_year_spending = 0
            cursor.close()

            return render_template('customer.html', last_year_spending=last_year_spending,
                                   monthly_spending=monthly_spending, flights=all_flights, myflights=myflights)

        # Gets all available flights
        cursor = conn.cursor()
        query = 'SELECT * FROM flight WHERE departure_date_and_time > CURRENT_DATE()'
        cursor.execute(query)
        all_flights = cursor.fetchall()

        # View My flights:
        query = "SELECT ticket.airline, ticket.flight_number, departure_airport, ticket.departure_date_and_time, arrival_airport, arrival_date_and_time, base_price, ID_num FROM flight, ticket WHERE customer_email = %s AND flight.airline = ticket.airline AND flight.flight_number = ticket.flight_number AND flight.departure_date_and_time = ticket.departure_date_and_time;"
        cursor.execute(query, (username))
        myflights = cursor.fetchall()

        # Get last 6 month spending data
        query = "SELECT SUM(ticket.sold_price) as total_spend, MONTH (ticket.purchase_date_and_time) AS Month FROM " \
                "ticket, customer WHERE customer.email = %s AND customer.email = ticket.customer_email AND " \
                "ticket.purchase_date_and_time between CURRENT_DATE() - INTERVAL 6 MONTH and CURRENT_DATE() GROUP BY " \
                "Month desc;"
        cursor.execute(query, (username))
        monthly_spending = cursor.fetchall()

        # Get last year spending data
        query = "SELECT SUM(ticket.sold_price) AS last_year_spending FROM ticket, customer WHERE customer.email = %s " \
                "AND customer.email = ticket.customer_email AND purchase_date_and_time between CURRENT_DATE() - INTERVAL " \
                "1 YEAR and CURRENT_DATE();"
        cursor.execute(query, (username))
        last_year_spending = cursor.fetchall()
        if last_year_spending:
            last_year_spending = str(last_year_spending).replace("[{'last_year_spending': Decimal('", "").replace(
                "')}]", "")
        else:
            last_year_spending = 0
        cursor.close()

        return render_template('customer.html', last_year_spending=last_year_spending,
                               monthly_spending=monthly_spending, flights=all_flights, myflights=myflights)

# Handles airline staff use cases
@app.route('/airlinestaffAuth', methods=['GET', 'POST'])
def airlinestaffAuth():
    username = session['username']
    error = None

    create_new_flights = []

    # For creating a new flight
    if 'create_new_flights' in request.form:
        airline = request.form['airline']
        flight_number = request.form['flight_number']
        departure_date_and_time = request.form['departure_date_and_time']
        departure_airport = request.form['departure_airport']
        arrival_airport = request.form['arrival_airport']
        arrival_date_and_time = request.form['arrival_date_and_time']
        base_price = request.form['base_price']
        id_num = request.form['ID_num']
        create_new_flights = [airline, flight_number, departure_date_and_time, departure_airport, arrival_airport,
                              arrival_date_and_time, base_price, id_num]

    # For changing status of a flight
    if 'set_status' in request.form:
        airline1 = request.form['airline1']
        flight_number1 = request.form['flight_number1']
        departure_date_and_time1 = request.form['departure_date_and_time1']
        status = request.form['status']

    # Adding airplane into system
    if 'add_airplane' in request.form:
        airline2 = request.form['airline2']
        id_num2 = request.form['ID_num2']
        number_of_seats = request.form['number_of_seats']
        manufacturing_company = request.form['manufacturing_company']
        age = request.form['age']

    # Adding airport into system
    if 'add_airport' in request.form:
        airport_name = request.form['airport_name']
        city = request.form['city']
        country = request.form['country']
        airport_type = request.form['airport_type']

    # View flight rating
    if 'view_ratings' in request.form:
        airline3 = request.form['airline3']
        flight_number3 = request.form['flight_number3']
        departure_date_and_time3 = request.form['departure_date_and_time3']

    # View most frequent customer
    if 'view_most_frequent' in request.form:
        airline4 = request.form['airline4']

    # View specific customer
    if 'view_specific_customer' in request.form:
        airline5 = request.form['airline5']
        customer_email = request.form['customer_email']

    # View report
    if 'view_report' in request.form:
        start_date = request.form['start_date']
        end_date = request.form['end_date']

    # cursor used to send queries
    cursor = conn.cursor()
    queried = False

    # If Create new flights: is filled:
    if 'create_new_flights' in request.form:
        if not None in create_new_flights:
            # executes query
            query = "INSERT INTO flight (airline, flight_number, departure_airport, \
                     departure_date_and_time, arrival_airport, arrival_date_and_time, base_price, ID_num) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (airline, flight_number, departure_airport, departure_date_and_time, \
                                    arrival_airport, arrival_date_and_time, base_price, id_num))
            conn.commit()
            queried = True
            success = "Successfully created new flight"
        else :
            error = "Missing some data in creating new flights"

    # If Change Status of flights: is filled:
    if 'set_status' in request.form:
        if airline1 != "" and flight_number1 != "" and departure_date_and_time1 != "" and status != "":
            # executes query
            query = "UPDATE set_status SET the_status = %s airline = %s AND flight_number = " \
                    "%s AND departure_date_and_time = %s"
            cursor.execute(query, (status, username, airline1, flight_number1, departure_date_and_time1))
            conn.commit()
            queried = True
            success = "Successfully set status"
        else:
            error = "Missing some data in setting status"

    # If Add airplane in the system: is filled:
    if 'add_airplane' in request.form:
        if airline2 != "" and id_num2 != "" and number_of_seats != "" and manufacturing_company != "" and age != "":
            # executes query
            query = "INSERT INTO airplane (airline, ID_num, number_of_seats, manufacturing_company, age) \
                    VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (airline2, id_num2, number_of_seats, manufacturing_company, age))
            conn.commit()
            queried = True
            success = "Successfully added new airplane"
        else:
            error = "Missing some data in adding airplane"

    # If Add new airport in the system: is filled:
    if 'add_airport' in request.form:
        if airport_name != "" and city != "" and country != "" and airport_type != "":
            # executes query
            query = "INSERT INTO airport (name, city, country) \
                    VALUES (%s, %s, %s)"
            cursor.execute(query, (airport_name, city, country))
            conn.commit()

            query = "INSERT INTO airport_type (name, airport_type) \
                    VALUES (%s, %s)"
            cursor.execute(query, (airport_name, airport_type))
            conn.commit()

            success = "Successfully added new airport"
            queried = True
        else:
            error = "Missing some data in adding airport"

    # If View flight ratings: is filled:
    if 'view_ratings' in request.form:
        if airline3 != "" and flight_number3 != "" and departure_date_and_time3 != "":
            # executes query
            # Airline Staff will be able to see each flight’s average ratings and all the comments
            # and ratings of that flight given by the customers.
            query = "SELECT rating, comment FROM review WHERE airline = %s AND flight_number = %s AND departure_date_and_time = %s"
            cursor.execute(query, (airline3, flight_number3, departure_date_and_time3))
            reviews = cursor.fetchall()
            cursor.close()

            cursor = conn.cursor()
            query = "SELECT AVG(rating) FROM review WHERE airline = %s AND flight_number = %s AND departure_date_and_time = %s"
            cursor.execute(query, (airline3, flight_number3, departure_date_and_time3))
            average_rating = cursor.fetchall()
            if not None in average_rating:
                average_rating = int(float(str(average_rating).replace("[{'AVG(rating)': Decimal('", "").replace("')}]", "")))
            else:
                average_rating = "No rating"
            cursor.close()

            # All airplanes owned by
            cursor = conn.cursor()
            query = "SELECT * FROM airplane WHERE airline = (SELECT airline_name FROM airline_staff WHERE username = %s)"
            cursor.execute(query, (session['username']))
            airplanes = cursor.fetchall()

            # All flights operated by x
            query = "SELECT * FROM flight WHERE airline = (SELECT airline_name FROM airline_staff WHERE username = %s)"
            cursor.execute(query, (session['username']))
            myflights = cursor.fetchall()

            # Get last month revenue
            query = "SELECT SUM(sold_price) as Earned_Revenue FROM ticket WHERE purchase_date_and_time between (CURRENT_DATE(" \
                    ") - INTERVAL 1 MONTH) and CURRENT_DATE() "
            cursor.execute(query)
            last_month_revenue = cursor.fetchall()

            if last_month_revenue is not None:
                last_month_revenue = str(last_month_revenue).replace("[{'Earned_Revenue': Decimal('", "").replace(
                    "')}]", "")
            else:
                last_month_revenue = 0

            # Get last year revenue
            query = "SELECT SUM(sold_price) as Earned_Revenue FROM ticket WHERE purchase_date_and_time between (CURRENT_DATE(" \
                    ") - INTERVAL 1 YEAR) and CURRENT_DATE() "
            cursor.execute(query)
            last_year_revenue = cursor.fetchall()

            if last_year_revenue is not None:
                last_year_revenue = str(last_month_revenue).replace("[{'Earned_Revenue': Decimal('", "").replace("')}]",
                                                                                                                 "")
            else:
                last_year_revenue = 0

            cursor.close()
            return render_template('airlinestaff.html', last_year_revenue=last_year_revenue,
                                   last_month_revenue=last_month_revenue, myflights=myflights, airplanes=airplanes)
        else:
            error = "Missing some data in view ratings"

    # If View frequent customers: is filled:
    if 'view_most_frequent' in request.form:
        if airline4 != "":
            # executes query
            query = "SELECT customer_email FROM ticket natural join flight WHERE airline = %s GROUP BY customer_email ORDER BY COUNT(*) DESC LIMIT 1"
            cursor.execute(query, (airline4))
            data = cursor.fetchall()
            cursor.close()
            data = str(data).replace("[{'customer_email': '", "").replace("'}]", "")
            if data == "()":
                data = "There have been no customers who have flown with airline " + airline4
            else:
                data = "The most frequent customer at airline " + airline4 + " is " + data

                # All airplanes owned by
                cursor = conn.cursor()
                query = "SELECT * FROM airplane WHERE airline = (SELECT airline_name FROM airline_staff WHERE username = %s)"
                cursor.execute(query, (session['username']))
                airplanes = cursor.fetchall()

                # All flights operated by x
                query = "SELECT * FROM flight WHERE airline = (SELECT airline_name FROM airline_staff WHERE username = %s)"
                cursor.execute(query, (session['username']))
                myflights = cursor.fetchall()

                # Get last month revenue
                query = "SELECT SUM(sold_price) as Earned_Revenue FROM ticket WHERE purchase_date_and_time between (CURRENT_DATE(" \
                        ") - INTERVAL 1 MONTH) and CURRENT_DATE() "
                cursor.execute(query)
                last_month_revenue = cursor.fetchall()

                if last_month_revenue is not None:
                    last_month_revenue = str(last_month_revenue).replace("[{'Earned_Revenue': Decimal('", "").replace(
                        "')}]", "")
                else:
                    last_month_revenue = 0

                # Get last year revenue
                query = "SELECT SUM(sold_price) as Earned_Revenue FROM ticket WHERE purchase_date_and_time between (CURRENT_DATE(" \
                        ") - INTERVAL 1 YEAR) and CURRENT_DATE() "
                cursor.execute(query)
                last_year_revenue = cursor.fetchall()

                if last_year_revenue is not None:
                    last_year_revenue = str(last_month_revenue).replace("[{'Earned_Revenue': Decimal('", "").replace(
                        "')}]", "")
                else:
                    last_year_revenue = 0

                cursor.close()
                return render_template('airlinestaff.html', last_year_revenue=last_year_revenue,
                                       last_month_revenue=last_month_revenue, myflights=myflights, airplanes=airplanes)

        else:
            error = "Missing some data in viewing most frequent customer"

    # If view specific customer is filled
    if 'view_specific_customer' in request.form:
        if airline5 != "" and customer_email != "":
            cursor = conn.cursor()
            query = "SELECT DISTINCT flight.airline, flight.flight_number, flight.departure_airport, " \
                    "flight.departure_date_and_time, flight.arrival_airport, flight.arrival_date_and_time, " \
                    "flight.base_price, flight.ID_num FROM customer, ticket, flight WHERE customer.email = %s AND " \
                    "customer.email = ticket.customer_email AND ticket.airline = %s AND ticket.flight_number = flight.flight_number"
            cursor.execute(query, (customer_email, airline5))
            customer_flight = cursor.fetchall()

            # All airplanes owned by
            cursor = conn.cursor()
            query = "SELECT * FROM airplane WHERE airline = (SELECT airline_name FROM airline_staff WHERE username = %s)"
            cursor.execute(query, (session['username']))
            airplanes = cursor.fetchall()

            # All flights operated by x
            query = "SELECT * FROM flight WHERE airline = (SELECT airline_name FROM airline_staff WHERE username = %s)"
            cursor.execute(query, (session['username']))
            myflights = cursor.fetchall()

            # Get last month revenue
            query = "SELECT SUM(sold_price) as Earned_Revenue FROM ticket WHERE purchase_date_and_time between (CURRENT_DATE(" \
                    ") - INTERVAL 1 MONTH) and CURRENT_DATE() "
            cursor.execute(query)
            last_month_revenue = cursor.fetchall()

            if last_month_revenue is not None:
                last_month_revenue = str(last_month_revenue).replace("[{'Earned_Revenue': Decimal('", "").replace(
                    "')}]", "")
            else:
                last_month_revenue = 0

            # Get last year revenue
            query = "SELECT SUM(sold_price) as Earned_Revenue FROM ticket WHERE purchase_date_and_time between (CURRENT_DATE(" \
                    ") - INTERVAL 1 YEAR) and CURRENT_DATE() "
            cursor.execute(query)
            last_year_revenue = cursor.fetchall()

            if last_year_revenue is not None:
                last_year_revenue = str(last_month_revenue).replace("[{'Earned_Revenue': Decimal('", "").replace("')}]",
                                                                                                                 "")
            else:
                last_year_revenue = 0

            cursor.close()
            return render_template('airlinestaff.html', last_year_revenue=last_year_revenue,
                                   last_month_revenue=last_month_revenue, myflights=myflights, airplanes=airplanes)
        else:
            error = "Missing some data in viewing specific customer"

    # If view reports is pressed and filled
    if 'view_report' in request.form:
        if start_date != "" and end_date != "":
            cursor = conn.cursor()
            query = "SELECT COUNT(ticket_id) as amounts_of_ticket, MONTH (purchase_date_and_time) AS Month FROM " \
                    "ticket WHERE  ticket.purchase_date_and_time between %s and %s GROUP BY Month asc; "
            cursor.execute(query, (start_date, end_date))
            report_data = cursor.fetchall()

            # All airplanes owned by
            cursor = conn.cursor()
            query = "SELECT * FROM airplane WHERE airline = (SELECT airline_name FROM airline_staff WHERE username = %s)"
            cursor.execute(query, (session['username']))
            airplanes = cursor.fetchall()

            # All flights operated by x
            query = "SELECT * FROM flight WHERE airline = (SELECT airline_name FROM airline_staff WHERE username = %s)"
            cursor.execute(query, (session['username']))
            myflights = cursor.fetchall()

            # Get last month revenue
            query = "SELECT SUM(sold_price) as Earned_Revenue FROM ticket WHERE purchase_date_and_time between (CURRENT_DATE(" \
                    ") - INTERVAL 1 MONTH) and CURRENT_DATE() "
            cursor.execute(query)
            last_month_revenue = cursor.fetchall()

            if last_month_revenue is not None:
                last_month_revenue = str(last_month_revenue).replace("[{'Earned_Revenue': Decimal('", "").replace(
                    "')}]", "")
            else:
                last_month_revenue = 0

            # Get last year revenue
            query = "SELECT SUM(sold_price) as Earned_Revenue FROM ticket WHERE purchase_date_and_time between (CURRENT_DATE(" \
                    ") - INTERVAL 1 YEAR) and CURRENT_DATE() "
            cursor.execute(query)
            last_year_revenue = cursor.fetchall()

            if last_year_revenue is not None:
                last_year_revenue = str(last_month_revenue).replace("[{'Earned_Revenue': Decimal('", "").replace("')}]",
                                                                                                                 "")
            else:
                last_year_revenue = 0

            cursor.close()
            return render_template('airlinestaff.html', report=report_data, last_year_revenue=last_year_revenue,
                                   last_month_revenue=last_month_revenue, myflights=myflights, airplanes=airplanes)

    if not queried:
        error = 'Incomplete or incorrect data provided'

    # All airplanes owned by
    cursor = conn.cursor()
    query = "SELECT * FROM airplane WHERE airline = (SELECT airline_name FROM airline_staff WHERE username = %s)"
    cursor.execute(query, (session['username']))
    airplanes = cursor.fetchall()

    # All flights operated by x
    query = "SELECT * FROM flight WHERE airline = (SELECT airline_name FROM airline_staff WHERE username = %s)"
    cursor.execute(query, (session['username']))
    myflights = cursor.fetchall()

    # Get last month revenue
    query = "SELECT SUM(sold_price) as Earned_Revenue FROM ticket WHERE purchase_date_and_time between (CURRENT_DATE(" \
            ") - INTERVAL 1 MONTH) and CURRENT_DATE() "
    cursor.execute(query)
    last_month_revenue = cursor.fetchall()

    if last_month_revenue is not None:
        last_month_revenue = str(last_month_revenue).replace("[{'Earned_Revenue': Decimal('", "").replace("')}]",
                                                                                                          "")
    else:
        last_month_revenue = 0

    # Get last year revenue
    query = "SELECT SUM(sold_price) as Earned_Revenue FROM ticket WHERE purchase_date_and_time between (CURRENT_DATE(" \
            ") - INTERVAL 1 YEAR) and CURRENT_DATE() "
    cursor.execute(query)
    last_year_revenue = cursor.fetchall()

    if last_year_revenue is not None:
        last_year_revenue = str(last_month_revenue).replace("[{'Earned_Revenue': Decimal('", "").replace("')}]", "")
    else:
        last_year_revenue = 0

    cursor.close()
    if error:
        return render_template('airlinestaff.html', error=error, last_year_revenue=last_year_revenue,
                           last_month_revenue=last_month_revenue, myflights=myflights, airplanes=airplanes)
    return render_template('airlinestaff.html', last_year_revenue=last_year_revenue,
                           last_month_revenue=last_month_revenue, myflights=myflights, airplanes=airplanes)

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
