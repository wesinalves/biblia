import psycopg2

with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * from webapp_idiom")
        #cur.fetchone()

        for record in cur:
            print(record)

        conn.commit()

        