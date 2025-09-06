CREATE TABLE user(
	user_id INTEGER PRIMARY KEY,
	user_name VARCHAR(50) NOT NULL,
	user_email VARCHAR(255) NOT NULL UNIQUE,
	password_hashed VARCHAR(255) NOT NULL,
	salt VARCHAR(255) NOT NULL,
	registration_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE account(
	account_id INTEGER PRIMARY KEY,
	user_id INTEGER NOT NULL,
	bank_name VARCHAR(50) NOT NULL,
	account_name VARCHAR(50) NOT NULL,
	account_type_id INTEGER NOT NULL,
	currency_id INTEGER NOT NULL,
	FOREIGN KEY(user_id) REFERENCES user(user_id),
	FOREIGN KEY(account_type_id) REFERENCES account_type(account_type_id)
);

CREATE TABLE account_type(
	account_type_id INTEGER PRIMARY KEY,
	type_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE vendor(
	vendor_id INTEGER PRIMARY KEY,
	vendor_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE transactions(
	transaction_id INTEGER PRIMARY KEY,
	account_id INTEGER NOT NULL,
	vendor_id INTEGER NOT NULL,
	transaction_date DATETIME NOT NULL,
	description TEXT,
	amount REAL,
	currency_id INTEGER NOT NULL,
	category_id INTEGER NOT NULL,
	FOREIGN KEY (account_id) REFERENCES account(account_id),
	FOREIGN KEY (vendor_id) REFERENCES vendor(vendor_id),
	FOREIGN KEY (currency_id) REFERENCES currency(currency_id),
	FOREIGN KEY (category_id) REFERENCES category(category_id)
);

CREATE TABLE category(
	category_id INTEGER PRIMARY KEY,
	category_name VARCHAR(50) NOT NULL UNIQUE,
	parent_category_id INTEGER,
	description TEXT,
	FOREIGN KEY (parent_category_id) REFERENCES category(category_id)
);

CREATE TABLE currency(
	currency_id INTEGER PRIMARY KEY,
	currency_name VARCHAR(10) NOT NULL UNIQUE,
	currency_value REAL
);
