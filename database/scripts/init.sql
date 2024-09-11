-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : lun. 09 sep. 2024 à 17:02
-- Version du serveur : 8.0.31
-- Version de PHP : 8.1.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `customer_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `addresses`
--

DROP TABLE IF EXISTS `addresses`;
CREATE TABLE IF NOT EXISTS `addresses` (
  `id_address` int NOT NULL AUTO_INCREMENT,
  `address_line1` varchar(255) NOT NULL,
  `address_line2` varchar(255) DEFAULT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(100) DEFAULT NULL,
  `postal_code` varchar(20) NOT NULL,
  `country` varchar(100) NOT NULL,
  `address_type` int NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` varchar(50) DEFAULT NULL,
  `id_customer` int NOT NULL,
  PRIMARY KEY (`id_address`),
  KEY `id_customer` (`id_customer`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `addresses`
--

INSERT INTO `addresses` (`id_address`, `address_line1`, `address_line2`, `city`, `state`, `postal_code`, `country`, `address_type`, `created_at`, `updated_at`, `id_customer`) VALUES
(1, '15 Rue des Lilas', NULL, 'Lyon', 'Auvergne-Rhône-Alpes', '69003', 'France', 1, '2024-09-09 19:02:12', NULL, 1),
(2, '100 Avenue des Champs-Élysées', 'Apt. 12B', 'Paris', NULL, '75008', 'France', 2, '2024-09-09 19:02:12', NULL, 2);

-- --------------------------------------------------------

--
-- Structure de la table `companies`
--

DROP TABLE IF EXISTS `companies`;
CREATE TABLE IF NOT EXISTS `companies` (
  `id_company` int NOT NULL AUTO_INCREMENT,
  `company_name` varchar(80) NOT NULL,
  `siret` varchar(15) NOT NULL,
  `address` varchar(255) NOT NULL,
  `postal_code` varchar(10) NOT NULL,
  `city` varchar(90) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_company`),
  UNIQUE KEY `siret` (`siret`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `companies`
--

INSERT INTO `companies` (`id_company`, `company_name`, `siret`, `address`, `postal_code`, `city`, `phone`, `email`) VALUES
(1, 'Coffee Distributors Inc.', '12345678901234', '10 Rue de la Paix', '75002', 'Paris', '155567788', 'contact@coffee-distributors.com'),
(2, 'Café Express SARL', '98765432109876', '5 Boulevard des Capucines', '75009', 'Paris', '177889988', 'info@cafeexpress.fr');

-- --------------------------------------------------------

--
-- Structure de la table `customers`
--

DROP TABLE IF EXISTS `customers`;
CREATE TABLE IF NOT EXISTS `customers` (
  `id_customer` int NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `username` varchar(80) NOT NULL,
  `first_name` varchar(80) NOT NULL,
  `last_name` varchar(80) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `last_login` datetime NOT NULL,
  `customer_type` int NOT NULL,
  `failed_login_attempts` int DEFAULT '0',
  `preferred_contact_method` int DEFAULT NULL,
  `opt_in_marketing` tinyint(1) DEFAULT NULL,
  `loyalty_points` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_customer`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `customers`
--

INSERT INTO `customers` (`id_customer`, `name`, `created_at`, `updated_at`, `username`, `first_name`, `last_name`, `phone`, `email`, `password_hash`, `last_login`, `customer_type`, `failed_login_attempts`, `preferred_contact_method`, `opt_in_marketing`, `loyalty_points`) VALUES
(1, 'CaféLover', '2024-09-09 19:02:12', NULL, 'cafefan123', 'Jean', 'Dupont', '612345678', 'jean.dupont@example.com', 'hashedpassword123', '2024-09-09 19:02:12', 1, 0, 1, 1, 120),
(2, 'ProBarista', '2024-09-09 19:02:12', NULL, 'barista_pro', 'Marie', 'Durand', '698765432', 'marie.durand@procoffee.com', 'hashedpassword456', '2024-09-09 19:02:12', 2, 0, 2, 1, 300);

-- --------------------------------------------------------

--
-- Structure de la table `customer_companies`
--

DROP TABLE IF EXISTS `customer_companies`;
CREATE TABLE IF NOT EXISTS `customer_companies` (
  `id_customer` int NOT NULL AUTO_INCREMENT,
  `id_company` int NOT NULL,
  PRIMARY KEY (`id_customer`,`id_company`),
  KEY `id_company` (`id_company`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `customer_companies`
--

INSERT INTO `customer_companies` (`id_customer`, `id_company`) VALUES
(2, 1),
(2, 2);

-- --------------------------------------------------------

--
-- Structure de la table `customer_feedback`
--

DROP TABLE IF EXISTS `customer_feedback`;
CREATE TABLE IF NOT EXISTS `customer_feedback` (
  `id_feedback` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `rating` int DEFAULT NULL,
  `comment` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `id_customer` int NOT NULL,
  PRIMARY KEY (`id_feedback`),
  KEY `id_customer` (`id_customer`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `customer_feedback`
--

INSERT INTO `customer_feedback` (`id_feedback`, `product_id`, `rating`, `comment`, `created_at`, `id_customer`) VALUES
(1, 1, 5, 'Amazing coffee, will buy again!', '2024-09-09 19:02:12', 1),
(2, 2, 4, 'Good quality but a bit pricey.', '2024-09-09 19:02:12', 2);

-- --------------------------------------------------------

--
-- Structure de la table `login_logs`
--

DROP TABLE IF EXISTS `login_logs`;
CREATE TABLE IF NOT EXISTS `login_logs` (
  `id_log` int NOT NULL AUTO_INCREMENT,
  `login_time` datetime NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` varchar(255) DEFAULT NULL,
  `id_customer` int NOT NULL,
  PRIMARY KEY (`id_log`),
  KEY `id_customer` (`id_customer`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `login_logs`
--

INSERT INTO `login_logs` (`id_log`, `login_time`, `ip_address`, `user_agent`, `id_customer`) VALUES
(1, '2024-09-09 19:02:12', '192.168.1.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 1),
(2, '2024-09-09 19:02:12', '192.168.1.2', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)', 2);

-- --------------------------------------------------------

--
-- Structure de la table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
CREATE TABLE IF NOT EXISTS `notifications` (
  `id_notification` int NOT NULL AUTO_INCREMENT,
  `message` varchar(255) NOT NULL,
  `date_created` datetime DEFAULT NULL,
  `is_read` tinyint(1) DEFAULT '0',
  `type` int NOT NULL,
  `id_customer` int NOT NULL,
  PRIMARY KEY (`id_notification`),
  KEY `id_customer` (`id_customer`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `notifications`
--

INSERT INTO `notifications` (`id_notification`, `message`, `date_created`, `is_read`, `type`, `id_customer`) VALUES
(1, 'Your order has been shipped!', '2024-09-09 19:02:12', 0, 1, 1),
(2, 'New product available: Organic Arabica!', '2024-09-09 19:02:12', 1, 2, 2);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
