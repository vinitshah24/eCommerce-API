DROP DATABASE IF EXISTS flask_rest_db;
CREATE DATABASE flask_rest_db;

-- DESCRIBE flask_rest_db.users;
-- DESCRIBE flask_rest_db.products;
-- DESCRIBE flask_rest_db.orders;

SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, 
	REFERENCED_TABLE_NAME,
	REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE REFERENCED_TABLE_SCHEMA = 'flask_rest_db' AND
	REFERENCED_TABLE_NAME = 'users' OR REFERENCED_TABLE_NAME = 'products';
    
SELECT * FROM flask_rest_db.products;
SELECT (products.cost + 10) FROM flask_rest_db.products;

SELECT * FROM flask_rest_db.orders;

SELECT
	orders.product_public_id, products.name, products.company, products.cost,
	orders.user_public_id, users.first_name, users.last_name
FROM flask_rest_db.orders
INNER JOIN flask_rest_db.products 
	ON orders.product_public_id = products.public_id
INNER JOIN flask_rest_db.users 
	ON orders.user_public_id = users.public_id;

SELECT * FROM flask_rest_db.users;
SELECT * FROM flask_rest_db.token_blacklist;