-- Adminer 4.8.0 MySQL 8.0.23 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `tankieWatch`;
CREATE DATABASE `tankieWatch` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `tankieWatch`;

DROP TABLE IF EXISTS `authors`;
CREATE TABLE `authors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `author` tinytext NOT NULL,
  `updated` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `author` (`author`(32))
) ENGINE=InnoDB AUTO_INCREMENT=5095 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `authors` (`id`, `author`, `updated`) VALUES
(5080,	'DonkeyKongDownB',	'2021-03-17 10:13:31'),
(5081,	'Firnin',	'2021-03-17 10:13:31'),
(5082,	'FrenchieB011',	'2021-03-17 10:13:31'),
(5083,	'GuyfromWisconsin',	'2021-03-17 10:13:31'),
(5084,	'LifeIsNotMyFavourite',	'2021-03-17 10:13:31'),
(5085,	'PTPESQ',	'2021-03-17 10:13:31'),
(5086,	'Relevant-stuff',	'2021-03-17 10:13:31'),
(5087,	'Sir_Llama_III',	'2021-03-17 10:13:31'),
(5088,	'Svegasvaka',	'2021-03-17 10:13:31'),
(5089,	'Warriorsofthenight02',	'2021-03-17 10:13:31'),
(5090,	'absurditT',	'2021-03-17 10:13:31'),
(5091,	'artem43858',	'2021-03-17 10:13:31'),
(5092,	'cjackc',	'2021-03-17 10:13:31'),
(5093,	'condoriano27',	'2021-03-17 10:13:31'),
(5094,	'tommycahil1995',	'2021-03-17 10:13:31');

DROP TABLE IF EXISTS `subreddits`;
CREATE TABLE `subreddits` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` tinytext NOT NULL,
  `weight` int NOT NULL DEFAULT '1',
  `updated` timestamp NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `subreddits` (`id`, `name`, `weight`, `updated`) VALUES
(2,	'accidentallycommunist\n',	1,	'2021-03-17 11:23:46'),
(3,	'againsthatesubreddits\n',	1,	'2021-03-17 11:23:46'),
(4,	'anarchafeminism\n',	1,	'2021-03-17 11:23:46'),
(5,	'anarchism\n',	1,	'2021-03-17 11:23:46'),
(6,	'anarchocommunism\n',	1,	'2021-03-17 11:23:46'),
(7,	'anarchosyndicalism\n',	1,	'2021-03-17 11:23:46'),
(8,	'anarchy101\n',	1,	'2021-03-17 11:23:46'),
(9,	'ani_communism\n',	1,	'2021-03-17 11:23:46'),
(10,	'antifascistsofreddit\n',	1,	'2021-03-17 11:23:46'),
(11,	'antifastonetoss\n',	1,	'2021-03-17 11:23:46'),
(12,	'antiwork\n',	1,	'2021-03-17 11:23:46'),
(13,	'askaliberal\n',	1,	'2021-03-17 11:23:46'),
(14,	'bannedfromthe_donald\n',	1,	'2021-03-17 11:23:46'),
(15,	'beto2020\n',	1,	'2021-03-17 11:23:46'),
(16,	'bidenbro\n',	1,	'2021-03-17 11:23:46'),
(17,	'bidencoalition\n',	1,	'2021-03-17 11:23:46'),
(18,	'bluemidterm2018\n',	1,	'2021-03-17 11:23:46'),
(19,	'breadtube\n',	1,	'2021-03-17 11:23:46'),
(20,	'breadirl\n',	1,	'2021-03-17 11:23:46'),
(21,	'centerleftpolitics\n',	1,	'2021-03-17 11:23:46'),
(22,	'chapotraphouse2\n',	1,	'2021-03-17 11:23:46'),
(23,	'chapotraphouse\n',	1,	'2021-03-17 11:23:46'),
(24,	'chomsky\n',	1,	'2021-03-17 11:23:46'),
(25,	'circlebroke2\n',	1,	'2021-03-17 11:23:46'),
(26,	'circlebroke\n',	1,	'2021-03-17 11:23:46'),
(27,	'communism101\n',	1,	'2021-03-17 11:23:46'),
(28,	'communism\n',	1,	'2021-03-17 11:23:46'),
(29,	'completeanarchy\n',	1,	'2021-03-17 11:23:46'),
(30,	'dankleft\n',	1,	'2021-03-17 11:23:46'),
(31,	'debateacommunist\n',	1,	'2021-03-17 11:23:46'),
(32,	'debateanarchism\n',	1,	'2021-03-17 11:23:46'),
(33,	'debatecommunism\n',	1,	'2021-03-17 11:23:46'),
(34,	'democrat\n',	1,	'2021-03-17 11:23:46'),
(35,	'democraticsocialism\n',	1,	'2021-03-17 11:23:46'),
(36,	'demsocialists\n',	1,	'2021-03-17 11:23:46'),
(37,	'drumpfisfinished\n',	1,	'2021-03-17 11:23:46'),
(38,	'elizabethwarren\n',	1,	'2021-03-17 11:23:46'),
(39,	'enlightenedcentrism\n',	1,	'2021-03-17 11:23:46'),
(40,	'enoughlibertarianspam\n',	1,	'2021-03-17 11:23:46'),
(41,	'enoughtrumpspam\n',	1,	'2021-03-17 11:23:46'),
(42,	'esist\n',	1,	'2021-03-17 11:23:46'),
(43,	'fragilewhiteredditor\n',	1,	'2021-03-17 11:23:46'),
(44,	'fuckthealtright\n',	1,	'2021-03-17 11:23:46'),
(45,	'fullcommunism\n',	1,	'2021-03-17 11:23:46'),
(46,	'genzedong\n',	1,	'2021-03-17 11:23:46'),
(47,	'greenandpleasant\n',	1,	'2021-03-17 11:23:46'),
(48,	'greenparty\n',	1,	'2021-03-17 11:23:46'),
(49,	'impeach_trump\n',	1,	'2021-03-17 11:23:46'),
(50,	'ironfrontusa\n',	1,	'2021-03-17 11:23:46'),
(51,	'iww\n',	1,	'2021-03-17 11:23:46'),
(52,	'joebiden\n',	1,	'2021-03-17 11:23:46'),
(53,	'keep_track\n',	1,	'2021-03-17 11:23:46'),
(54,	'latestagecapitalism\n',	1,	'2021-03-17 11:23:46'),
(55,	'leftcommunism\n',	1,	'2021-03-17 11:23:46'),
(56,	'leftwithoutedge\n',	1,	'2021-03-17 11:23:46'),
(57,	'liberal\n',	1,	'2021-03-17 11:23:46'),
(58,	'libertarianleft\n',	1,	'2021-03-17 11:23:46'),
(59,	'libertariansocialism\n',	1,	'2021-03-17 11:23:46'),
(60,	'marchagainsttrump\n',	1,	'2021-03-17 11:23:46'),
(61,	'marxismkkk\n',	1,	'2021-03-17 11:23:46'),
(62,	'marxism_101\n',	1,	'2021-03-17 11:23:46'),
(63,	'moretankiechapo\n',	1,	'2021-03-17 11:23:46'),
(64,	'ndp\n',	1,	'2021-03-17 11:23:46'),
(65,	'neoliberal\n',	1,	'2021-03-17 11:23:46'),
(66,	'okbuddycapitalist\n',	1,	'2021-03-17 11:23:46'),
(67,	'onguardforthee\n',	1,	'2021-03-17 11:23:46'),
(68,	'ourpresident\n',	1,	'2021-03-17 11:23:46'),
(69,	'pete_buttigieg\n',	1,	'2021-03-17 11:23:46'),
(70,	'political_revolution\n',	1,	'2021-03-17 11:23:46'),
(71,	'politicalhumor\n',	1,	'2021-03-17 11:23:47'),
(72,	'politics\n',	1,	'2021-03-17 11:23:47'),
(73,	'pragerurine\n',	1,	'2021-03-17 11:23:47'),
(74,	'presidentialracememes\n',	1,	'2021-03-17 11:23:47'),
(75,	'progressive\n',	1,	'2021-03-17 11:23:47'),
(76,	'russialago\n',	1,	'2021-03-17 11:23:47'),
(77,	'sandersforpresident\n',	1,	'2021-03-17 11:23:47'),
(78,	'selfawarewolves\n',	1,	'2021-03-17 11:23:47'),
(79,	'shitliberalssay\n',	1,	'2021-03-17 11:23:47'),
(80,	'shitthe_donaldSays\n',	1,	'2021-03-17 11:23:47'),
(81,	'socialdemocracy\n',	1,	'2021-03-17 11:23:47'),
(82,	'socialjusticeinaction\n',	1,	'2021-03-17 11:23:47'),
(83,	'socialjustice101\n',	1,	'2021-03-17 11:23:47'),
(84,	'socialism\n',	1,	'2021-03-17 11:23:47'),
(85,	'socialism_101\n',	1,	'2021-03-17 11:23:47'),
(86,	'socialistra\n',	1,	'2021-03-17 11:23:47'),
(87,	'stupidpol\n',	1,	'2021-03-17 11:23:47'),
(88,	'the_mueller\n',	1,	'2021-03-17 11:23:47'),
(89,	'therightcantmeme\n',	1,	'2021-03-17 11:23:47'),
(90,	'threearrows\n',	1,	'2021-03-17 11:23:47'),
(91,	'toiletpaperusa\n',	1,	'2021-03-17 11:23:47'),
(92,	'topmindsofreddit\n',	1,	'2021-03-17 11:23:47'),
(93,	'tulsi\n',	1,	'2021-03-17 11:23:47'),
(94,	'vaushv\n',	1,	'2021-03-17 11:23:47'),
(95,	'voteblue\n',	1,	'2021-03-17 11:23:47'),
(96,	'wayofthebern\n',	1,	'2021-03-17 11:23:47'),
(97,	'yangforpresidenthq',	1,	'2021-03-17 11:23:47'),
(98,	'GenZhou',	2,	'2021-03-17 11:24:55'),
(99,	'informedtankie',	2,	'2021-03-17 11:25:23'),
(100,	'asktankies',	2,	'2021-03-17 11:26:05');

-- 2021-03-17 11:35:09
