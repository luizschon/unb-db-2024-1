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
    event_id integer NOT NULL REFERENCES event (id) ON DELETE CASCADE,
    modality_id integer NOT NULL REFERENCES modality (id) ON DELETE RESTRICT
);

CREATE TABLE team
(
    id serial PRIMARY KEY,
    name character varying(50) NOT NULL,
    logo bytea NOT NULL
);

CREATE TABLE ranking
(
    tournament_id integer REFERENCES tournament (id) ON DELETE CASCADE,
    team_id integer REFERENCES team (id) ON DELETE RESTRICT,
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
    certification bytea NOT NULL
);

CREATE TABLE match
(
    id serial PRIMARY KEY,
    duration tsrange NOT NULL,
    tournament_id integer NOT NULL REFERENCES tournament (id) ON DELETE CASCADE,
    team1_id integer NOT NULL REFERENCES team (id) ON DELETE RESTRICT,
    team2_id integer NOT NULL REFERENCES team (id) ON DELETE RESTRICT,
    team1_score integer DEFAULT 0,
    team2_score integer DEFAULT 0,
    winner_id integer REFERENCES team (id) ON DELETE RESTRICT,
    location_id integer NOT NULL REFERENCES team (id) ON DELETE RESTRICT,
    referee_cpf character(11) NOT NULL REFERENCES referee (cpf) ON DELETE RESTRICT
);

CREATE TABLE player
(
    cpf character(11) PRIMARY KEY,
    name character varying(50) NOT NULL,
    birthdate date NOT NULL,
    starting boolean DEFAULT false,
    photo bytea NOT NULL,
    team_id integer NOT NULL REFERENCES team (id) ON DELETE CASCADE
);

CREATE TABLE coach
(
    cpf character(11) PRIMARY KEY,
    name character varying(50) NOT NULL,
    birthdate date NOT NULL,
    team_id integer NOT NULL REFERENCES team(id) ON DELETE CASCADE
);

CREATE TABLE sponsor
(
    cnpj character(14) PRIMARY KEY,
    name character varying(50) NOT NULL,
    logo bytea NOT NULL
);

CREATE TABLE sponsorship
(
    event_id integer REFERENCES event (id) ON DELETE CASCADE,
    sponsor_cnpj character(14) REFERENCES sponsor (cnpj) ON DELETE RESTRICT,
    amount money NOT NULL,
    PRIMARY KEY (event_id, sponsor_cnpj)
);

CREATE OR REPLACE VIEW upcoming_matches AS
    SELECT match.id, match.location_id, match.referee_cpf, match.team1_id,
    match.team2_id, match.duration, event.id as event_id, event.name AS event_name,
    m.id AS modality_id, m.name AS modality_name, team1.name AS team1_name,
    team2.name AS team2_name, l.name, l.city, l.state, l.address, r.name AS referee_name
    FROM event
    INNER JOIN tournament AS t ON t.event_id = event.id
    INNER JOIN modality AS m ON t.modality_id = m.id
    INNER JOIN match ON match.tournament_id = t.id
    INNER JOIN location AS l ON match.location_id = l.id
    INNER JOIN team AS team1 ON team1.id = match.team1_id
    INNER JOIN team AS team2 ON team2.id = match.team2_id
    INNER JOIN referee AS r ON match.referee_cpf = r.cpf
    WHERE lower(match.duration) > CURRENT_TIMESTAMP AT TIME ZONE 'UTC';

CREATE OR REPLACE VIEW finished_matches AS
    SELECT match.*, event.id as event_id, event.name AS event_name,
    m.id AS modality_id, m.name AS modality_name, team1.name AS team1_name,
    team2.name AS team2_name, l.name, l.city, l.state, l.address, r.name AS referee_name
    FROM event
    INNER JOIN tournament AS t ON t.event_id = event.id
    INNER JOIN modality AS m ON t.modality_id = m.id
    INNER JOIN match ON match.tournament_id = t.id
    INNER JOIN location AS l ON match.location_id = l.id
    INNER JOIN team AS team1 ON team1.id = match.team1_id
    INNER JOIN team AS team2 ON team2.id = match.team2_id
    INNER JOIN referee AS r ON match.referee_cpf = r.cpf
    WHERE upper(duration) < CURRENT_TIMESTAMP AT TIME ZONE 'UTC';

CREATE OR REPLACE VIEW ongoing_matches AS
    SELECT match.id, match.location_id, match.referee_cpf, match.team1_id,
    match.team2_id, match.team1_score, match.team2_score, match.duration,
    event.id as event_id, event.name AS event_name, m.id AS modality_id,
    m.name AS modality_name, team1.name AS team1_name, team2.name AS team2_name,
    l.name, l.city, l.state, l.address, r.name AS referee_name
    FROM event
    INNER JOIN tournament AS t ON t.event_id = event.id
    INNER JOIN modality AS m ON t.modality_id = m.id
    INNER JOIN match ON match.tournament_id = t.id
    INNER JOIN location AS l ON match.location_id = l.id
    INNER JOIN team AS team1 ON team1.id = match.team1_id
    INNER JOIN team AS team2 ON team2.id = match.team2_id
    INNER JOIN referee AS r ON match.referee_cpf = r.cpf
    WHERE CURRENT_TIMESTAMP AT TIME ZONE 'UTC' <@ duration;

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

INSERT INTO event (name, date)
VALUES ('Evento massa', '2024-08-27');
INSERT INTO event (name, date)
VALUES ('Evento legal', '2024-08-30');
INSERT INTO event (name, date)
VALUES ('Evento incrivel', '2024-09-03');
INSERT INTO event (name, date)
VALUES ('Evento mais ou menos', '2024-09-20');
INSERT INTO event (name, date)
VALUES ('Evento supimpa', '2024-09-20');

INSERT INTO sponsor (cnpj, name, logo)
VALUES ('11111111111111', 'Parrot Co.', pg_read_binary_file('parrot.png'));
INSERT INTO sponsor (cnpj, name, logo)
VALUES ('22222222222222', 'Fakestate Inc.', pg_read_binary_file('fakestate.png'));
INSERT INTO sponsor (cnpj, name, logo)
VALUES ('33333333333333', 'Green Company', pg_read_binary_file('green.jpg'));
INSERT INTO sponsor (cnpj, name, logo)
VALUES ('44444444444444', 'Triag Co.', pg_read_binary_file('triangle.png'));
INSERT INTO sponsor (cnpj, name, logo)
VALUES ('55555555555555', 'Gear SA', pg_read_binary_file('gearing.png'));

INSERT INTO sponsorship
VALUES (1, '11111111111111', 1000);
INSERT INTO sponsorship
VALUES (1, '22222222222222', 2000);
INSERT INTO sponsorship
VALUES (2, '22222222222222', 5000);
INSERT INTO sponsorship
VALUES (3, '55555555555555', 5000);
INSERT INTO sponsorship
VALUES (3, '11111111111111', 10000);
INSERT INTO sponsorship
VALUES (3, '33333333333333', 5000);
INSERT INTO sponsorship
VALUES (5, '11111111111111', 8000);
INSERT INTO sponsorship
VALUES (5, '22222222222222', 10000);
INSERT INTO sponsorship
VALUES (5, '44444444444444', 9000);
INSERT INTO sponsorship
VALUES (5, '55555555555555', 6000);

INSERT INTO modality (name, rules)
VALUES ('Futebol', pg_read_binary_file('regulamento_futebol.pdf'));
INSERT INTO modality (name, rules)
VALUES ('Voleibol', pg_read_binary_file('regulamento_volei.pdf'));
INSERT INTO modality (name, rules)
VALUES ('Futsal', pg_read_binary_file('regulamento_futsal.pdf'));
INSERT INTO modality (name, rules)
VALUES ('Basquete', pg_read_binary_file('regulamento_basquete.pdf'));
INSERT INTO modality (name, rules)
VALUES ('Tênis', pg_read_binary_file('regulamento_tenis.pdf'));

-- INSERT INTO tournament ()
-- VALUES ();

INSERT INTO team (name, logo)
VALUES ('Panda', pg_read_binary_file('pandas.png'));
INSERT INTO team (name, logo)
VALUES ('Hollow', pg_read_binary_file('hollow.png'));
INSERT INTO team (name, logo)
VALUES ('Postgres', pg_read_binary_file('postgres.png'));
INSERT INTO team (name, logo)
VALUES ('Tatu Bolas', pg_read_binary_file('tatu_bolas.png'));
INSERT INTO team (name, logo)
VALUES ('Caveiras', pg_read_binary_file('caveiras.png'));

-- INSERT INTO ranking ()
-- VALUES ();

INSERT INTO referee
VALUES ('11111111111', 'José da Silva', '1980-10-10', pg_read_binary_file('sample.pdf'));
INSERT INTO referee
VALUES ('22222222222', 'Luciele Valadares', '1990-10-18', pg_read_binary_file('sample.pdf'));
INSERT INTO referee
VALUES ('33333333333', 'Pedro Guimarães', '1985-08-27', pg_read_binary_file('sample.pdf'));
INSERT INTO referee
VALUES ('44444444444', 'Fernando Souza', '1979-04-20', pg_read_binary_file('sample.pdf'));
INSERT INTO referee
VALUES ('55555555555', 'Laila Gomes', '1992-01-02', pg_read_binary_file('sample.pdf'));

INSERT INTO coach
VALUES ('66666666666', 'Ricardo Cardoso', '1985-10-10', 1);
INSERT INTO coach
VALUES ('77777777777', 'Maria Cardoso', '1989-12-10', 2);
INSERT INTO coach
VALUES ('88888888888', 'Fernando Pereira', '1990-02-25', 3);
INSERT INTO coach
VALUES ('99999999999', 'Josefina de Jesus', '1980-12-25', 4);
INSERT INTO coach
VALUES ('10000000000', 'Felipe Bastos', '1968-06-06', 5);
INSERT INTO coach
VALUES ('10000000001', 'Felipe Bastos', '1968-06-06', 1);
INSERT INTO coach
VALUES ('10000000002', 'Priscila Fernandes', '1980-06-10', 2);
INSERT INTO coach
VALUES ('10000000003', 'Paula Brago', '1990-07-06', 3);

INSERT INTO player
VALUES ('10000000004', 'Rodolfo Nogueira', '2000-08-27', true, pg_read_binary_file('person1.jpg'), 1);
INSERT INTO player
VALUES ('10000000005', 'Filipe Souza', '2003-09-10', false, pg_read_binary_file('person2.jpg'), 1);
INSERT INTO player
VALUES ('10000000006', 'Hudson Machado', '1997-12-14', true, pg_read_binary_file('person3.jpg'), 2);
INSERT INTO player
VALUES ('10000000007', 'Fernanda Rodrigues', '1996-10-01', false, pg_read_binary_file('person4.jpg'), 2);
INSERT INTO player
VALUES ('10000000008', 'Rodrigo Oliveira', '2001-12-25', false, pg_read_binary_file('person5.jpg'), 3);
INSERT INTO player
VALUES ('10000000009', 'Carlos Frei', '2001-11-09', true, pg_read_binary_file('person6.jpg'), 3);
INSERT INTO player
VALUES ('10000000010', 'Luisa Ferreira', '2002-01-01', true, pg_read_binary_file('person7.jpg'), 4);
INSERT INTO player
VALUES ('10000000011', 'Pedro de Jesus', '2005-04-10', true, pg_read_binary_file('person8.jpg'), 5);

INSERT INTO location (name, city, state, address, capacity)
VALUES ('Mané Garrincha', 'Brasília', 'Distrito Federal', 'SRPN Estádio Nacional Mané Garrincha', 69910);
INSERT INTO location (name, city, state, address, capacity)
VALUES ('Arena Real', 'Sobradinho', 'Distrito Federal', 'Quadra 8 Conjunto A', 520);
INSERT INTO location (name, city, state, address, capacity)
VALUES ('Arena Irreal', 'Taguatinga', 'Distrito Federal', 'QNJ 14 Conjunto 10', 200);
INSERT INTO location (name, city, state, address, capacity)
VALUES ('Quadra dos Sonhos', 'Brasília', 'Distrito Federal', 'SQN 313', 100);
INSERT INTO location (name, city, state, address, capacity)
VALUES ('Quadra de Tênis', 'Brasília', 'Distrito Federal', 'Setor Hab Ind Sul', 200);

-- INSERT INTO match ()
-- VALUES ();

END;
