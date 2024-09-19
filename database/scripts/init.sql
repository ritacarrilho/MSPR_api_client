CREATE TABLE Customers(
   id_customer INT AUTO_INCREMENT,
   name VARCHAR(80) NOT NULL,
   created_at DATETIME NOT NULL,
   updated_at DATETIME,
   username VARCHAR(80) NOT NULL,
   first_name VARCHAR(80) NOT NULL,
   last_name VARCHAR(80) NOT NULL,
   phone VARCHAR(15),
   email VARCHAR(100) NOT NULL,
   password_hash VARCHAR(255) NOT NULL,
   last_login DATETIME NOT NULL,
   customer_type INT NOT NULL,
   failed_login_attempts INT DEFAULT 0,
   preferred_contact_method INT,
   opt_in_marketing BOOLEAN,
   loyalty_points INT NOT NULL DEFAULT 0,
   PRIMARY KEY(id_customer),
   UNIQUE(email)
);

CREATE TABLE Companies(
   id_company INT AUTO_INCREMENT,
   company_name VARCHAR(80) NOT NULL,
   siret VARCHAR(15) NOT NULL,
   address VARCHAR(255) NOT NULL,
   postal_code VARCHAR(10) NOT NULL,
   city VARCHAR(90) NOT NULL,
   phone VARCHAR(15),
   email VARCHAR(100),
   PRIMARY KEY(id_company),
   UNIQUE(siret),
   UNIQUE(email)
);

-- CREATE TABLE Customer_Feedback(
--    id_feedback INT AUTO_INCREMENT,
--    product_id INT NOT NULL,
--    rating INT,
--    comment VARCHAR(50),
--    created_at DATETIME,
--    id_customer INT NOT NULL,
--    PRIMARY KEY(id_feedback),
--    FOREIGN KEY(id_customer) REFERENCES Customers(id_customer)
-- );

CREATE TABLE Notifications(
   id_notification INT AUTO_INCREMENT,
   message VARCHAR(255) NOT NULL,
   date_created DATETIME,
   is_read BOOLEAN DEFAULT FALSE,
   type INT NOT NULL,
   id_customer INT NOT NULL,
   PRIMARY KEY(id_notification),
   FOREIGN KEY(id_customer) REFERENCES Customers(id_customer)
);

CREATE TABLE Addresses(
   id_address INT AUTO_INCREMENT,
   address_line1 VARCHAR(255) NOT NULL,
   address_line2 VARCHAR(255),
   city VARCHAR(100) NOT NULL,
   state VARCHAR(100),
   postal_code VARCHAR(20) NOT NULL,
   country VARCHAR(100) NOT NULL,
   address_type INT NOT NULL,
   created_at DATETIME NOT NULL,
   updated_at VARCHAR(50),
   id_customer INT NOT NULL,
   PRIMARY KEY(id_address),
   FOREIGN KEY(id_customer) REFERENCES Customers(id_customer)
);

CREATE TABLE Login_Logs(
   id_log INT AUTO_INCREMENT,
   login_time DATETIME NOT NULL,
   ip_address VARCHAR(45),
   user_agent VARCHAR(255),
   id_customer INT NOT NULL,
   PRIMARY KEY(id_log),
   FOREIGN KEY(id_customer) REFERENCES Customers(id_customer)
);

CREATE TABLE Customer_Companies(
   id_customer INT AUTO_INCREMENT,
   id_company INT,
   PRIMARY KEY(id_customer, id_company),
   FOREIGN KEY(id_customer) REFERENCES Customers(id_customer),
   FOREIGN KEY(id_company) REFERENCES Companies(id_company)
);

CREATE TABLE Customer_Feedback(
   id_feedback INT AUTO_INCREMENT,
   product_id INT NOT NULL,
   rating INT,
   comment VARCHAR(50),
   created_at DATETIME,
   id_customer INT NOT NULL,
   PRIMARY KEY(id_feedback),
   FOREIGN KEY(id_customer) REFERENCES Customers(id_customer)
);

INSERT INTO Customers (name, created_at, updated_at, username, first_name, last_name, phone, email, password_hash, last_login, customer_type, failed_login_attempts, preferred_contact_method, opt_in_marketing, loyalty_points) 
VALUES 
('CaféLover', NOW(), NULL, 'cafefan123', 'Jean', 'Dupont', '612345678', 'jean.dupont@example.com', '$2b$12$sBu.zaAskPVy8QUUmHUPPu9vi33B0SXLzOe9qO5dJ2G5qQwVDJ4Ve', NOW(), 2, 0, 1, TRUE, 120),
('ProBarista', NOW(), NULL, 'barista_pro', 'Marie', 'Durand', '698765432', 'marie.durand@procoffee.com', '$2b$12$sBu.zaAskPVy8QUUmHUPPu9vi33B0SXLzOe9qO5dJ2G5qQwVDJ4Ve', NOW(), 2, 0, 2, TRUE, 300),
('toto', NOW(), NULL, 'kawa', 'kawa', 'kawa', '698765123', 'toto@email.com', '$2b$12$sBu.zaAskPVy8QUUmHUPPu9vi33B0SXLzOe9qO5dJ2G5qQwVDJ4Ve', NOW(), 2, 0, 2, TRUE, 300),
('admin', NOW(), NULL, 'kawa', 'kawa', 'kawa', '698765123', 'admin@email.com', '$2b$12$sBu.zaAskPVy8QUUmHUPPu9vi33B0SXLzOe9qO5dJ2G5qQwVDJ4Ve', NOW(), 1, 0, 2, TRUE, 300);

INSERT INTO Companies (company_name, siret, address, postal_code, city, phone, email) 
VALUES 
('Coffee Distributors Inc.', '12345678901234', '10 Rue de la Paix', '75002', 'Paris', '155567788', 'contact@coffee-distributors.com'),
('Café Express SARL', '98765432109876', '5 Boulevard des Capucines', '75009', 'Paris', '177889988', 'info@cafeexpress.fr');

INSERT INTO Customer_Feedback (product_id, rating, comment, created_at, id_customer) 
VALUES 
(1, 5, 'Amazing coffee, will buy again!', NOW(), 1),
(2, 4, 'Good quality but a bit pricey.', NOW(), 2);

INSERT INTO Notifications (message, date_created, is_read, type, id_customer) 
VALUES 
('Your order has been shipped!', NOW(), FALSE, 1, 1),
('New product available: Organic Arabica!', NOW(), TRUE, 2, 2);

INSERT INTO Addresses (address_line1, address_line2, city, state, postal_code, country, address_type, created_at, updated_at, id_customer) 
VALUES 
('15 Rue des Lilas', NULL, 'Lyon', 'Auvergne-Rhône-Alpes', '69003', 'France', 1, NOW(), NULL, 1),
('100 Avenue des Champs-Élysées', 'Apt. 12B', 'Paris', NULL, '75008', 'France', 2, NOW(), NULL, 2);

INSERT INTO Login_Logs (login_time, ip_address, user_agent, id_customer) 
VALUES 
(NOW(), '192.168.1.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 1),
(NOW(), '192.168.1.2', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)', 2);

INSERT INTO Customer_Companies (id_customer, id_company) 
VALUES 
(1, 1),
(2, 2);