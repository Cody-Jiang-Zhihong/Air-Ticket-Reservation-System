select *
from Future_flights

select flight_number, the_status
from Set_status
where the_status = 'delayed'

select Customer.name
from Customer, Ticket
where Customer.email = Ticket.customer_email

select *
from Airplane
where airline = 'Jet Blue'