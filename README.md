# DBMS MySQL Project
## Commands
- Creating database
  ```sql
  CREATE DATABASE ecart;
  USE ecart;
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
    House TEXT NOT NULL, 
    City VARCHAR(45) NOT NULL, 
    State VARCHAR(45) NOT NULL, 
    Pincode INT NOT NULL, 
    PRIMARY KEY(User_ID)
  );

  CREATE TABLE product
  (
    Product_ID INT AUTO_INCREMENT NOT NULL, 
    Name TEXT NOT NULL, 
    Description TEXT, 
    Price DECIMAL(9,2) NOT NULL, 
    Stock INT NOT NULL, 
    Image TEXT NOT NULL, 
    Category VARCHAR(45) NOT NULL, 
    PRIMARY KEY(Product_ID)
  ); 

  CREATE TABLE cart
  (
    Product_ID INT NOT NULL, 
    User_ID INT NOT NULL, 
    Quantity INT NOT NULL, 
    FOREIGN KEY(Product_ID) REFERENCES product(Product_ID), 
    FOREIGN KEY(User_ID) REFERENCES user(User_ID)
  );
  
  CREATE TABLE sales
  (
    Invoice_no INT AUTO_INCREMENT NOT NULL, 
    Price DECIMAL(9,2) NOT NULL, 
    Timestamp TIMESTAMP NOT NULL, 
    User_ID INT NOT NULL, 
    Product_ID INT NOT NULL, 
    PRIMARY KEY(Invoice_no), 
    FOREIGN KEY(User_ID) REFERENCES user(User_ID),
    FOREIGN KEY(Product_ID) REFERENCES product(Product_ID)
  );   
  ```
  
  ## Queries
  
  This section conatins all triggers, procedures and functions. 
  
  ---
  ### Functions
  
* Function to check the availability of stock.

  ```sql
  delimiter $$
  create function cat_stock(n int)
  returns varchar(20)
  deterministic
  begin
  declare reqm varchar(20);
  if n < 12  then 
  set reqm = "ALERT : Low stock";
  elseif (n > 12 and n <=50) then 
  set reqm = “Adequate”;
  elseif n > 50 then
  set reqm = “More Than Enough”; 
  end if;
  return (reqm);
  end $$
  delimiter ;
  ```
  
* Function to check the pricing of available product. 
  
   ```sql
   delimiter $$
   create function cat_price(n int)
   returns varchar(20)
   deterministic
   begin
   declare price varchar(20);
   if n < 500  then 
   set price = “Low Price”;
   elseif (n > 500 and n <=2000) then 
   set price = “Medium Price”;
   elseif n > 2000 then
   set price = “High Price”; 
   end if;
   return (price);
   end $$
   delimiter ;
   ```

* Function to sort by category.

  ```sql
  DELIMITER //
  create procedure category(IN cat varchar(45))
  BEGIN
  set @sql_txt=concat('SELECT * FROM product WHERE category="',cat,'"');
  prepare stmt from @sql_txt;
  execute stmt;
  END //	
  DELIMITER ;
  ---

* Function to update and insert into cart.
  ```sql
  DELIMITER //
  create procedure user_cart(IN P_ID INT, IN U_ID INT, IN q INT)
  BEGIN
  DECLARE mycount INT;
  set mycount= (select count(*) from cart where Product_ID=P_ID AND User_ID=U_ID);
  if mycount>0
  then
  update cart set quantity=quantity+q where Product_ID=P_ID AND User_ID=U_ID;
  else
  insert into cart(Product_ID, User_ID, quantity) values(P_ID, U_ID, q);
  END if;
  END //
  DELIMITER ;
  ```
  
  ### Procedures
  
* Procedure to insert values into the designated table - 
  * User Table -
    ```sql
    Delimiter $$ 
    Create procedure insertUser(Fname VARCHAR(45), Lname VARCHAR(45), Email TEXT , Pwd TEXT, h TEXT, C VARCHAR(45), S VARCHAR(45), P INT)
    Begin
    Insert into user (first_name, last_name, email, password, house, city, state, pincode) values(fname , lname, email, pwd, h ,c,s,p );
    End $$
    Delimiter ;  
    ```
 
  * Product Table - To add into product table, given conditions that -
    * If product already exists in the cart, then increment by one
    * else insert new values;
    ```sql
    Delimiter $$ 
    Create procedure insertProduct( pid int,Name TEXT , Des TEXT, P DECIMAL(9,2), S INT, Image TEXT, Category VARCHAR(45))
    Begin
    If (exists(select * from product where product.product_id = pid) ) then
    Update product set quantity = quantity + 1 where product.product_id = pid ;
    Else 
    Insert into product(Product_ID, Name, Description, Price, Stock, Image, Category) values(name, des ,p ,s ,I ,c);
    End if;
    End $$
    Delimiter ;  

    ```
  * Cart Table - To be discussed and added.
  * Bill Table - To be discussed and added.

* Procedure to display values of the designated table - 
```sql
Delimiter $$ 
Create procedure displayTable( IN tname varchar (30))
Begin
Set @table = name;
Set @sql_text = concat (“select * from “, @table );
Prepare stmt from @sql_text;
Execute stmt;
End $$
Delimiter ;  
```
   
  
  ---
  
## Triggers

### To be added soon -
* Trigger to update the number of items present in the cart, everytime he/she/they/it/wtf add or remove an item from the cart  -
  ```sql
  ```
  
* Trigger to update the total amount of user, everytime he/she/they/it/wtf add or remove an item from the cart -
  ```sql
  ```
