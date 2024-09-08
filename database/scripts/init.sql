-- Customers table
CREATE TABLE IF NOT EXISTS customers(
   id_customer INT AUTO_INCREMENT,
   created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
   name VARCHAR(80) NOT NULL,
   username VARCHAR(80) NOT NULL,
   first_name VARCHAR(80) NOT NULL,
   last_name VARCHAR(80) NOT NULL,
   postal_code VARCHAR(10) NOT NULL,
   city VARCHAR(90) NOT NULL,
   PRIMARY KEY(id_customer)
);

-- Companies table (fix: only id_company has AUTO_INCREMENT)
CREATE TABLE IF NOT EXISTS companies(
   id_company INT AUTO_INCREMENT,
   id_customer INT,
   company_name VARCHAR(80) NOT NULL,
   PRIMARY KEY(id_company),  -- id_company as the primary key with AUTO_INCREMENT
   FOREIGN KEY(id_customer) REFERENCES customers(id_customer) ON DELETE CASCADE
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders(
   id_order INT AUTO_INCREMENT,
   id_customer INT,
   created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY(id_order),  -- id_order as the primary key with AUTO_INCREMENT
   FOREIGN KEY(id_customer) REFERENCES customers(id_customer) ON DELETE CASCADE
);

-- Profiles table
CREATE TABLE IF NOT EXISTS profiles(
   id_profile INT AUTO_INCREMENT,
   first_name VARCHAR(80) NOT NULL,
   last_name VARCHAR(50) NOT NULL,
   id_customer INT NOT NULL,
   PRIMARY KEY(id_profile),
   FOREIGN KEY(id_customer) REFERENCES customers(id_customer) ON DELETE CASCADE
);

-- Insert sample data into customers table
INSERT INTO customers (created_at, name, username, first_name, last_name, postal_code, city)
VALUES 
('2023-08-29 16:28:58', 'Jan Schiller', 'Kailee.Greenholt73', 'Keven', 'Kris', '61432-1180', 'St. Joseph'),
('2023-08-30 12:38:41', 'Joanne Breitenberg', 'Lue98', 'Robbie', 'Oberbrunner', '24609-3023', 'San Tan Valley'),
('2023-08-30 13:26:04', 'Bridget Torp', 'Bobbie_Dickens', 'Bradford', 'Kuphal', '48348', 'East Toniton'),
('2023-08-30 02:44:11', 'Gina Dicki', 'Madelynn73', 'Freeman', 'Kessler', '47788', 'Boganfort'),
('2023-08-29 16:48:46', 'Jeannie Bailey', 'Jordi.Marks', 'Doyle', 'Beier', '56546', 'Pharr'),
('2023-08-29 14:53:59', 'Rose Nolan', 'Kaya_Hintz38', 'Fern', 'Klocko', '60926-4558', 'New Novaberg'),
('2023-08-29 22:26:29', 'Miss Darrell Simonis', 'Johan_Kihn', 'Guido', 'West', '30273-1807', 'Autumnton'),
('2023-08-30 08:38:40', 'Tony Grimes', 'Nella.Franey', 'Alfonzo', 'Bergnaum', '31080', 'Elmhurst'),
('2023-08-30 10:18:08', 'Wendell Stoltenberg DDS', 'Aaliyah.Walter', 'Dillon', 'Leuschke', '70883', 'West Hildafort'),
('2023-08-29 18:59:05', 'Miss Leonard Russel', 'Dakota.Cremin', 'Garfield', 'Koss', '91773', 'Georgiannastead');

-- Insert sample data into companies table
INSERT INTO companies (id_customer, company_name)
VALUES 
(1, 'Bechtelar LLC'),
(2, 'Rowe - Robel'),
(3, 'Fritsch, Bayer and Sanford'),
(4, 'Koepp, Abernathy and Wisozk'),
(5, 'Crona Group'),
(6, 'Pollich, Gorczany and Wolf'),
(7, 'Smitham, Labadie and Kovacek'),
(8, 'Luettgen and Sons'),
(9, 'Willms, Purdy and Gorczany'),
(10, 'Stamm, Lubowitz and Ryan');

-- Insert sample data into Orders table
INSERT INTO orders (id_customer, created_at)
VALUES 
(1, '2023-08-30 08:35:27'),
(1, '2023-08-30 05:22:50'),
(2, '2023-08-29 19:21:39'),
(2, '2023-08-30 10:01:12'),
(3, '2023-08-29 21:22:06'),
(3, '2023-08-29 22:22:50'),
(4, '2023-08-30 13:52:46'),
(4, '2023-08-30 08:07:15'),
(5, '2023-08-29 16:24:29'),
(5, '2023-08-30 12:53:48');

-- Insert sample data into Profiles table
INSERT INTO profiles (first_name, last_name, id_customer)
VALUES 
('Mitchell', 'Carter', 1),
('Chauncey', 'Borer', 2),
('Noah', 'Veum', 3),
('Rachael', 'Welch', 4),
('Annamae', 'Daugherty', 5),
('Celia', 'Sanford', 6),
('Guadalupe', 'Kris', 7),
('Laron', 'Satterfield', 8),
('Addie', 'Ondricka', 9),
('Santiago', 'Willms', 10);