create table users (
    id integer primary key autoincrement,
    name varchar(30),
    age integer(11)
);

insert into users(name, age) values ("Test 1", 12);