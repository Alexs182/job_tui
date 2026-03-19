
import datetime
import hashlib

import sqlalchemy 
from sqlalchemy import Column, String, Integer, DateTime, update
from sqlalchemy.orm import sessionmaker, declarative_base

BASE = declarative_base()

class SQLHandler():
    def __init__(self):
        self.db_engine = None

        self.connect()
        self.create_tables()

    def connect(self):
        conn_string = "sqlite:///database.db"
        self.db_engine = sqlalchemy.create_engine(conn_string)
        Session = sessionmaker()
        Session.configure(bind=self.db_engine)
        self.session = Session()

        print(f"Connected to: {conn_string}")

    def create_tables(self):
        BASE.metadata.create_all(
            self.db_engine, 
            BASE.metadata.tables.values(),
            checkfirst=True
        )

    def insert_job(self, job: dict[str, any]):
        
        job_string = ''.join(filter( None, [
            job.get('job_title', ""),
            job.get('company', ""),
            job.get('location', ""),
            job.get('list_date', "")
        ]))

        print(job_string)
        job_hash = hashlib.md5(job_string.encode('utf-8')).hexdigest()
        print(job_hash)
        existing = self.session.query(Jobs).filter_by(
            job_hash = job_hash
        ).first()

        if not existing:
            insert = Jobs(
                title = job["job_title"],
                company = job["company"],
                location = job["location"],
                link = job["job_link"],
                job_hash = job_hash,
                list_date = job["list_date"],
                seen_at = datetime.datetime.now()
            )
            self.session.add(insert)
            self.session.commit()
        else:
            print(f"{job_hash} all ready exisits, skipping insert.")

    def get_jobs(self):
        return (
            self.session.query(
                Jobs.id,
                Jobs.title, 
                Jobs.company, 
                Jobs.location,
                Jobs.link,
                Jobs.list_date
            )
            .all()
        )

    def get_job(self, job_id):
        return (
            self.session.query(
                Jobs.id,
                Jobs.title, 
                Jobs.company, 
                Jobs.location,
                Jobs.link,
                Jobs.list_date
            )
            .filter(Jobs.id == job_id)
            .first()
        )

class Jobs(BASE):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    salary = Column(String)
    link = Column(String)
    job_hash = Column(String)
    list_date = Column(String)
    seen_at = Column(DateTime)


