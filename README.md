### Getting Started
- To start the project, execute the <i><b>run.py</b></i> file using Python 3

### Prerequisites
- Install Python 3.
- Create a virtual environment.
- Install required packages using the following commands:
  - pip install flask
  - pip install mysql-connector-python

### Screenshots
- The "assets" folder contains screenshots of the web app to give you a visual overview of its features.

### Main folder
- The "app" folder contains the main files responsible for the server's functionality.

## Queries
	create database myshop;
	use myshop;

## TABLES:
	company:
		create table company(company_name varchar(30), cash_balance decimal(10, 2));
		ALTER TABLE company add constraint positive_cash_balance CHECK (cash_balance > 0);
	item:
		create table item(item_id INT primary key, item_name varchar(255), qty int);
		ALTER TABLE item add constraint unique_item_name UNIQUE(item_name);
	item_qty:
		create table item_qty(item_id int, qty int, foreign key (item_id) references item(item_id) on delete cascade);
	purchase:
		create table purchase(purchase_id INT primary key,
		purchase_date DATE,
		purchase_time TIME,
		item_id INT,
		qty INT,
		rate int,
		amount decimal(10,2),
		foreign key (item_id) references item(item_id) on delete cascade);

	sales:
		create table sales( sales_id int primary key auto_increment, 
		sales_date date, 
		sales_time time, 
		item_id int, 
		qty int, 
		rate int, 
		amount int, 
		foreign key (item_id) references item(item_id) on delete cascade);

	users_list:
		create table users_list(user varchar(25), secretkey varchar(20));

## Note: Use this query before login: 
	insert into users_list(user, secretkey) values('admin','admin');
 	insert into company(company_name, cash_balance) values('Stationery Paradise', 0);

   	- For Linux users,
    	- I have exported my schema in a name "myshop.sql"
     	- Just create a database with any name, then goto Linux terminal (basically bash)
        - Change the working directory to the location of myshop.sql
	- mysql -u "username" -p "Your database Name" < myshop.sql
 	- Now use "mysql -u root -p" to enter into db in terminal
	

## Project Structure :

	/home/user/Projects/PettyShop
	├── app/
	│   ├── __init__.py
	│   ├── routes.py
	│   ├── templates/
	│   │	├── added_cash.html
	│   │	├── error.html
	│   │	├── index.html
	│   │	├── ItemAdded.html
	│   │	├── ItemExist.html
	│   │	├── main.html
	│   │	├── not_enough_balance.html
	│   │	├── purchased.html
	│   │	├── removeItem.html
	│   │	├── sell.html
	│   │	├── userAdded.html
	│   │	└── UserExist.html
	│   │
	│   └── static/
	│       ├── 1.jpg
	│       ├── 2.jpg
	│       ├── 4.jpg
	│       ├── 5.jpg
	│       ├── added_cash.css
	│       ├── corner.png
	│       ├── error.css
	│       ├── ItemAdded.css
	│       ├── ItemExist.css
	│       ├── main.css
	│       ├── purchased.css
	│       ├── removeItem.css
	│       ├── sell.css
	│       ├── style.css
	│       ├── style-bg1.jpg
	│       ├── userAdded.css
	│       └── userExist.css
	│
	├────── assets/
	│	├── Screenshots/
	│	│   ├── 1.png
	│	│   ├── 2.png
	│	│   ├── 3.png
	│	│   └── LoginPage.png
	│	│
	│	└── Presentation.pptx
	│
	└────── Exported Schema/
		└── myshop.sql 
