drop database if exists tuition;
create database tuition;
use tuition;

create table tutee (
	email varchar(64) not null primary key,
    password varchar(64) not null,
    fullname varchar(64) not null,
    gender char(1) not null,
    age int not null,
    address varchar(64) not null,
    contact_number varchar(8) not null
);

INSERT INTO tutee(email, password, fullname, gender, age, address, contact_number) VALUES 
    ("maurice@gmail.com","password","Maurice Lim", "M", 23, "blk123", "87654321");