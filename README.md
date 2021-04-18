# DBMS MySQL Project
## Commands
- Creating database
  create database ecart;
  use ecart;
- Creating tables
    ```sql
create table user(User_ID int auto_increment not null, email text not null, password text not null, house text, city varchar(45) not null, state varchar(45) not null, pincode int not null, first_name varchar(45) not null, last_name varchar(45) not null, Primary key(user_id));
create table product(product_ID int not null, price decimal not null, name varchar(45) not null, description varchar(500) not null, image text not null, stock int, category varchar(45) not null, primary key(product_id)); 
create table cart(product_id int not null, user_id int auto_increment not null, quantity int not null, price decimal not null, timestamp timestamp not null, Foreign key(product_id) references product(product_id), Foreign key(user_id) references user(user_id));
create table bill(price decimal not null, Invoice_no int not null, timestamp timestamp not null, user_id int auto_increment, product_id int, Primary key(Invoice_no), Foreign key(user_id) references user(user_id), Foreign key(product_id) references product(product_id));   
 SELECT * FROM USERS;
    SELECT userId, email FROM USERS;
    ```