--task0:
select t1.collection_id, (select name from "Collections" where id=t1.collection_id) as name_collection, (select type from "Prices_tickets" where id=t2."Prices_tickets_id") as type, count(*) from "Collection_gallery" t1 
join  "Gallery_Prices_tickets" t2 on (t1.gallery_id=t2."Gallery_id") group by(t1.collection_id, t2."Prices_tickets_id") having count(*)>1;

--task 1:
select id, name, (select sum(insurance_value) from "Exhibits" where collection_id=c.id) from "Collections" c;

--task 2:
with coll as(select c.id, count(*) from "Collections" c join "Exhibits" e on c.id=e.collection_id group by c.id having count(*)>1)
select g.id, g.name, (select distinct count(*) from coll left join "Collection_gallery" cg on coll.id=cg.collection_id where cg.gallery_id=g.id ) 
from "Gallery" g 

--task 3:
ALTER TABLE IF EXISTS "Collection_gallery_Exhibits"
    ADD CONSTRAINT action_cg FOREIGN KEY ("Collection_gallery_id")
    REFERENCES "Collection_gallery" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;
ALTER TABLE IF EXISTS "Collection_gallery_Exhibits"
    ADD CONSTRAINT action_e FOREIGN KEY ("Exhibits_id")
    REFERENCES "Exhibits" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;
ALTER TABLE IF EXISTS "Exhibits"
    ADD CONSTRAINT action_collec FOREIGN KEY ("collection_id")
    REFERENCES "Collections" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;
ALTER TABLE IF EXISTS "Collection_gallery"
    ADD CONSTRAINT action_collec FOREIGN KEY ("collection_id")
    REFERENCES "Collections" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;
with d0 as (select collection_id, count(*) from "Collection_gallery" group by(collection_id) having count(*)<=1)
delete from "Collections" where id in(select collection_id from d0);

--task 4:
update "Exhibits" set insurance_value=insurance_value*2 where collection_id=(select id from "Collections" where name='Одежда народов востока') and protec_people=TRUE;

--task 5:
alter table "Exhibits" add column if not exists gallery_id integer;

--task 6:
update "Exhibits" set gallery_id='-1' where gallery_id is null;
alter table "Exhibits"
ADD CONSTRAINT check_galleryid_not_null
CHECK (gallery_id IS NOT NULL);


									  
									 