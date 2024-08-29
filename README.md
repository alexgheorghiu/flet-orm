# A flet-orm Flet app

An example of a minimal Flet app with SqlAlchemy

Based on [Flet Tutorial - Crud With SqlAlchemy ORM SQLITE](https://www.youtube.com/watch?v=BdhDprSpIgU)

## DB setup

### Have SQLite3 installed
```bash
sudo apt-get install sqlite3
```

### Create database
```bash
mkdir db
touch db/dbperson.db
sqlite3 db/dbperson.db
```
then use the SQL file from documentation `documentation/schema.sql` to create tables

## Run app

### Install dependencies
```
pip3 install -r requirements
```

### Run it
To run the app:

```
flet run [app_directory]
```