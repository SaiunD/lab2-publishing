import psycopg2
from view import View


class Model:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='230520',
            host='localhost',
            port=5432
        )
        self.view = View()
        self.create_table_author()
        self.create_table_publication()
        self.create_table_collection()
        self.create_table_publishing()

    def create_table_author(self):
        c = self.conn.cursor()

        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'Author')")
        table_exists = c.fetchone()[0]

        if not table_exists:
            c.execute('''
                CREATE TABLE "Author" (
                    "AuthorID" character varying NOT NULL,
                    "Name" character varying NOT NULL,
                    "Surname" character varying NOT NULL,
                    CONSTRAINT "Author_pkey" PRIMARY KEY ("AuthorID")
                )
            ''')

        self.conn.commit()

    def create_table_publication(self):
        c = self.conn.cursor()

        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'Publicaion')")
        table_exists = c.fetchone()[0]

        if not table_exists:
            c.execute('''
                CREATE TABLE IF NOT EXISTS "Publication" (
                    "PublicationID" character varying NOT NULL,
                    "Name" character varying NOT NULL,
                    "Language" character varying NOT NULL,
                    "Field" character varying NOT NULL,
                    "Pages" integer,
                    CONSTRAINT "Publication_pkey" PRIMARY KEY ("PublicationID")
                )
            ''')

        self.conn.commit()

    def create_table_collection(self):
        c = self.conn.cursor()

        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'Collection')")
        table_exists = c.fetchone()[0]

        if not table_exists:
            c.execute('''
                CREATE TABLE "Collection" (
                    "ISSN" integer NOT NULL,
                    "Name" character varying NOT NULL,
                    "Type" character varying NOT NULL,
                    "Category" character varying NOT NULL,
                    CONSTRAINT "Collection_pkey" PRIMARY KEY ("ISSN")
                )
            ''')

        self.conn.commit()

    def create_table_publishing(self):
        c = self.conn.cursor()

        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'Publishing')")
        table_exists = c.fetchone()[0]

        if not table_exists:
            c.execute('''
                CREATE TABLE "Publishing" (
                    "AuthorID" character varying,
                    "PublicationID" character varying,
                    "ISSN" integer,
                    "date" date,
                    CONSTRAINT "Publishing_AuthorID_fkey" FOREIGN KEY ("AuthorID") REFERENCES "Author" ("AuthorID"),
                    CONSTRAINT "Publishing_PublicationID_fkey" FOREIGN KEY ("PublicationID") REFERENCES "Publication" ("PublicationID"),
                    CONSTRAINT "Publishing_ISSN_fkey" FOREIGN KEY ("ISSN") REFERENCES "Collection" ("ISSN")
                )
            ''')

        self.conn.commit()

    def get_all(self, table_name):
        c = self.conn.cursor()
        c.execute(f'SELECT * FROM "{table_name}"')
        return c.fetchall()

    def add_data(self, table_name, data):
        try:
            c = self.conn.cursor()
            placeholders = ", ".join(["%s"] * len(data))
            sql = f"INSERT INTO \"{table_name}\" VALUES ({placeholders});"
            c.execute(sql, list(data.values()))
            self.conn.commit()
            self.view.show_message("Added successfully!")
        except psycopg2.errors.ForeignKeyViolation as e:
            self.conn.rollback()
            self.view.show_message(f"ПОМИЛКА: немає референсу на дані з батьківських таблиць. \nКод помилки: {e.pgcode}.")
        except psycopg2.errors.UniqueViolation as e:
            self.conn.rollback()
            self.view.show_message(f"ПОМИЛКА: дані з таким ключем вже існують. \nКод помилки: {e.pgcode}.")

    def update_data(self, table_name, data, condition_column, condition_value):
        try:
            if not table_name or not data or not condition_column or condition_value is None:
                print("Insufficient information to update data.")
                return

            c = self.conn.cursor()
            set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
            sql = f"UPDATE \"{table_name}\" SET {set_clause} WHERE \"{condition_column}\" = %s;"

            values = list(data.values())
            values.append(condition_value)
            c.execute(sql, values)
            self.conn.commit()
            self.view.show_message("Updated successfully!")
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)

    def delete_data(self, table_name, cond, val):
        try:
            if not table_name or cond is None:
                print("Insufficient information to update data.")
                return

            c = self.conn.cursor()
            sql = f"DELETE FROM \"{table_name}\" WHERE \"{cond}\" = '{val}';"
            c.execute(sql)
            self.conn.commit()
            self.view.show_message("Deleted successfully!")
        except psycopg2.errors.ForeignKeyViolation as e:
            self.conn.rollback()
            self.view.show_message(f"ПОМИЛКА: видаліть спочатку з \"Publishing\" записи з \"{cond}\" = '{val}'\nПісля чого спробуйте ще раз.")

    def delete_data_publishing(self, table_name, cond1, val1, cond2, val2, cond3, val3):
        try:
            if not table_name or cond1 or cond2 or cond3 is None:
                print("Insufficient information to update data.")
                return

            c = self.conn.cursor()
            sql = f"DELETE FROM \"{table_name}\" WHERE \"{cond1}\" = '{val1}' AND \"{cond2}\" = '{val2}'AND \"{cond3}\" = {val3}"
            c.execute(sql)
            self.conn.commit()
            self.view.show_message("Deleted successfully!")
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)

    def generate_data(self, table_name, num):
        try:
            c = self.conn.cursor()
            if table_name == "Author":
                sql = (f"insert into \"Author\" select distinct md5(random()::text), chr(trunc(65+random()*25)::int) || chr(trunc(97+random()*26)::int) || chr(trunc(97+random()*26)::int), chr(trunc(65+random()*25)::int) || chr(trunc(97+random()*26)::int) || chr(trunc(97+random()*26)::int)"
                       f"from generate_series(1,{num})")
            elif table_name == "Publication":
                sql = (f"INSERT INTO \"Publication\""
                       f"SELECT DISTINCT "
                       f"md5(random()::text), "
                       f"chr(trunc(65 + random() * 25)::int) || chr(trunc(97 + random() * 26)::int) || chr(trunc(97 + random() * 26)::int) || chr(trunc(65 + random() * 25)::int) || chr(trunc(97 + random() * 26)::int) || chr(trunc(97 + random() * 26)::int), "
                       f"('{{\"ukrainian\", \"english\", \"spanish\", \"croatian\", \"portuguese\", \"french\"}}'::text[])[floor(random()*6)+1], "
                       f"('{{\"medicine\", \"biology\", \"engineering\", \"economics\", \"physics\", \"chemistry\", \"history\", \"philosophy\"}}'::text[])[floor(random()*8+1)], floor(random() * 100) "
                       f"FROM generate_series(1, {num})"
                       )
            elif table_name == "Collection":
                sql = (f"INSERT INTO \"Collection\""
                       f"SELECT pr.\"ISSN\", pr.\"Name\", pr.\"Type\", pr.\"Category\""
                       f"FROM \"Collection\""
                       f"RIGHT JOIN"
                       f"(SELECT DISTINCT "
                       f"floor(random() * 100000000) + 1, "
                       f"chr(trunc(65 + random() * 25)::int) || chr(trunc(97 + random() * 26)::int) || chr(trunc(97 + random() * 26)::int) || chr(trunc(65 + random() * 25)::int) || chr(trunc(97 + random() * 26)::int) || chr(trunc(97 + random() * 26)::int), "
                       f"('{{\"e-book\", \"paper book\"}}'::text[])[floor(random()*2)+1], "
                       f"('{{\"A\", \"B\", \"C\"}}'::text[])[floor(random()*3+1)] "
                       f"FROM generate_series(1, {num})) pr"
                       f"ON \"Collection\".\"ISSN\" = sb.\"ISSN\" and \"Collection\".\"Name\"=sb.\"Name\" and \"Collection\".\"Type\" = sb.\"Type\" and \"Collection\".\"Category\"=sb.\"Category\""
                       f"WHERE \"Collection\".\"ISSN\" is null and \"Collection\".\"Name\" is null and \"Collection\".\"Type\" is null and \"Collection\".\"Category\" is null"
                       )
            elif table_name == "Publishing":
                num3 = round(num**(1/3), 0)
                sql = (f"INSERT INTO \"Publishing\" "
                       f"SELECT pr.\"AuthorID\", pr.\"PublicationID\", pr.\"ISSN\", pr.\"Date\" "
                       f"FROM \"Publishing\" RIGHT JOIN"
                       f"(SELECT DISTINCT "
                       f"t1.\"AuthorID\", "
                       f"t2.\"PublicationID\", "
                       f"t3.\"ISSN\", "
                       f"'2000-01-01'::date + trunc(random() * 366 * 10)::int as \"Date\" "
                       f"FROM "
                       f"(SELECT \"AuthorID\", row_number() OVER (ORDER BY random()) as rn FROM \"Author\" order by random() LIMIT {num3}) t1, "
                       f"(SELECT \"PublicationID\", row_number() OVER (ORDER BY random()) as rn FROM \"Publication\" order by random() LIMIT {num3}) t2, "
                       
                       
                       f"(SELECT \"ISSN\", row_number() OVER (ORDER BY random()) as rn FROM \"Collection\" order by random() LIMIT {num3}) t3 "
                       f"LIMIT {num}) pr "
                       f"ON \"Publishing\".\"AuthorID\" = pr.\"AuthorID\" "
                       f"AND \"Publishing\".\"PublicationID\" = pr.\"PublicationID\""
                       f"AND \"Publishing\".\"ISSN\" = pr.\"ISSN\""
                       f"WHERE \"Publishing\".\"AuthorID\" IS NULL and \"Publishing\".\"PublicationID\" is null and \"Publishing\".\"ISSN\" is null"
                       )
            c.execute(sql, num)
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)

    def show_by_field_language(self, field, language):
        try:
            c = self.conn.cursor()
            sql = (f"SELECT \"Author\".\"Name\" AS author_name, \"Author\".\"Surname\" AS author_surname, \"Publication\".\"Name\" AS pub_name, \"Publishing\".\"Date\" "
                   f"FROM \"Author\" "
                   f"JOIN \"Publishing\" ON \"Author\".\"AuthorID\" = \"Publishing\".\"AuthorID\""
                   f"JOIN \"Publication\" ON \"Publishing\".\"PublicationID\" = \"Publication\".\"PublicationID\" "
                   f"WHERE \"Publication\".\"Field\" = '{field}' AND \"Publication\".\"Language\" = '{language}'"
                   )
            c.execute(sql)
            self.conn.commit()
            return c.fetchall()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)

    def show_by_category(self, category):
        try:
            c = self.conn.cursor()
            sql = (f"SELECT a.\"Name\", a.\"Surname\", COUNT(p.\"PublicationID\") AS PublicationCount "
                   f"FROM \"Author\" a "
                   f"INNER JOIN \"Publishing\" pb ON a.\"AuthorID\" = pb.\"AuthorID\" "
                   f"INNER JOIN \"Publication\" p ON pb.\"PublicationID\" = p.\"PublicationID\" "
                   f"INNER JOIN \"Collection\" c ON pb.\"ISSN\" = c.\"ISSN\" "
                   f"WHERE c.\"Category\" = '{category}' "
                   f"GROUP BY a.\"Name\", a.\"Surname\", c.\"Category\""
                   )
            c.execute(sql)
            self.conn.commit()
            return c.fetchall()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)

    def show_collection(self, issn):
        try:
            c = self.conn.cursor()
            sql = (f"SELECT P.\"Language\", COUNT(*) AS PublicationCount "
                   f"FROM \"Publication\" P "
                   f"INNER JOIN \"Publishing\" PA ON PA.\"PublicationID\" = P.\"PublicationID\" "
                   f"INNER JOIN \"Author\" as A ON A.\"AuthorID\" = PA.\"AuthorID\" "
                   f"INNER JOIN \"Collection\" C ON PA.\"ISSN\" = C.\"ISSN\" "
                   f"WHERE c.\"ISSN\" = {issn} "
                   f"GROUP BY P.\"Language\" "
                   f"ORDER BY PublicationCount"
                   )
            c.execute(sql)
            self.conn.commit()
            return c.fetchall()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)
