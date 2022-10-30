DROP view if exists researchdata;
DROP table if exists CloseContacts, Notifications, InfectionHistory, VaccinationHistory, BuildingAccess, Users, Buildings, VaccinationTypes, ContactTracers;

create table Users(
	id uuid primary key,
	nric text unique not null,
	name text not null,
	dob date not null,
	email text,
	phone text not null,
	gender text not null,
	address text not null,
	postal_code text not null
);

create table Buildings(
	id uuid primary key,
	name text not null,
	location integer not null
);

create table BuildingAccess(
	id bigserial primary key,
	user_id uuid references Users(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	building_id uuid references Buildings(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	access_timestamp TIMESTAMP not null,
	unique(user_id, building_id, access_timestamp)
);

create table VaccinationTypes(
	id bigserial primary key,
	name text not null,
	start_date date not null
);

create table VaccinationHistory(
	id bigserial primary key,
	user_id uuid references Users(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	vaccination_id integer references VaccinationTypes(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	date_taken date not null,
	unique(user_id, vaccination_id, date_taken)
);

create table InfectionHistory(
	id bigserial primary key,
	user_id uuid references Users(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	recorded_timestamp TIMESTAMP not null,
	unique(user_id, recorded_timestamp)
);

create table ContactTracers(
	id uuid primary key
);

create table Notifications(
	due_date date,
	start_date date,
	tracer_id uuid references ContactTracers(id)
		ON DELETE SET NULL
		ON UPDATE CASCADE,
	infection_id integer references infectionhistory(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	uploaded_status boolean default FALSE,
	primary key(infection_id)
);

create table CloseContacts(
	id bigserial primary key,
	infected_user_id uuid references Users(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	contacted_user_id uuid references Users(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	contact_timestamp timestamp not null,
	rssi numeric not null,
	infectionhistory_id integer references InfectionHistory(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	constraint different_user check(
		infected_user_id <> contacted_user_id
	)
);







