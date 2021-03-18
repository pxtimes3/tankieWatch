-- Adminer 4.8.0 MySQL 8.0.23 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `activity`;
CREATE TABLE `activity` (
  `id` int NOT NULL AUTO_INCREMENT,
  `author_id` int NOT NULL,
  `activity` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'json',
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `author_id` (`author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `authors`;
CREATE TABLE `authors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `author` tinytext NOT NULL,
  `updated` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `author` (`author`(32))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `subreddits`;
CREATE TABLE `subreddits` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` tinytext NOT NULL,
  `weight` float NOT NULL DEFAULT '1',
  `updated` timestamp NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`(32))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- 2021-03-18 19:09:39
