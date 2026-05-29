SET search_path TO lyfter_car_rental;

BEGIN;

CREATE TABLE users (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(60),
    birthdate DATE NOT NULL,
    account_status VARCHAR(20),
    CONSTRAINT valid_status CHECK (account_status IN ('active', 'closed', 'delinquent'))
);

INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('pallchorn0@bbb.org', 'kbinden0', 'nE8cvap?7E?G', 'Adan Colenutt', '1955-04-12', 'closed');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('smerriment1@fc2.com', 'egreedyer1', 'uH7.$!GCLkt', 'Dalenna Davoren', '2003-11-19', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('rgoodfellowe2@constantcontact.com', 'edobrowolski2', 'mX8+dVUMn', 'Lindon Von Welden', '1950-09-09', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('egateman3@zdnet.com', 'dloweth3', 'qA7!BoL?Pq7)m', 'Jeremiah Utton', '1962-12-22', 'closed');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('bgebuhr4@blogs.com', 'pfigge4', 'sU9`FJ\Lo||7Nur', 'Mirna Bertelsen', '2008-02-25', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('bmourbey5@discuz.net', 'lbrabin5', 'aZ8>@$/&_5V', 'Deirdre Kidstoun', '1985-08-18', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('gtwatt6@census.gov', 'asilveston6', 'vO2~8=2=x0?=G', 'Crissy Crasford', '1969-02-17', 'closed');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('kbarwack7@blogs.com', 'gjeanet7', 'eH4?j00h8', 'Kellsie Pinson', '1967-09-05', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('kpurkess8@gov.uk', 'rmeakes8', 'tT0"$2jv0sEJ', 'Zora Organ', '1963-09-14', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('ksatyford9@globo.com', 'lmalamore9', 'eD5+_Gu8', 'Davy Scalia', '1937-04-19', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('aredsella@people.com.cn', 'pbleslia', 'uD9%PnY+', 'Tann Tomaszewski', '1975-05-05', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('mmcquillanb@angelfire.com', 'fsmallshawb', 'uT4$q3F+"', 'Zebulen Rosgen', '1991-10-15', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('acuttenc@bravesites.com', 'tcreadyc', 'lM0&zce&D)r&<KK', 'Jen Zupo', '1999-07-13', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('scristofarod@abc.net.au', 'vlaverockd', 'gQ6}TN}#S9}', 'Purcell Van Der Weedenburg', '1929-10-24', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('cdibnere@house.gov', 'wmillmoree', 'qO8~j2pGBn}Xb*', 'Aubry Evitt', '1967-07-30', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('rdixseef@unesco.org', 'gbrestonf', 'pH8cG}Np~T{|__''', 'Jonathon Kharchinski', '1967-07-01', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('stalkingtong@topsy.com', 'lfelgatg', 'rM4"Ia%%@<o0W|D', 'Otho Gilffillan', '1922-06-23', 'closed');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('sbeddoesh@washingtonpost.com', 'tplumeh', 'uN1{X}(&39', 'Thomasina Antuoni', '1982-05-25', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('sfarmani@ox.ac.uk', 'jgalifordi', 'fZ7}vm}2=wq', 'Buck Ortiger', '1959-05-05', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('mmacadamj@howstuffworks.com', 'rkobaj', 'kC2+TGn@3Dkj', 'Aluin Russi', '1985-10-19', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('gtoppesk@ed.gov', 'hendleyk', 'xL98c,y', 'Mersey Peto', '1998-01-05', 'closed');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('cangearl@artisteer.com', 'mmathersl', 'yZ5(xRnYR|Z7u?xa', 'Deck Melmar', '1991-07-07', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('gorsm@howstuffworks.com', 'hshergillm', 'xZ5?SOTQ,}h', 'Tull Westmore', '1940-07-22', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('bboultwoodn@tripod.com', 'reamesn', 'wE4@!pf8E', 'Shea Grise', '1980-09-01', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('cbrigdaleo@google.de', 'gvanneo', 'mS7*C|7P$o', 'Levey Cunio', '1973-01-22', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('cgathwaitep@ucla.edu', 'jcrookallp', 'fE9/zhfS#i}lgP', 'Lucy Toma', '1985-02-11', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('ashenfischq@smh.com.au', 'jbatisteq', 'nA1!pFi3m@', 'Joceline Pautot', '1997-12-19', 'closed');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('stiftr@timesonline.co.uk', 'hchamleyr', 'jW5/O%eJ&Y6D', 'Riki Stebbin', '1922-02-20', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('gdiamants@youku.com', 'jdyersons', 'pS9@s13($O\36&P5', 'Gianina Huc', '1941-12-17', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('rgoldingayt@mysql.com', 'bgillinot', 'tK7)KND9#k*''B', 'Jayne Zettoi', '2003-03-21', 'delinquent');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('djealousu@hao123.com', 'bbirrellu', 'yS3&3<6l$|', 'Korrie Spiers', '1994-03-25', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('tjochensv@nationalgeographic.com', 'ldogertyv', 'pN0$a/MO\u=e', 'Becca Burge', '1971-09-09', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('kbridellw@wikimedia.org', 'kminersw', 'jS2?E5"!~\D\o', 'Cassondra Sieb', '1969-03-06', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('clipgensx@house.gov', 'ccaudrelierx', 'sG4?tkV}<5M', 'Katherine Wraight', '1990-06-27', 'delinquent');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('abertelety@t.co', 'othirwelly', 'dK0+uW|(ln8', 'Cammi Stirton', '2011-04-13', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('bdyottz@toplist.cz', 'jsitlintonz', 'rF4*bcWJ&FK', 'Coraline McIlvenny', '1962-09-11', 'delinquent');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('oomailey10@omniture.com', 'bwainer10', 'oB1{Za=Uu|4c', 'Dominga Talks', '1921-05-08', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('ogowthrop11@tripadvisor.com', 'zbeardshaw11', 'wM5{MH|("p7', 'Kelci Hathorn', '2004-05-12', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('mbullock12@addtoany.com', 'cwyer12', 'fM8*@BpDsm', 'Tymothy McFie', '1924-11-01', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('jwhitemarsh13@ucoz.ru', 'jbeccera13', 'mK9}lXC4v=Tum', 'Kristina Knock', '1981-07-02', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('klusty14@nhs.uk', 'vsanchiz14', 'eR8/Fj<', 'Jed Harnetty', '1935-01-06', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('gisworth15@irs.gov', 'flillgard15', 'uA2+*''?r', 'Dillie Kaysor', '1975-08-22', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('ssinkin16@nps.gov', 'gstiegars16', 'pO8,#p5${', 'Englebert Patchett', '1993-08-02', 'closed');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('cdibdale17@slate.com', 'atrahar17', 'cY2F@vS', 'Corbin Pegram', '1956-07-04', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('rvanbaaren18@ft.com', 'ofreebury18', 'aL1{\jC=4zRhKi', 'Matthiew Mengue', '1972-03-25', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('emacauley19@tripod.com', 'acarlo19', 'cD3_G\b4u>,zW)3', 'Karel Jell', '1968-01-18', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('kcastro1a@hao123.com', 'emould1a', 'vE8/_R+|R', 'Birch Lathan', '1997-06-25', 'delinquent');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('amillom1b@msu.edu', 'arisdall1b', 'cT3)l.#xa7w\_cj', 'Freddy Pllu', '1947-08-01', 'delinquent');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('efitzmaurice1c@theatlantic.com', 'ygrew1c', 'gL9?/SHVh"', 'Tobe Shasnan', '1970-06-26', 'active');
INSERT INTO users (email, username, password, full_name, birthdate, account_status) VALUES ('escarlin1d@state.tx.us', 'lbisp1d', 'dK9?5Ils.x<rrK`}', 'Miltie Jendrys', '1964-02-08', 'active');

COMMIT;