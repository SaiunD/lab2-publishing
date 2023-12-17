import random
import string
from datetime import datetime, timedelta
from random import random

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Date, func, literal_column, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from view import View
from database import Database

Base = declarative_base()


class Author(Base):
    __tablename__ = 'Author'
    AuthorID = Column(String, primary_key=True)
    Name = Column(String)
    Surname = Column(String)

    def __repr__(self):
        return "<Author(name='{}', surname='{}')>" \
            .format(self.Name, self.Surname)


class Publication(Base):
    __tablename__ = 'Publication'
    PublicationID = Column(String, primary_key=True)
    Name = Column(String)
    Language = Column(String)
    Field = Column(String)
    Pages = Column(Integer)

    def __repr__(self):
        return "<Publication(name='{}', language='{}', field={}, pages={})>" \
            .format(self.Name, self.Language, self.Field, self.Pages)

    def generate_random_language(self):
        languages = ['ukrainian', 'english', 'spanish', 'croatian', 'portuguese', 'french']
        return random.choice(languages)

    def generate_random_field(self):
        fields = ['medicine', 'biology', 'engineering', 'economics', 'physics', 'chemistry', 'history', 'philosophy']
        return random.choice(fields)


class Collection(Base):
    __tablename__ = 'Collection'
    ISSN = Column(Integer, primary_key=True)
    Name = Column(String)
    Type = Column(String)
    Category = Column(String)

    def __repr__(self):
        return "<Collection(ISSN='{}', name='{}', type={}, category={})>" \
            .format(self.ISSN, self.Name, self.Type, self.Category)

    def generate_random_type(self):
        types = ['e-book', 'paper book']
        return random.choice(types)

    def generate_random_category(self):
        categories = ['A', 'B', 'C']
        return random.choice(categories)


class Publishing(Base):
    __tablename__ = 'Publishing'
    AuthorID = Column(String, ForeignKey('Author.AuthorID'), primary_key=True)
    PublicationID = Column(String, ForeignKey('Publication.PublicationID'), primary_key=True)
    ISSN = Column(Integer, ForeignKey('Collection.ISSN'), primary_key=True)
    date = Column(Date)
    author = relationship(Author, backref="authors")
    publication = relationship(Publication, backref="publications")
    collection = relationship(Collection, backref="collections")

    def __repr__(self):
        return "<Publishing(date='{}')>" \
            .format(self.date)


class Model:
    def __init__(self):
        self.view = View()
        self.DB = Database(Base)

    def get_all(self, table_name):
        t = self.get_class(table_name)
        return self.DB.session.query(t).all()

    def add_data(self, table_name, data):
        if table_name == "Author":
            t = Author(
                AuthorID=data[0],
                Name=data[1],
                Surname=data[2]
            )
        elif table_name == "Publication":
            t = Publication(
                PublicationID=data[0],
                Name=data[1],
                Language=data[2],
                Field=data[3],
                Pages=data[4]
            )
        elif table_name == "Collection":
            t = Collection(
                ISSN=data[0],
                Name=data[1],
                Type=data[2],
                Category=data[3]
            )
        elif table_name == "Publishing":
            t = Publishing(
                AuthorID=data[0],
                PublicationID=data[1],
                ISSN=data[2],
                date=data[3]
            )
        self.DB.session.add(t)
        self.DB.session.commit()
        print("Added successfully!")

    def update_data(self, table_name, data, condition_column, condition_value):
        if table_name == "Author":
            u = self.DB.session.query(Author).filter_by(AuthorID=condition_value).first()
            u.Name = data[1]
            u.Surname = data[2]
        elif table_name == "Publication":
            u = self.DB.session.query(Publication).filter_by(PublicationID=condition_value).first()
            u.Name = data[1]
            u.Language = data[2]
            u.Field = data[3]
            u.Pages = data[4]
        elif table_name == "Collection":
            u = self.DB.session.query(Collection).filter_by(ISSN=condition_value).first()
            u.Name = data[1]
            u.Type = data[2]
            u.Category = data[3]
        self.DB.session.commit()
        self.view.show_message("Updated successfully!")

    def get_class(self, table_name):
        if table_name == "Author":
            return Author
        elif table_name == "Publication":
            return Publication
        elif table_name == "Collection":
            return Collection
        elif table_name == "Publishing":
            return Publishing

    def delete_data(self, table_name, cond, val):
        t = self.get_class(table_name)
        d = self.DB.query(t).filter(
            getattr(t, cond) == val).first()

        # Перевіримо, чи знайдено запис
        if d:
            # Видалимо запис
            self.DB.session.delete(d)

            # Збережемо зміни
            self.DB.session.commit()
            print("Дані видалено успішно.")
        else:
            print("Запис не знайдено.")

    def delete_data_publishing(self, table_name, cond1, val1, cond2, val2, cond3, val3):
        d = (
            self.DB.session.query(Publishing)
            .filter(getattr(Publishing, cond1) == val1)
            .filter(getattr(Publishing, cond2) == val2)
            .filter(getattr(Publishing, cond3) == val3)
            .first()
        )
        if d:
            # Видалимо запис
            self.DB.session.delete(d)

            # Збережемо зміни
            self.DB.session.commit()
            print("Дані видалено успішно.")
        else:
            print("Запис не знайдено.")

    def random_string(length):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))

    def generate_random_date(self):
        start_date = datetime(2000, 1, 1)
        random_days = timedelta(days=int(random() * 366 * 10))
        return start_date + random_days

    def generate_data(self, table_name, num):
        try:
            if table_name == "Author":
                for _ in range(num):
                    author = Author(
                        AuthorID=func.md5(func.cast(func.random(), sqlalchemy.Text)).label('AuthorID'),
                        Name=func.concat(
                            literal_column("CAST(trunc(random() * 26) + 65 AS INTEGER)"),
                            literal_column("CAST(trunc(random() * 26) + 97 AS INTEGER)"),
                            literal_column("CAST(trunc(random() * 26) + 97 AS INTEGER)")
                        ).label('Name'),
                        Surname=func.concat(
                            literal_column("CAST(trunc(random() * 26) + 65 AS INTEGER)"),
                            literal_column("CAST(trunc(random() * 26) + 97 AS INTEGER)"),
                            literal_column("CAST(trunc(random() * 26) + 97 AS INTEGER)")
                        ).label('Surname')
                    )
                    self.DB.session.add(author)
            elif table_name == "Publication":
                for _ in range(num):
                    publication = Publication(
                        PublicationID=func.md5(func.cast(func.random(), sqlalchemy.Text)).label('PublicationID'),
                        Name=func.concat(
                            literal_column("CAST(trunc(random() * 25) + 65 AS INTEGER)"),
                            literal_column("CAST(trunc(random() * 26) + 97 AS INTEGER)"),
                            literal_column("CAST(trunc(random() * 26) + 97 AS INTEGER)"),
                            literal_column("CAST(trunc(random() * 25) + 65 AS INTEGER)"),
                            literal_column("CAST(trunc(random() * 26) + 97 AS INTEGER)"),
                            literal_column("CAST(trunc(random() * 26) + 97 AS INTEGER)")
                        ).label('Name'),
                        Language=Publication.generate_random_language(Base),
                        Field=Publication.generate_random_field(Base),
                        Pages=func.floor(func.random() * 100)
                    )
                    self.DB.session.add(publication)
            elif table_name == "Collection":
                for _ in range(num):
                    collection = Collection(
                        ISSN=func.floor(func.random() * 100000000) + 1,
                        Name=func.concat(
                            func.cast(func.trunc(65 + func.random() * 25), String),
                            func.cast(func.trunc(97 + func.random() * 26), String),
                            func.cast(func.trunc(97 + func.random() * 26), String),
                            func.cast(func.trunc(65 + func.random() * 25), String),
                            func.cast(func.trunc(97 + func.random() * 26), String),
                            func.cast(func.trunc(97 + func.random() * 26), String), ),
                        Type=Collection.generate_random_type(Base),
                        Category=Collection.generate_random_category(Base)
                    )
                    self.DB.session.add(collection)

            elif table_name == "Publishing":
                num3 = round(num ** (1 / 3))
                sql = text(
                    "INSERT INTO \"Publishing\" "
                    "SELECT pr.\"AuthorID\", pr.\"PublicationID\", pr.\"ISSN\", pr.\"Date\" "
                    "FROM \"Publishing\" RIGHT JOIN "
                    "(SELECT DISTINCT "
                    "t1.\"AuthorID\", "
                    "t2.\"PublicationID\", "
                    "t3.\"ISSN\", "
                    "'2000-01-01'::date + trunc(random() * 366 * 10)::int as \"Date\" "
                    "FROM "
                    "(SELECT \"AuthorID\", row_number() OVER (ORDER BY random()) as rn FROM \"Author\" order by random() LIMIT :num3) t1, "
                    "(SELECT \"PublicationID\", row_number() OVER (ORDER BY random()) as rn FROM \"Publication\" order by random() LIMIT :num3) t2, "
                    "(SELECT \"ISSN\", row_number() OVER (ORDER BY random()) as rn FROM \"Collection\" order by random() LIMIT :num3) t3 "
                    "LIMIT :num) pr "
                    "ON \"Publishing\".\"AuthorID\" = pr.\"AuthorID\" "
                    "AND \"Publishing\".\"PublicationID\" = pr.\"PublicationID\" "
                    "AND \"Publishing\".\"ISSN\" = pr.\"ISSN\" "
                    "WHERE \"Publishing\".\"AuthorID\" IS NULL and \"Publishing\".\"PublicationID\" is null and \"Publishing\".\"ISSN\" is null"
                )

                self.DB.session.execute(sql, {'num3': num3, 'num': num})

            self.DB.session.commit()

        except SQLAlchemyError as e:
            self.DB.session.rollback()
            print(e)

    def show_by_field_language(self, field, language):
        try:
            result = (
                self.DB.session.query(
                    Author.Name.label('author_name'),
                    Author.Surname.label('author_surname'),
                    Publication.Name.label('pub_name'),
                    Publishing.date
                )
                .join(Publishing, Author.AuthorID == Publishing.AuthorID)
                .join(Publication, Publishing.PublicationID == Publication.PublicationID)
                .filter(Publication.Field == field, Publication.Language == language)
                .all()
            )
            return result
        except SQLAlchemyError as e:
            # Обробка помилок
            self.DB.session.rollback()
            print(e)

    def show_by_category(self, category):
        try:
            result = (
                self.DB.session.query(
                    Author.Name.label('author_name'),
                    Author.Surname.label('author_surname'),
                    func.count(Publication.PublicationID).label('PublicationCount')
                )
                .join(Publishing, Author.AuthorID == Publishing.AuthorID)
                .join(Publication, Publishing.PublicationID == Publication.PublicationID)
                .join(Collection, Publishing.ISSN == Collection.ISSN)
                .filter(Collection.Category == category)
                .group_by(Author.Name, Author.Surname, Collection.Category)
                .all()
            )
            return result
        except SQLAlchemyError as e:
            # Обробка помилок
            self.DB.session.rollback()
            print(e)

    def show_collection(self, issn):
        try:
            result = (
                self.DB.session.query(
                    Publication.Language.label('Language'),
                    func.count().label('PublicationCount')
                )
                .join(Publishing, Publication.PublicationID == Publishing.PublicationID)
                .join(Author, Publishing.AuthorID == Author.AuthorID)
                .join(Collection, Publishing.ISSN == Collection.ISSN)
                .filter(Collection.ISSN == issn)
                .group_by(Publication.Language)
                .order_by(func.count())
                .all()
            )
            return result
        except SQLAlchemyError as e:
            # Обробка помилок
            self.DB.session.rollback()
            print(e)
