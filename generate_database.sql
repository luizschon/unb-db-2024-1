BEGIN;

DROP TABLE IF EXISTS sponsorship;
DROP TABLE IF EXISTS sponsor;
DROP TABLE IF EXISTS coach;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS match;
DROP TABLE IF EXISTS referee;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS ranking;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS tournament;
DROP TABLE IF EXISTS modality;
DROP TABLE IF EXISTS event;

CREATE TABLE event
(
    id serial PRIMARY KEY,
    name character varying(50) NOT NULL,
    date date NOT NULL
);

CREATE TABLE modality
(
    id serial PRIMARY KEY,
    name character varying(50) NOT NULL,
    rules bytea NOT NULL
);

CREATE TABLE tournament
(
    id serial PRIMARY KEY,
    event_id serial NOT NULL REFERENCES event (id) ON DELETE CASCADE,
    modality_id serial NOT NULL REFERENCES modality (id) ON DELETE RESTRICT
);

CREATE TABLE team
(
    id serial PRIMARY KEY,
    name character varying(50) NOT NULL,
    logo bytea NOT NULL
);

CREATE TABLE ranking
(
    tournament_id serial REFERENCES tournament (id) ON DELETE CASCADE,
    team_id serial REFERENCES team (id) ON DELETE RESTRICT,
    points integer DEFAULT 0,
    PRIMARY KEY (tournament_id, team_id)
);

CREATE TABLE location
(
    id serial PRIMARY KEY,
    name character varying(50) NOT NULL,
    city character varying(50) NOT NULL,
    state character varying(50) NOT NULL,
    address character varying(100) NOT NULL,
    capacity integer NOT NULL
);

CREATE TABLE referee
(
    cpf character(11) PRIMARY KEY,
    name character varying(50) NOT NULL,
    birthdate date NOT NULL,
    photo bytea NOT NULL,
    certification bytea NOT NULL
);

CREATE TABLE match
(
    id serial PRIMARY KEY,
    duration tsrange NOT NULL,
    tournament_id serial NOT NULL REFERENCES tournament (id) ON DELETE CASCADE,
    team1_id serial NOT NULL REFERENCES team (id) ON DELETE RESTRICT,
    team2_id serial NOT NULL REFERENCES team (id) ON DELETE RESTRICT,
    team1_score integer NOT NULL DEFAULT 0,
    team2_score integer NOT NULL DEFAULT 0,
    winner_id serial REFERENCES team (id) ON DELETE RESTRICT,
    location_id serial NOT NULL REFERENCES team (id) ON DELETE RESTRICT,
    referee_cpf character(11) NOT NULL REFERENCES referee (cpf) ON DELETE RESTRICT
);

CREATE TABLE player
(
    cpf character(11) PRIMARY KEY,
    name character varying(50) NOT NULL,
    birthdate date NOT NULL,
    starting boolean DEFAULT false,
    photo bytea NOT NULL,
    team_id serial NOT NULL REFERENCES team (id) ON DELETE CASCADE
);

CREATE TABLE coach
(
    cpf character(11) PRIMARY KEY,
    name character varying(50) NOT NULL,
    birthdate date NOT NULL,
    photo bytea NOT NULL,
    team_id serial NOT NULL REFERENCES team(id) ON DELETE CASCADE
);

CREATE TABLE sponsor
(
    cnpj character(14) PRIMARY KEY,
    name character varying(50) NOT NULL,
    logo bytea NOT NULL
);

CREATE TABLE sponsorship
(
    event_id serial REFERENCES event (id) ON DELETE CASCADE,
    sponsor_cnpj character(14) REFERENCES sponsor (cnpj) ON DELETE RESTRICT,
    amount money NOT NULL,
    PRIMARY KEY (event_id, sponsor_cnpj)
);

-- TODO: generate data

END;
