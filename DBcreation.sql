-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://github.com/pgadmin-org/pgadmin4/issues/new/choose if you find any bugs, including reproduction steps.
BEGIN;

CREATE TABLE IF NOT EXISTS public.genre (
    genre_id serial PRIMARY KEY,
    genre_name VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS public.movie
(
    "ID" serial NOT NULL,
    "Title" VARCHAR NOT NULL,
    imdb_rating integer,
    rotten_rating integer,
    meta_rating integer,
    pg_rating VARCHAR,
    CONSTRAINT "ID" PRIMARY KEY ("ID")
);

COMMENT ON TABLE public.movie
    IS 'contains movie details
';


CREATE TABLE IF NOT EXISTS public.movie_genre (
    movie_id INTEGER REFERENCES public.movie ("ID"),
    genre_id INTEGER REFERENCES public.genre (genre_id),
    PRIMARY KEY (movie_id, genre_id)
);

CREATE TABLE IF NOT EXISTS public.movie_actor
(
    movie integer NOT NULL,
    actor integer NOT NULL,
    PRIMARY KEY (movie, actor)
);

CREATE TABLE IF NOT EXISTS public.movie_director
(
    movie integer NOT NULL,
    director integer NOT NULL,
    PRIMARY KEY (movie, director)
);

CREATE TABLE IF NOT EXISTS public.movie_producer
(
    movie integer NOT NULL,
    producer integer NOT NULL,
    PRIMARY KEY (movie, producer)
);

CREATE TABLE IF NOT EXISTS public.movie_synopsis
(
    movie integer NOT NULL,
    synopsis integer NOT NULL,
    PRIMARY KEY (movie, synopsis)
);

CREATE TABLE IF NOT EXISTS public.person
(
    "ID" serial NOT NULL,
    "Name" character varying(255) NOT NULL,
    gender boolean,
    nationality character varying(255),
    "DOB" date,
    PRIMARY KEY ("ID")
);

COMMENT ON COLUMN public.person."DOB"
    IS 'date of birth';

CREATE TABLE IF NOT EXISTS public.synopsis
(
    "ID" serial NOT NULL,
    synopsis VARCHAR,
    CONSTRAINT synopsis_pkey PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public.award
(
    "ID" serial NOT NULL,
    name character varying,
    date date,
    PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public.movie_award
(
    "award_ID" integer NOT NULL,
    "movie_ID" integer NOT NULL,
    PRIMARY KEY ("award_ID", "movie_ID")
);

CREATE TABLE IF NOT EXISTS public.award_person
(
    "award_ID" integer NOT NULL,
    "person_ID" integer NOT NULL,
    PRIMARY KEY ("award_ID", "person_ID")
);

ALTER TABLE IF EXISTS public.movie_actor
    ADD CONSTRAINT movie_actor_movie_fkey FOREIGN KEY (movie)
    REFERENCES public.movie ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.movie_actor
    ADD FOREIGN KEY (actor)
    REFERENCES public.person ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.movie_director
    ADD CONSTRAINT movie_director_movie_fkey FOREIGN KEY (movie)
    REFERENCES public.movie ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.movie_director
    ADD FOREIGN KEY (director)
    REFERENCES public.person ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.movie_producer
    ADD CONSTRAINT movie_producer_movie_fkey FOREIGN KEY (movie)
    REFERENCES public.movie ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.movie_producer
    ADD FOREIGN KEY (producer)
    REFERENCES public.person ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.movie_synopsis
    ADD CONSTRAINT movie FOREIGN KEY (movie)
    REFERENCES public.movie ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.movie_synopsis
    ADD CONSTRAINT synopsis FOREIGN KEY (synopsis)
    REFERENCES public.synopsis ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.movie_award
    ADD FOREIGN KEY ("award_ID")
    REFERENCES public.award ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.movie_award
    ADD FOREIGN KEY ("movie_ID")
    REFERENCES public.movie ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.award_person
    ADD FOREIGN KEY ("award_ID")
    REFERENCES public.award ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.award_person
    ADD FOREIGN KEY ("person_ID")
    REFERENCES public.person ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.movie_genre
    ADD CONSTRAINT movie_genre_movie_fkey FOREIGN KEY (movie_id)
    REFERENCES public.movie ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.movie_genre
    ADD CONSTRAINT movie_genre_genre_fkey FOREIGN KEY (genre_id)
    REFERENCES public.genre (genre_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;
END;
