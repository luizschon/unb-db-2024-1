BEGIN;

DROP TABLE IF EXISTS sponsorship CASCADE;
DROP TABLE IF EXISTS sponsor CASCADE;
DROP TABLE IF EXISTS coach CASCADE;
DROP TABLE IF EXISTS player CASCADE;
DROP TABLE IF EXISTS match CASCADE;
DROP TABLE IF EXISTS referee CASCADE;
DROP TABLE IF EXISTS location CASCADE;
DROP TABLE IF EXISTS ranking CASCADE;
DROP TABLE IF EXISTS team CASCADE;
DROP TABLE IF EXISTS tournament CASCADE;
DROP TABLE IF EXISTS modality CASCADE;
DROP TABLE IF EXISTS event CASCADE;

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
    team1_score integer DEFAULT 0,
    team2_score integer DEFAULT 0,
    winner_id integer REFERENCES team (id) ON DELETE RESTRICT,
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

CREATE OR REPLACE FUNCTION prevent_update_winner_before_match_end()
RETURNS trigger AS $$
BEGIN
    IF NEW.winner_id IS NOT NULL AND CURRENT_TIMESTAMP AT TIME ZONE 'UTC' <= upper(NEW.duration) THEN
        RAISE EXCEPTION 'Updates to winner column are not allowed before match end';
    ELSEIF NEW.winner_id IS NOT NULL AND NEW.winner_id != NEW.team1_id OR NEW.winner_id != NEW.team2_id THEN
        RAISE EXCEPTION 'Winner should be one of the competing teams';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER check_winner_update
BEFORE INSERT OR UPDATE ON match
FOR EACH ROW
EXECUTE FUNCTION prevent_update_winner_before_match_end();

CREATE OR REPLACE FUNCTION prevent_update_score_before_match()
RETURNS trigger AS $$
BEGIN
    IF NEW.team1_score != OLD.team1_score OR NEW.team2_score != OLD.team2_score
    AND CURRENT_TIMESTAMP AT TIME ZONE 'UTC' < lower(NEW.duration) THEN
        RAISE EXCEPTION 'Scores can only be updated during and after the match';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER check_score_update
BEFORE INSERT OR UPDATE ON match
FOR EACH ROW
EXECUTE FUNCTION prevent_update_score_before_match();

CREATE OR REPLACE PROCEDURE update_winners()
LANGUAGE SQL
BEGIN ATOMIC
    UPDATE match SET winner_id = CASE
        WHEN team1_score > team2_score THEN team1_id
        WHEN team1_score < team2_score THEN team2_id
        ELSE NULL
    END WHERE CURRENT_TIMESTAMP AT TIME ZONE 'UTC' > upper(duration);
END;

-- TODO: generate data


END;
