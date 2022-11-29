create table Airport (
    name varchar(20) not null,
    city varchar(20),
    country varchar(20),

    primary key (name)
);

create table Airport_type (
    name varchar(20) not null,
    airport_type varchar(20),

    primary key (name),
    foreign key (name) references Airport(name)
);

create table Airline (
    airline_name varchar(20) not null,

    primary key (airline_name)
);

create table Operates_in (
    airport_name varchar(20) not null,
    airline_name varchar(20) not null,

    primary key (airport_name, airline_name),
    foreign key (airport_name) references Airport(name),
    foreign key (airline_name) references Airline(airline_name)
);

create table Airplane (
    airline varchar(20) not null,
    ID_num int(20) not null,
    number_of_seats int(5),
    manufacturing_company varchar(20),
    age int(5),

    primary key (airline, ID_num)
);

create table Owns (
    airline_name varchar(20) not null,
    airline varchar(20) not null,
    ID_num int(20) not null,

    primary key (airline_name, airline, ID_num),
    foreign key (airline_name) references Airline(airline_name),
    foreign key (airline, ID_num) references Airplane(airline, ID_num)
);

create table Ticket (
    ticket_id int(20) not null,
    customer_email varchar(40),
    airline_name varchar(20),
    flight_number int(20),
    sold_price int(10),

    card_type varchar(10),
    card_num int(20),
    card_name varchar(10),
    expiration_date int(10),
    purchase_date_and_time datetime(1),

    primary key (ticket_id)
);

create table Issued_by (
    ticket_id int(20) not null,
    airline_name varchar(20) not null,

    primary key (ticket_id, airline_name),
    foreign key (ticket_id) references Ticket(ticket_id),
    foreign key (airline_name) references Airplane(airline)
);

create table Flight (
    airline varchar(20) not null,
    flight_number int(10) not null,
    departure_airport varchar(10),
    departure_date_and_time datetime(1) not null,
    arrival_airport varchar(10),
    arrival_date_and_time datetime(1),
    base_price int(10),
    ID_num int(10),

    primary key (airline, flight_number, departure_date_and_time)
);

create table Hosts (
    airline_name varchar(20) not null,
    flight_number int(10) not null,
    departure_date_and_time datetime(1) not null,
    airline varchar(20) not null,

    primary key (airline_name, flight_number, departure_date_and_time, airline),
    foreign key (airline_name) references Airline(airline_name),
    foreign key (airline, flight_number, departure_date_and_time) references Flight(airline, flight_number, departure_date_and_time)
);

create table Customer (
    name varchar(20),
    email varchar(20) not null,
    password varchar(30),
    building_name varchar(10),
    street varchar(10),
    city varchar(10),
    state varchar(10),
    phone_num int(20),
    passport_num varchar(20),
    passport_expiration int(10),
    passport_country varchar(10),
    date_of_birth int(10),

    primary key (email)
);

create table Review (
    email varchar(20) not null,
    airline varchar(20) not null,
    flight_number int(10) not null,
    departure_date_and_time datetime(1) not null,
    rating int(10),
    comment varchar(1000),

    primary key (email, airline, flight_number, departure_date_and_time),
    foreign key (email) references Customer(email),
    foreign key (airline, flight_number, departure_date_and_time) references Flight(airline, flight_number, departure_date_and_time)
);

create table View_info (
    email varchar(20) not null,
    airline varchar(20) not null,
    flight_number int(10) not null,
    departure_date_and_time datetime(1) not null,

    primary key (email, airline, flight_number, departure_date_and_time)
);

create table Past_flights (
    email varchar(20) not null,
    airline varchar(20) not null,
    flight_number int(10) not null,
    departure_date_and_time datetime(1) not null,
    past_flight varchar(10),

    primary key (email, airline, flight_number, departure_date_and_time)
);

create table Future_flights (
    email varchar(20) not null,
    airline varchar(20) not null,
    flight_number int(10) not null,
    departure_date_and_time datetime(1) not null,
    future_flight varchar(10),

    primary key (email, airline, flight_number, departure_date_and_time)
);

create table Orders (
    ticket_id int(20) not null,
    email varchar(20) not null,

    primary key (ticket_id, email),
    foreign key (ticket_id) references Ticket(ticket_id),
    foreign key (email) references Customer(email)
);

create table Airline_staff (
    username varchar(20) not null,
    password varchar(20),
    first_name varchar(10),
    last_name varchar(10),
    date_of_birth int(10),
    airline_name varchar(20) not null,

    primary key (username)
);

create table Phone_number (
    username varchar(20) not null,
    phone_number int(20),

    primary key (username),
    foreign key (username) references Airline_staff(username)
);

create table Email_address (
    username varchar(20) not null,
    email_address varchar(20),

    primary key (username),
    foreign key (username) references Airline_staff(username)
);

create table Works_for (
    username varchar(20) not null,
    airline_name varchar(20) not null,

    primary key (username, airline_name),
    foreign key (username) references Airline_staff(username),
    foreign key (airline_name) references Airline(airline_name)
);

create table Add_plane (
    username varchar(20) not null,
    airline varchar(20) not null,
    ID_num int(20) not null,

    primary key (username, airline, ID_num),
    foreign key (username) references Airline_staff(username),
    foreign key (airline, ID_num) references Airplane(airline, ID_num)
);

create table Set_status (
    username varchar(20) not null,
    airline varchar(20) not null,
    flight_number int(10) not null,
    departure_date_and_time datetime(1) not null,
    the_status varchar(10),

    primary key (username, airline, flight_number, departure_date_and_time),
    foreign key (username) references Airline_staff(username),
    foreign key (airline) references Airplane(airline)
);