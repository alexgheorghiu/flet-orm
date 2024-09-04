CREATE USER 'fletorm'@'localhost' IDENTIFIED BY 'fletorm';

GRANT ALL PRIVILEGES ON fletorm.* TO 'fletorm'@'localhost' WITH GRANT OPTION;

create table `users` (
    `id` int(10) unsigned not null auto_increment,
    `name` varchar(30),
    `age` integer(11),
    primary key (`id`)
);

insert into users(name, age) values ("Test 1", 12);
insert into users(name, age) values ("Test 2", 22);
insert into users(name, age) values ("Test 3", 7);
insert into users(name, age) values ("Test 4", 37);