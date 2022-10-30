drop table if exists researchdata, researchers;
create table researchdata(
	id bigserial primary key,
	dob text,
	gender text,
	postal_code text,
	list_of_vaccines text,
	last_close_contact text,
	last_infected_date text,
	total_infection bigint,
	total_close_contact_as_infected bigint,
	total_close_contact_with_infected bigint
);

create table researchers(
    id uuid primary key
)