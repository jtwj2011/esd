-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `booking`
--
CREATE DATABASE IF NOT EXISTS `tutor` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `tutor`;

-- --------------------------------------------------------

--
-- Table structure for table `booking`

DROP TABLE IF EXISTS `tutor`;
CREATE TABLE IF NOT EXISTS `tutor`(
   `tutor_id` varchar(24) NOT NULL,
   `contact_number` varchar(8) NOT NULL,
  `name` varchar(12) NOT NULL,
  `level` varchar(50) NOT NULL,
  `subject` varchar(50) NOT NULL,
  `subject_rate` varchar(50) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `review` varchar(50) NOT NULL,
  `password_hash` varchar(64) NOT NULL,
  PRIMARY KEY (`tutor_id`, `subject`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `booking`
--


INSERT INTO `tutor` (`tutor_id`, `contact_number`, `name`, `level`, `subject`, `subject_rate`, `gender`, `review`, `password_hash`) VALUES
('abc@gmail.com', '12345678', 'amy', 'primary', 'Math', '30', 'F', 'best tutor ever!', 'asdfgh'),
('def@gmail.com', '11111111', 'ben', 'secondary', 'Chinese', '30', 'M', 'most inspiring tutor ever!', 'qwerty'),
('ghi@gmail.com', '22222222', 'cindy', 'primary', 'English', '20', 'F', 'most interesting tutor ever!', 'qwerty'),
('ghi@gmail.com', '22222222', 'cindy', 'pre-school', 'Science', '25', 'F', 'most interesting tutor ever!', 'qwerty');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
