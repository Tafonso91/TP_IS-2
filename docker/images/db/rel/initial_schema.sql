CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;

-- Tabela Country
CREATE TABLE public.country (
    id   uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    country_name VARCHAR(50),
    geom GEOMETRY NULL,
    created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW() 
);

-- Tabela Strong_Foot
CREATE TABLE public.strong_foot (
    id  uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    foot_name VARCHAR(50),
    created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Tabela Club
CREATE TABLE public.club (
    id  uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    club_name VARCHAR(100),
    created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Tabela Player
CREATE TABLE public.player (
    id    uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100),
    height INT,
    price VARCHAR(20),
    salary VARCHAR(20),
    club_id uuid NOT NULL,
    country_id uuid NOT NULL,
    foot_id uuid NOT NULL,
    created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Tabela Player_Stats
CREATE TABLE public.player_stats (
    id  uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    overall INT,
    potential INT,
    offense VARCHAR(10),
    defense VARCHAR(10),
    player_id uuid NOT NULL,
    created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
   
);
CREATE TABLE public.teachers (
    name    VARCHAR (100),
    city    VARCHAR(100),
    created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO teachers(name, city) VALUES('Luís Teófilo', 'Porto');
INSERT INTO teachers(name, city) VALUES('Ricardo Castro', 'Braga');

INSERT INTO club(club_name) VALUES('Atlético dos Arcos');
INSERT INTO club(club_name) VALUES('Areosense');

INSERT INTO strong_foot(foot_name) VALUES('Right');
INSERT INTO strong_foot(foot_name) VALUES('Left');

INSERT INTO country(country_name) VALUES('Taiwan');

INSERT INTO player (name, height, price, salary, club_id, country_id, foot_id)
VALUES ('Zé Roberto', 180, '$10M', '$100K', 
        (SELECT id FROM club WHERE club_name = 'Atlético dos Arcos'), 
        (SELECT id FROM country WHERE country_name = 'Taiwan'), 
        (SELECT id FROM strong_foot WHERE foot_name = 'Right'));


ALTER TABLE player
    ADD CONSTRAINT player_club_id_fk
        FOREIGN KEY (club_id) REFERENCES club
            ON DELETE CASCADE;

ALTER TABLE player
    ADD CONSTRAINT player_country_id_fk
        FOREIGN KEY (country_id) REFERENCES country
            ON DELETE CASCADE;

ALTER TABLE player
    ADD CONSTRAINT player_strongfoot_id_fk
        FOREIGN KEY (foot_id) REFERENCES strong_foot
            ON DELETE CASCADE;

ALTER TABLE player_stats
    ADD CONSTRAINT playerstats_player_id_fk
        FOREIGN KEY (player_id) REFERENCES player
            ON DELETE CASCADE;





