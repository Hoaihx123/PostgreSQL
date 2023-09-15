create sequence gallery_se increment by 1 start 1
create sequence seq increment by 1 start 1

INSERT INTO public."Gallery" VALUES (setval('gallery_se',1),'Pace Gallery'),(nextval('gallery_se'),'Gagosian'),(nextval('gallery_se'),'David Zwirner'),
(nextval('gallery_se'),'White Cube'),(nextval('gallery_se'),'Lisson Gallery'),(nextval('gallery_se'),'Thaddaeus Ropac'),(nextval('gallery_se'),'Perrotin');

INSERT INTO public."Prices_tickets" VALUES (setval('seq',1),'adult',15),(nextval('seq'),'elderly',12), (nextval('seq'),'children',10),
(nextval('seq'),'student',12),(nextval('seq'),'foreigners',11);

INSERT INTO public."Gallery_Prices_tickets" values (1,2),(1,4),(1,5),(2,3),(2,4),(2,5),(3,2),(3,4),(3,3),(4,3),(5,2),(7,3);

INSERT INTO public."Collections" values (setval('seq',1),'Музей императорских коллекций (Токио)','Часы работы: 9:00—16:00, закрыт по понедельникам и пятницам.Вход свободный.'),
(nextval('seq'),'Метеоритная коллекция Российской академии наук','одно из крупнейших музейных собраний метеоритов в России.'),
(nextval('seq'),'Коллекция Филиппи','Коллекция Филиппи является собранием клерикальных, религиозных и духовных головных уборов.'),
(nextval('seq'),'Дзиковская коллекция','название несуществующего в настоящее время единого собрания произведений искусства'),
(nextval('seq'),'Коллекция достопримечательностей Российской империи','Создание коллекции охватывает период с 1903 (или 1904) по 1916 год.'),
(nextval('seq'),'Музей личных коллекций','Открытие состоялось в 1994-м, а в 2005 году отдел был перенесён в отреставрированную усадьбу на Волхонке');


INSERT INTO public."Collection_gallery" values (setval('seq',1),2,1,'11-10-23',NULL),(nextval('seq'),2,4,'16-10-22','11-11-22'),(nextval('seq'),3,2,'1-3-23','14-5-24'),(nextval('seq'),3,5,'11-10-24',NULL),
(nextval('seq'),4,6,'1-9-22',NULL),(nextval('seq'),4,3,'3-10-23',NULL),(nextval('seq'),5,2,'01-10-22','1-3-23'),(nextval('seq'),5,4,'11-1-23',NULL);


INSERT INTO public."Exhibits" values (setval('seq',1),'Мумия','Па-ди-ист не единственный мумифицированный мертвец в Эрмитаже. Всего в запасниках их хранится не меньше пяти.',10000,18,1,1.3,3,1.2,100,0,120,120),
(nextval('seq'),'Мадонна Бенуа','она попала в Россию, проста: Мария Бенуа, в девичестве Сапожникова, получила картину по наследству от отца.',100000,15,2,1.5,1.0,2.5,100,-10,150,50),
(nextval('seq'),'Мадонна Литта',NULL,40000,18,3,2.1,0.5,5.2,100,20,200,15),
(nextval('seq'),'Часы «Павлин»',NULL,52000,16,4,0.5,0.3,0.8,150,-20,200,12),
(nextval('seq'),'«Даная» Рембрандта',NULL,180000,18,5,0.5,1.2,3.7,100,20,200,30);


INSERT INTO public."Collection_gallery_Exhibits" VALUES (1,5),(2,3),(3,1),(3,2),(5,4),(5,2);


alter table "Exhibits" drop column gallery_id
select setval('seq',1)

delete from public."Gallery"  where true
select * from public."Collection_gallery_Exhibits" 