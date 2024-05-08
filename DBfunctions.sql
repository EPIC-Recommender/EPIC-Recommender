-- FUNCTION: public.insert_genre(character varying)

-- DROP FUNCTION IF EXISTS public.insert_genre(character varying);

CREATE OR REPLACE FUNCTION public.insert_genre(
	genre_name_input character varying)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    genre_id_output integer;
BEGIN
    -- Check if the genre already exists
    SELECT genre_id INTO genre_id_output
    FROM public.genre
    WHERE genre_name = genre_name_input;
    
    -- If the genre exists, return its ID
    IF FOUND THEN
        RETURN genre_id_output;
    ELSE
        -- Insert the new genre
        INSERT INTO public.genre (genre_name)
        VALUES (genre_name_input)
        RETURNING genre_id INTO genre_id_output;
        
        RETURN genre_id_output;
    END IF;
END;
$BODY$;

ALTER FUNCTION public.insert_genre(character varying)
    OWNER TO postgres;

