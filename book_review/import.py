#importing necassary libraries
import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#databse connect
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#creating tables
db.execute("create table books(isbn text primary key, title text not null, author text not null, year integer not null)")
db.execute("create table username(id serial primary key, name text not null, password text not null)")
db.execute("create table review(isbn text not null, name text not null, star smallint not null, review text)")

file = open("books.csv")
reader = csv.reader(file)

for isbn,title,author, year in reader:
    if year == "year":
        continue
    db.execute("insert into books(isbn,title,author,year) values(:isbn,:title,:author,:year)", {"isbn":isbn, "title":title, "author":author, "year":int(year)})
    db.commit()
