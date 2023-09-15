--task 1:
CREATE TABLE staff(
	id integer PRIMARY KEY,
	last_name varchar(64) NOT NULL,
	first_name varchar(64) NOT NULL,
	second_name varchar(64),
	sex char NOT NULL,
	birthday date,
	post varchar (128) NOT NULL,
	department varchar (128) NOT NULL,
	head_id integer references staff(id),
	CHECK (sex in ('м','ж')),
	CONSTRAINT post_department_unique UNIQUE (post, department)
);

select * from staff
drop sequence staff_id_seq

--task 2:
CREATE SEQUENCE staff_id_seq INCREMENT BY -1 start with 5 cache 10 NO minvalue maxvalue 5;
INSERT INTO staff VALUES
	(nextval('staff_id_seq'), 'Сталин','Иосиф','Виссарионович','м', to_date('21.12.1879','DD.MM.YYYY'),'Председатель','ГКО', null),
	(nextval('staff_id_seq'), 'Молотов','Вячеслав','Михайлович','м', to_date('09.03.1890', 'DD.MM.YYYY'), 'Заместитель председателя', 'ГКО', 5),
	(nextval('staff_id_seq'), 'Маленков','Георгий','Максимилианович','м', to_date('08.01.1902', 'DD.MM.YYYY'), 'Начальник', 'УК ЦК ВКП(б)', 4),
	(nextval('staff_id_seq'), 'Ворошилов','Климент','Ефремович','м', to_date('04.02.1881', 'DD.MM.YYYY'), 'Председатель КО', 'СНК', 4),
	(nextval('staff_id_seq'), 'Микоян','Анастас','Иванович','м', to_date('25.11.1895', 'DD.MM.YYYY'), 'Председатель', 'КП-ВС РККА', 4) 
returning *;

--task 3:
SELECT t1.last_name, t1.first_name, t1.second_name, t1.post, t2.last_name as hLast_name, t2.first_name as hFirstName, t2.second_name as hSecond_name
FROM staff t1 LEFT JOIN staff t2 ON (t1.head_id=t2.id);

--task 4:
update staff s1 set id=id-3 where (select count(*) from staff s2 where s2.head_id=s1.id)=0;
--task 5:
CREATE OR REPLACE PROCEDURE birthday_boys(month integer) as $$
	DECLARE
		attr_e record;
		a integer;
	BEGIN
		a:=0;
		FOR attr_e in (SELECT * FROM staff where extract(month from birthday) = month)
		LOOP
			raise info '% % % ',attr_e.last_name,attr_e.first_name,attr_e.second_name;
			a := a+1;
		END LOOP;
		raise info '%',a;
		raise info '%', (SELECT max(extract(year from age(NOW(),birthday))) from staff where extract(month from birthday) = month);
		raise info '%', (SELECT min(extract(year from age(NOW(),birthday))) from staff  where extract(month from birthday) = month);
		raise info '%', (SELECT round(avg(extract(year from age(NOW(),birthday))),2) from staff  where extract(month from birthday) = month);
	END
$$
LANGUAGE plpgsql;
call birthday_boys(2);

--task 6:
WITH RECURSIVE max_length AS (
	SELECT id, head_id, 1 AS s_length FROM staff WHERE head_id IS NULL
	UNION ALL SELECT s.id, s.head_id, s_length + 1 FROM staff s
	JOIN max_length ml ON s.head_id = ml.id
)
SELECT MAX(s_length)
FROM max_length;
