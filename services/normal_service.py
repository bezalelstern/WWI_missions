from db import get_db_connection, release_db_connection
import psycopg2

from services.logger import log_error, log


def normalize_db():
    source_conn = get_db_connection()
    try :
        query = """
        insert into normal_mission select * from mission
        """
        query1 = """CREATE TABLE target (
                            target_pk serial primary key,
                            mission_id integer,
                            country VARCHAR(100),
                            city VARCHAR(100),
                            type VARCHAR(100),
                            industry VARCHAR(255),
                            priority VARCHAR(5),
                            latitude NUMERIC(10, 6),
                            longitude NUMERIC(10, 6)
                        )
        """
        query2 = """insert into target(mission_id, country, city, type, industry, priority, latitude, longitude)
                        SELECT DISTINCT
                            mission_id,
                            target_country,
                            target_city,
                            target_type,
                            target_industry,
                            target_priority,
                            target_latitude,
                           target_longitude
                        from normal_mission;
        """

        query3 = """ALTER TABLE normal_mission
                        DROP COLUMN target_country,
                        DROP COLUMN target_city,
                        DROP COLUMN target_type,
                        DROP COLUMN target_industry,
                        DROP COLUMN target_priority,
                        DROP COLUMN target_latitude,
                        DROP COLUMN target_longitude;
                       """
        query3_5 = """ALTER TABLE normal_mission ADD COLUMN target_fk int references target(target_pk);"""


        query4 = """UPDATE normal_mission
                    SET target_fk = target.target_pk
                    FROM target
                    WHERE normal_mission.mission_id = target.mission_id;
        """


        query5 = """CREATE TABLE country (
                    country_id SERIAL PRIMARY KEY,
                    country_name VARCHAR(100)
                    );"""


        query6 = """
                   CREATE TABLE city (
                        city_id SERIAL PRIMARY KEY,
                        city_name VARCHAR(100),
                        country_id INTEGER REFERENCES country(country_id)
                    );
        """


        query7 = """CREATE TABLE target_type (
        type_id SERIAL PRIMARY KEY,
        type_name VARCHAR(100) UNIQUE
        );
        """

        query8 = """CREATE TABLE target_industry (
                    industry_id SERIAL PRIMARY KEY,
                    industry_name VARCHAR(255) UNIQUE
);
        """
        query9 = """
        INSERT INTO country(country_name) SELECT DISTINCT target.country FROM target;
        """
        query10 = """
        INSERT INTO city (city_name, country_id)
        SELECT DISTINCT city, (SELECT country_id FROM country WHERE country_name = target.country)
        FROM target;
           """
        query11= """
        INSERT INTO target_type (type_name)
        SELECT DISTINCT type FROM target;
               """
        query12 = """
                INSERT INTO target_industry (industry_name)
                SELECT DISTINCT industry FROM target;
               """
        query13 = """
                UPDATE target
                SET country = (
                    SELECT country_id FROM country WHERE country.country_name = target.country
                );
               """
        query14 = """
        UPDATE target
        SET industry = (
        SELECT industry_id FROM target_industry WHERE target_industry.industry_name =  target.industry
        );
               """
        query15 = """
        UPDATE target
        SET type = (
         SELECT type_id FROM target_type WHERE target_type.type_name = target.type
        );
               """
        query16 = """
            ALTER TABLE target
            DROP COLUMN city;
               """

        # execute the queries
        queries = [query, query1, query2, query3, query3_5, query4, query5, query6, query7, query8, query9, query10, query11, query12, query13, query14, query15, query16]
        with source_conn.cursor() as cursor:
           for query in queries:
               cursor.execute(query)
        source_conn.commit()
        log("Normalization completed successfully")


    except Exception as e:
        print(f"An error occurred: {e}")
        log_error(f"An error occurred: {e}")
        source_conn.rollback()
    finally:
        release_db_connection(source_conn)