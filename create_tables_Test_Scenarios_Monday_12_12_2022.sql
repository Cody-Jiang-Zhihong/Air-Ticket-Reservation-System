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

    primary key (airline, ID_num, number_of_seats, manufacturing_company, age )
);

create table Owns (
    airline_name varchar(20) not null,
    airline varchar(20) not null,
    ID_num int(20) not null,

    primary key (airline_name, airline, ID_num),
    foreign key (airline_name) references Airline(airline_name),
    foreign key (airline, ID_num) references Airplane(airline, ID_num)
);

create table Flight (
    airline varchar(20) not null,
    flight_number int(10) not null,
    airplane_id_num int(20) not null,
    departure_airport varchar(10),
    departure_date_and_time datetime(1) not null,
    arrival_airport varchar(10),
    arrival_date_and_time datetime(1),
    base_price int(10),

    primary key (airline, flight_number, departure_date_and_time)
);

create table Ticket (
    ticket_id int(20) not null,
    customer_email varchar(40),
    airline varchar(20) not null,
    flight_number int(10) not null,
    sold_price int(10),
    departure_date_and_time datetime(1) not null,

    card_type varchar(10),
    card_num varchar(30),
    name_on_card varchar(30),
    expiration_date datetime(1),
    purchase_date_and_time datetime(1)

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
    password varchar(32),
    building_name varchar(10),
    street varchar(10),
    city varchar(10),
    state varchar(10),
    phone_num int(20),
    passport_num varchar(20),
    passport_expiration datetime(1),
    passport_country varchar(10),
    date_of_birth datetime(1),

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

create table Airline_staff (
    username varchar(20) not null,
    password varchar(32),
    first_name varchar(10),
    last_name varchar(10),
    date_of_birth datetime(1),
    airline_name varchar(20) not null,

    primary key (username)
);

create table Phone_number (
    username varchar(20) not null,
    phone_number varchar(20),

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
    number_of_seats int(10) not null,
    manufacturing_company varchar(20) not null,
    age int(5) not null,

    primary key (username, airline, ID_num),
    foreign key (username) references Airline_staff(username),
    foreign key (airline, ID_num, number_of_seats, manufacturing_company, age) 
                       references Airplane(airline, ID_num, number_of_seats, manufacturing_company, age)
);

create table Set_status (
    username varchar(20) not null,
    airline varchar(20) not null,
    flight_number int(10) not null,
    departure_date_and_time datetime(1) not null,
    arrival_date_and_time datetime(1) not null,
    the_status varchar(10),

    primary key (username, airline, flight_number, departure_date_and_time),
    foreign key (username) references Airline_staff(username),
    foreign key (airline) references Airplane(airline)
);