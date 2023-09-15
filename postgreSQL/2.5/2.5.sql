--task 0:
CREATE OR REPLACE FUNCTION control_price() RETURNS TRIGGER AS $$
	DECLARE
	cnt integer;
	BEGIN
		select count(*) into cnt from "Collection_gallery"
		where gallery_id = NEW.gallery_id;
		if cnt =0 then
		raise exception 'Нельзя';
		return NULL;
		end if;
		return OLD;
	END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE TRIGGER on_insert
BEFORE INSERT ON "Gallery_Prices_tickets"
FOR EACH ROW EXECUTE PROCEDURE control_price();

--task 1:
CREATE OR REPLACE FUNCTION quantity(name_gallery varchar) RETURNS integer AS $$
	DECLARE
	quantity integer;
	BEGIN
		SELECT DISTINCT count(*) INTO quantity
		from "Gallery" g join "Collection_gallery" cg on g.id=cg.collection_id 
						 join "Collection_gallery_Exhibits" cge on cg.id=cge."Collection_gallery_id" where g.name=name_gallery;
		return quantity;
	END
$$ LANGUAGE plpgsql;
select quantity(name) from "Gallery";

--task 2:
CREATE OR REPLACE FUNCTION test_min(integer, integer) RETURNS integer AS $$
	BEGIN
		IF $2 < $1 THEN	RETURN $2;
		ELSE RETURN $1;
		END IF;
	END
$$ LANGUAGE plpgsql;
CREATE OR REPLACE AGGREGATE integer_min(integer)
(
	stype = integer,
	sfunc = test_min,
	initcond = 2147483647
);
select integer_min(price) from "Collections" c join "Collection_gallery" cg on  c.id= cg.collection_id
											    join "Gallery_Prices_tickets" cpt on cg.gallery_id=cpt."Gallery_id"
												join "Prices_tickets" pt on  cpt."Prices_tickets_id"=pt.id



-- select c.id, cg.gallery_id, price from "Collections" c join "Collection_gallery" cg on  c.id= cg.collection_id
-- 											    join "Gallery_Prices_tickets" cpt on cg.gallery_id=cpt."Gallery_id"
-- 												join "Prices_tickets" pt on  cpt."Prices_tickets_id"=pt.id

--task 3:
CREATE VIEW exhibits_view AS
SELECT id, name, tempe_max, tempe_min, humidity_max, humidity_min, protec_people FROM "Exhibits";

CREATE OR REPLACE FUNCTION update_exhi_view() RETURNS TRIGGER AS $$
BEGIN
	IF (TG_OP = 'UPDATE') THEN
		UPDATE "Exhibits" SET name = NEW.name, tempe_max=NEW.tempe_max,tempe_min=NEW.tempe_min,
		humidity_max=NEW.humidity_max,humidity_min=NEW.humidity_min,protec_people=NEW.protec_people
		WHERE id = OLD.id;
		IF NOT FOUND THEN RETURN NULL; END IF;
	RETURN NEW;
	END IF;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER update_view
INSTEAD OF UPDATE ON exhibits_view
FOR EACH ROW EXECUTE PROCEDURE update_exhi_view();


UPDATE exhibits_view set tempe_min=58, humidity_min=-273 where id=2;
select * from "Exhibits";

--task 4:
CREATE OR REPLACE FUNCTION init() RETURNS VOID AS $$
	BEGIN 
		DROP TABLE IF EXISTS cache_queue;
		CREATE TABLE cache_queue(
			id SERIAL,
			data varchar(64)
		);
	END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION enqueue(a varchar(64)) RETURNS VOID AS $$
	BEGIN 
		INSERT INTO cache_queue (data) values (a);
	END;
$$ LANGUAGE plpgsql;
	
CREATE OR REPLACE FUNCTION dequeue() RETURNS VOID AS $$
	BEGIN 
		DELETE FROM cache_queue WHERE id=(select min(id) from cache_queue);
	END;
$$ LANGUAGE plpgsql;
	
CREATE OR REPLACE FUNCTION empty() RETURNS VOID AS $$
	BEGIN 
		DELETE FROM cache_queue;
	END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION top() RETURNS varchar(64) AS $$
	BEGIN 
		RETURN(SELECT data from cache_queue order by(id) asc limit 1);
	END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION tail() RETURNS varchar(64) AS $$
	BEGIN 
		RETURN(SELECT data from cache_queue order by(id) desc limit 1);
	END;
$$ LANGUAGE plpgsql;

select * from cache_queue;
select enqueue('08789sak');
select dequeue();
select empty();
select top();


