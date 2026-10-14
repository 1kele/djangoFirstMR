create table hotels_hotels(
id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
name VARCHAR(255) not null UNIQUE,
city VARCHAR(100) not null,
address TEXT,
founding_date DATE not null,
stars INT not null check (stars <= 5 and stars > 0)
);

create table hotels_rooms(
id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
hotel_id INT not null,
price NUMERIC(10,2) not null,
occupancy INT not null,
description TEXT,
created_at DATE DEFAULT CURRENT_DATE,

FOREIGN KEY (hotel_id) references Hotels(id),

constraint chk_room_occupancy
	check (occupancy > 0),

constraint chk_room_price
	check (price > 0)
);

create table hotels_facilities(
id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
name VARCHAR(255)
);

create table hotels_rooms_facilities(
room_id INT,
facility_id INT,

primary key(room_id, facility_id),

FOREIGN key (room_id) references Rooms(id) on delete cascade,
FOREIGN key (facility_id) references Facilities(id) on delete cascade
);

create table bookings_booking(
id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
room_id INT,
start_date DATE,
end_date DATE,
price_per_night NUMERIC(10,2),
total_price NUMERIC(12,2),
status TEXT,


foreign key (room_id) references Rooms(id) on delete CASCADE,

constraint chk_booking_dates
	check (end_date > start_date),

constraint chk_booking_price
	check (price_per_night > 0),

constraint chk_booking_total_price
	check (total_price > 0),

constraint chk_booking_status
	check (status in ('created', 'confirmed', 'cancelled', 'completed'))
);

