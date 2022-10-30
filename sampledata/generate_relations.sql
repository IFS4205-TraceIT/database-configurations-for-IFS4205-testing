do $$
DECLARE
	row record;
	ballot int;
	current_user_id uuid;
	random_date_time timestamp;
	temp_id int;
	temp_user_id uuid;
	temp_int int;
	temp_infectionh_id int;
	temp_timestamp timestamp;
BEGIN
	for row in (select * from users) LOOP
		current_user_id := row.id;
		-- Generate infection history
		-- SELECT floor(random()*(b-a+1))+a;
		ballot := (select floor(random()*(5-0+1))+0);
		for i in 1..ballot LOOP
			random_date_time := (
				select timestamp '2020-01-01 00:00:00' +
			   random() * (NOW() -
						   timestamp '2020-01-01 00:00:00')
								);
			insert into infectionhistory(user_id, recorded_timestamp) values(current_user_id, random_date_time);
		END LOOP;
		-- Generate vaccinationhistory
		ballot := (select floor(random()*(5-0+1))+0);
		for i in 1..ballot LOOP
			temp_id := (select floor(random()*(4-1+1))+1);
			temp_timestamp := (select start_date from vaccinationtypes where id = (select temp_id));
			random_date_time := (
				select date((select temp_timestamp) +
			   random() * (NOW() -
						   (select temp_timestamp))
								));
			
			BEGIN
				insert into vaccinationhistory(user_id, vaccination_id, date_taken) 
				values(current_user_id, temp_id,random_date_time);
			EXCEPTION WHEN unique_violation THEN 
			END;
		END LOOP;
		-- Generate closecontacts
		temp_int := (select count(id) from infectionhistory ih where ih.user_id = (select current_user_id));
		if temp_int > 0 then
			ballot := (select floor(random()*(200-0+1))+0);
			for i in 1..ballot LOOP
				temp_infectionh_id := (select id from infectionhistory ih where ih.user_id = (select current_user_id) order by random() limit 1);
				temp_timestamp := (select recorded_timestamp from infectionhistory ih where ih.id = (select temp_infectionh_id));
				temp_user_id := (select w.id from users w where w.id <> (select current_user_id) order by random() limit 1);
				random_date_time := (
					select (select temp_timestamp) - INTERVAL '14 DAY' +
				   random() * ((select temp_timestamp) -
							   ((select temp_timestamp) - INTERVAL '14 DAY'))
									);
				temp_int := (select -(floor(random()*(90-10+1))+10));
				BEGIN
					insert into closecontacts(infected_user_id, contacted_user_id, contact_timestamp, rssi, infectionhistory_id) 
					values(current_user_id, temp_user_id, random_date_time, temp_int, temp_infectionh_id);
				EXCEPTION WHEN unique_violation THEN
				END;
			END LOOP;
		end if;
		-- Generate Buildingaccess
		ballot := (select floor(random()*(15-0+1))+0);
		for i in 1..ballot LOOP
			random_date_time := (
				select timestamp '2020-01-01 00:00:00' +
			   random() * (NOW() -
						   timestamp '2020-01-01 00:00:00')
								);
			temp_user_id := (select id from buildings order by random() limit 1);
			BEGIN
				insert into buildingaccess(user_id, building_id, access_timestamp) values(current_user_id, temp_user_id, random_date_time);
			EXCEPTION WHEN unique_violation THEN
			END;
		END LOOP;
		-- raise notice 'Value: %', row;
	END LOOP;
end;$$
