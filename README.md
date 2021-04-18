# DBMS MySQL Project
## Commands
- Creating database
  ```sql
  CREATE database ecart;
  use ecart;
  ```
- Creating tables
  ```sql
  CREATE TABLE user
  (
    User_ID INT AUTO_INCREMENT NOT NULL, 
    First_name VARCHAR(45) NOT NULL, 
    Last_name VARCHAR(45) NOT NULL, 
    Email TEXT NOT NULL, 
    Password TEXT NOT NULL,
    house TEXT, 
    City VARCHAR(45) NOT NULL, 
    State VARCHAR(45) NOT NULL, 
    Pincode INT NOT NULL, 
    PRIMARY KEY(User_ID)
  );

  CREATE TABLE product
  (
    Product_ID INT NOT NULL, 
    Price DECIMAL NOT NULL, 
    Name VARCHAR(45) NOT NULL, 
    Description VARCHAR(500) NOT NULL, 
    Image TEXT NOT NULL, 
    Stock INT, 
    Category VARCHAR(45) NOT NULL, 
    PRIMARY KEY(Product_id)
  ); 

  CREATE TABLE cart
  (
    Product_id INT NOT NULL, 
    User_id INT AUTO_INCREMENT NOT NULL, 
    Quantity INT NOT NULL, 
    Price DECIMAL NOT NULL, 
    Timestamp TIMESTAMP NOT NULL, 
    FOREIGN KEY(Product_id) REFERENCES product(Product_id), 
    FOREIGN KEY(User_id) REFERENCES user(User_id)
  );
  
  CREATE TABLE bill
  (
    Price DECIMAL NOT NULL, 
    Invoice_no INT NOT NULL, 
    Timestamp TIMESTAMP NOT NULL, 
    User_id INT AUTO_INCREMENT NOT NULL, 
    Product_id INT NOT NULL, 
    PRIMARY KEY(Invoice_no), 
    FOREIGN KEY(User_id) REFERENCES user(User_id),
    FOREIGN KEY(Product_id) REFERENCES product(Product_id)
  );   
  ```
