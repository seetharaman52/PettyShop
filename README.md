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

### Project Structure
- The "app" folder contains the main files responsible for the server's functionality.

### Queries
## DATABASE:
	create database myshop;
	use myshop;

## TABLE'S:
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
	insert into users_list(user, secretkey) values('admin','admin')
