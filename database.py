from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database:
    """
    This is the general encapsulating class having some SQLAlchemy specific features (engine and session).
    Also, it hides implementation details of database functions
    """

    def __init__(self, Base):
        """
        Initialization of SQLAlchemy engine and session
        """
        engine = create_engine("postgresql://postgres:230520@localhost:5432/postgres")
        session_class = sessionmaker(bind=engine)
        self.session = session_class()
        Base.metadata.create_all(engine)

    def generate_publishing(self, Author, Publication, Collection, Publishing, func, Date, num):
        num3 = round(num ** (1 / 3))
        for _ in range(num):
            g = Publishing(
                AuthorID=self.session.query(Author).order_by(func.random()).limit(num3).subquery().c.AuthorID,
                PublicationID=self.session.query(Publication).order_by(func.random()).limit(
                    num3).subquery().c.PublicationID,
                ISSN=self.session.query(Collection).order_by(func.random()).limit(num3).subquery().c.ISSN,
                Date='2000-01-01' + func.trunc(func.random() * 366 * 10).cast(Date)
            )
            self.session.add(g)
        self.session.commit()
