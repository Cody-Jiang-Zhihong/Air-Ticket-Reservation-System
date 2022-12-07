delete from Airport;
delete from Airport_type;
delete from Operates_in;
delete from Airline;
delete from Owns;
delete from Airplane;
delete from Issued_by;
delete from Ticket;
delete from Flight;
delete from Hosts;
delete from Review;
delete from Customer;
delete from View_info;
delete from Orders;
delete from Airline_staff;
delete from Phone_number;
delete from Email_address;
delete from Works_for;
delete from Add_plane;
delete from Set_status;

insert into Airline values ('Jet Blue');
insert into Airline values ('EVA Air');
insert into Airline values ('Nippon Airways');
insert into Airline values ('Japan Airlines');

insert into Airport values ('JFK', 'NYC', 'US');
insert into Airport values ('PVG', 'Shanghai', 'China');
insert into Airport values ('SDJ', 'Sendai', 'Japan');
insert into Airport values ('YNY', 'Yangyang', 'South Korea');

insert into Customer values ('Cody', 'zj2247@nyu.edu', MD5('12345'), '2Metrotech', 'JayST', 'Brooklyn', 'NY', '91754588', 'EA999', '2022-11-29 21:22::00.0', 'China', '2000-11-29 21:22::00.0');
insert into Customer values ('Preston', 'plt7955@nyu.edu', MD5('12345'), '2Metrotech', 'JayST', 'Brooklyn', 'NY', '12349', 'EA12345', '2022-11-29 21:22::00.0', 'US', '2000-11-29 21:22::00.0');
insert into Customer values ('Tony', 'sth1234@uyn.edu', MD5('12345'), '2Metrotech', 'JayST', 'Brooklyn', 'NY', '098765543', 'EA22222', '2022-11-29 21:22::00.0', 'US', '2000-11-29 21:22::00.0');

insert into Airplane values ('Jet Blue', '2270001', '248', 'PokemonCompany', '2');
insert into Airplane values ('Jet Blue', '265601', '128', 'PokemonCompany', '4');
insert into Airplane values ('Jet Blue', '287933', '248', 'PokemonCompany', '1');

insert into Airline_staff values ('IronMan', '555555', 'Tony', 'Stark', '20001011','Jet Blue');

insert into Set_status values ('IronMan', 'Jet Blue', '213421', '202211', 'on-time');
insert into Set_status values ('IronMan', 'Jet Blue', '676432', '202211', 'on-time');
insert into Set_status values ('IronMan', 'Jet Blue', '439999', '202211', 'delayed');

insert into Flight values ('Jet Blue', '123', 'JFK', '2022-11-10 21:12:00.0', 'PVG', '2022-11-29 21:22::00.0', '500', '00001');
insert into Flight values ('EVA Air', '321', 'SDJ', '2022-11-10 21:22:00.0', 'PVG', '2022-11-29 21:22::00.0', '1500', '00001');
insert into Flight values ('Nippon Airways', '213', 'SDJ', '2012-11-10 21:22:00.0', 'JFK', '2022-11-29 21:22::00.0', '5010', '00001');
insert into Flight values ('Jet Blue', '123', 'JFK', '2002-11-10 21:22:00.0', 'SDJ', '2022-11-29 21:22::00.0', '500', '00001');
insert into Flight values ('EVA Air', '3231', 'SDJ', '2021-11-10 21:22:00.0', 'JFK', '2022-11-29 21:22::00.0', '5001', '00001');
insert into Flight values ('Nippon Airways', '213', 'SDJ', '2020-11-10 21:22:00.0', 'JFK', '2022-12-29 21:22::00.0', '500', '00001');
insert into Flight values ('Japan Airlines', '1263', 'JFK', '2019-11-10 21:22:00.0', 'PVG', '2022-11-29 21:22::00.0', '500', '00001');
insert into Flight values ('EVA Air', '3231', 'YNY', '2018-11-10 21:22:00.0', 'SDJ', '2022-11-29 21:22::00.0', '500', '00001');
insert into Flight values ('Nippon Airways', '2143', 'SDJ', '2017-11-10 21:22::00.0', 'JFK', '2022-11-29 21:22::00.0', '500', '00001');
insert into Flight values ('Jet Blue', '1213', 'PVG', '2002-11-9 21:22::00.0', 'SDJ', '2022-11-29 21:22::00.0', '5100', '00001');
insert into Flight values ('EVA Air', '3231', 'YNY', '2021-11-8 21:22::00.0', 'JFK', '2022-11-29 21:22::00.0', '5001', '00001');
insert into Flight values ('Nippon Airways', '213', 'SDJ', '2020-11-7 21:22::00.0', 'JFK', '2022-12-29 21:22::00.0', '500', '00001');
insert into Flight values ('Japan Airlines', '1263', 'JFK', '2019-11-6 21:22::00.0', 'PVG', '2022-11-29 21:22::00.0', '500', '00001');
insert into Flight values ('EVA Air', '3231', 'PVG', '2018-11-12 21:22::00.0', 'SDJ', '2022-11-29 21:22::00.0', '500', '00001');
insert into Flight values ('Nippon Airways', '2143', 'PVG', '2017-11-14 21:22::00.0', 'JFK', '2022-11-29 21:22::00.0', '500', '00001');

insert into Ticket values ('1', '', 'Jet Blue', '123', '500', '2002-11-10 21:22:00.0', 'Visa', '312866464', 'cardone', '20260810', '20221108');
insert into Ticket values ('3', '', 'Jet Blue', '123', '500', '2022-11-10 21:12:00.0', 'Visa', '87956462', 'cardthree', '20260225', '20221119');


