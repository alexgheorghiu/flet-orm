create table users (
    id integer primary key autoincrement,
    name varchar(30),
    age integer(11)
);

insert into users(name, age) values ("Test 1", 12);
insert into users(name, age) values ("Test 2", 22);
insert into users(name, age) values ("Test 3", 7);
insert into users(name, age) values ("Test 4", 37);
