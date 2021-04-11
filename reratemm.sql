-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 11, 2021 at 08:57 AM
-- Server version: 8.0.21
-- PHP Version: 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `reratemm`
--

-- --------------------------------------------------------

--
-- Table structure for table `act`
--

DROP TABLE IF EXISTS `act`;
CREATE TABLE IF NOT EXISTS `act` (
  `movie_id` int NOT NULL,
  `actor_id` int NOT NULL,
  PRIMARY KEY (`movie_id`,`actor_id`) USING BTREE,
  KEY `actor_id` (`actor_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `act`
--

INSERT INTO `act` (`movie_id`, `actor_id`) VALUES
(5, 1),
(4, 2),
(2, 4),
(1, 5),
(3, 8);

-- --------------------------------------------------------

--
-- Table structure for table `actor`
--

DROP TABLE IF EXISTS `actor`;
CREATE TABLE IF NOT EXISTS `actor` (
  `id` int NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `country` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `date_of_birth` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `actor`
--

INSERT INTO `actor` (`id`, `name`, `country`, `date_of_birth`) VALUES
(1, 'Jackie Chan', 'Hong Kong', '19540407'),
(2, 'Robert Downey Jr.', 'United States of America', '19650404'),
(4, 'Takeru Satoh', 'Japan', '19890321'),
(5, 'Hyun Bin', 'Korea', '19820925'),
(8, 'Fan Bingbing', 'China', '19810916');

-- --------------------------------------------------------

--
-- Table structure for table `album`
--

DROP TABLE IF EXISTS `album`;
CREATE TABLE IF NOT EXISTS `album` (
  `id` int NOT NULL,
  `cover` binary(1) DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `album_or_ep` int DEFAULT NULL,
  `releaseDate` datetime DEFAULT NULL,
  `detailedInfo` text CHARACTER SET utf8 COLLATE utf8_bin,
  `g_id` int DEFAULT NULL,
  `track_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `c_id` int DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `g_id` (`g_id`) USING BTREE,
  KEY `track_name` (`track_name`) USING BTREE,
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `album`
--

INSERT INTO `album` (`id`, `cover`, `name`, `album_or_ep`, `releaseDate`, `detailedInfo`, `g_id`, `track_name`, `c_id`) VALUES
(1, NULL, 'album_1', 1, '2020-01-01 00:00:00', 'test1', 1, 'track_2', 1),
(2, NULL, 'album_2', 1, '2020-01-02 00:00:00', 'test2', 3, 'track_3', 4),
(3, NULL, 'album_3', 1, '2020-01-03 00:00:00', 'test3', 2, 'track_4', 2),
(4, NULL, 'album_4', 0, '2020-01-04 00:00:00', 'test4', 2, 'track_1', 5),
(5, NULL, 'album_5', 1, '2020-01-05 00:00:00', 'test5', 5, 'track_5', 3);

-- --------------------------------------------------------

--
-- Table structure for table `albumartists`
--

DROP TABLE IF EXISTS `albumartists`;
CREATE TABLE IF NOT EXISTS `albumartists` (
  `id` int NOT NULL,
  `artist` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`,`artist`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Table structure for table `albumcomment`
--

DROP TABLE IF EXISTS `albumcomment`;
CREATE TABLE IF NOT EXISTS `albumcomment` (
  `comment_id` int NOT NULL DEFAULT '0',
  `content` text CHARACTER SET utf8 COLLATE utf8_bin,
  `createtime` datetime DEFAULT NULL,
  PRIMARY KEY (`comment_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `albumcomment`
--

INSERT INTO `albumcomment` (`comment_id`, `content`, `createtime`) VALUES
(1, '{content1:\"content1\",content2:\"conten2\"}', '2019-01-01 00:00:00'),
(2, '{content1:\"content1\",content2:\"conten2\"}', '2019-01-02 00:00:00'),
(3, '{content1:\"content1\",content2:\"conten2\"}', '2019-01-03 00:00:00'),
(4, '{content1:\"content1\",content2:\"conten2\"}', '2019-01-04 00:00:00'),
(5, '{content1:\"content1\",content2:\"conten2\"}', '2019-01-05 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `albumrating`
--

DROP TABLE IF EXISTS `albumrating`;
CREATE TABLE IF NOT EXISTS `albumrating` (
  `rate_id` int NOT NULL,
  `createtime` datetime DEFAULT NULL,
  `value` double DEFAULT NULL,
  PRIMARY KEY (`rate_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `albumrating`
--

INSERT INTO `albumrating` (`rate_id`, `createtime`, `value`) VALUES
(1, '2020-03-01 00:00:00', 1),
(2, '2020-03-02 00:00:00', 2),
(3, '2020-03-03 00:00:00', 5.5),
(4, '2020-03-04 00:00:00', 6.6),
(5, '2020-03-05 00:00:00', 9.8);

-- --------------------------------------------------------

--
-- Table structure for table `artist`
--

DROP TABLE IF EXISTS `artist`;
CREATE TABLE IF NOT EXISTS `artist` (
  `id` int NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `portrait` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `detailedinfo` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `company` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `country` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `g_id` int DEFAULT NULL,
  `track_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `album_id` int DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `g_id` (`g_id`) USING BTREE,
  KEY `track_name` (`track_name`) USING BTREE,
  KEY `album_id` (`album_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `artist`
--

INSERT INTO `artist` (`id`, `name`, `portrait`, `detailedinfo`, `company`, `country`, `g_id`, `track_name`, `album_id`) VALUES
(0, 'a', '', '', '', '', 2, 'track_1', 1),
(2, 'b', 'None', 'None', 'MicroSoft', 'Canada', 1, 'track_2', 1),
(3, 'c', 'None', 'None', 'MicroSoft', 'Canada', 2, 'track_1', 5),
(4, 'd', 'None', 'None', 'SFU', 'Canada', 1, 'track_4', 4),
(5, 'e', 'None', 'None', 'SFU', 'Canada', 1, 'track_5', 3);

-- --------------------------------------------------------

--
-- Table structure for table `direct`
--

DROP TABLE IF EXISTS `direct`;
CREATE TABLE IF NOT EXISTS `direct` (
  `movie_id` int NOT NULL,
  `director_id` int NOT NULL,
  PRIMARY KEY (`movie_id`,`director_id`) USING BTREE,
  KEY `director_id` (`director_id`) USING BTREE,
  KEY `movie_id` (`movie_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `direct`
--

INSERT INTO `direct` (`movie_id`, `director_id`) VALUES
(5, 1),
(4, 2),
(3, 3),
(2, 4),
(1, 5);

-- --------------------------------------------------------

--
-- Table structure for table `director`
--

DROP TABLE IF EXISTS `director`;
CREATE TABLE IF NOT EXISTS `director` (
  `id` int NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `country` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `date_of_birth` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `director`
--

INSERT INTO `director` (`id`, `name`, `country`, `date_of_birth`) VALUES
(1, 'director_1', 'country_1', '20200201'),
(2, 'director_2', 'country_2', '20200202'),
(3, 'director_3', 'country_3', '20200301'),
(4, 'director_4', 'country_4', '20200203'),
(5, 'director_5', 'country_5', '20200204');

-- --------------------------------------------------------

--
-- Table structure for table `genre`
--

DROP TABLE IF EXISTS `genre`;
CREATE TABLE IF NOT EXISTS `genre` (
  `id` int NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `album_track_artist_movie` int DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `genre`
--

INSERT INTO `genre` (`id`, `name`, `album_track_artist_movie`) VALUES
(1, 'genre_1', 1),
(2, 'genre_2', 2),
(3, 'genre_3', 3),
(4, 'genre_4', 4),
(5, 'genre_5', 1);

-- --------------------------------------------------------

--
-- Table structure for table `movie`
--

DROP TABLE IF EXISTS `movie`;
CREATE TABLE IF NOT EXISTS `movie` (
  `id` int NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `release_date` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `country` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `detailed_information` text CHARACTER SET utf8 COLLATE utf8_bin,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `movie`
--

INSERT INTO `movie` (`id`, `title`, `release_date`, `country`, `detailed_information`) VALUES
(1, 'movie_1', '20180505', 'China', 'detalied_movie_1'),
(2, 'movie_2', '20180502', 'China', 'detalied_movie_2'),
(3, 'movie_3', '20180503', 'China', 'detalied_movie_3'),
(4, 'movie_4', '20180504', 'China', 'detalied_movie_4'),
(5, 'movie_5', '20180505', 'China', 'detalied_movie_5');

-- --------------------------------------------------------

--
-- Table structure for table `moviecomment`
--

DROP TABLE IF EXISTS `moviecomment`;
CREATE TABLE IF NOT EXISTS `moviecomment` (
  `comment_id` int NOT NULL,
  `movie_id` int NOT NULL,
  `createtime` datetime DEFAULT NULL,
  `content` text CHARACTER SET utf8 COLLATE utf8_bin,
  PRIMARY KEY (`comment_id`,`movie_id`) USING BTREE,
  KEY `movie_id` (`movie_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `moviecomment`
--

INSERT INTO `moviecomment` (`comment_id`, `movie_id`, `createtime`, `content`) VALUES
(1, 1, '2020-01-01 00:00:00', 'comment_1'),
(2, 1, '2020-02-01 00:00:00', 'comment_2'),
(3, 2, '2020-03-01 00:00:00', 'comment_3'),
(4, 2, '2020-04-01 00:00:00', 'comment_4'),
(5, 4, '2020-05-01 00:00:00', 'comment_5');

-- --------------------------------------------------------

--
-- Table structure for table `movierating`
--

DROP TABLE IF EXISTS `movierating`;
CREATE TABLE IF NOT EXISTS `movierating` (
  `rate_id` int NOT NULL,
  `createtime` datetime DEFAULT NULL,
  `value` double DEFAULT NULL,
  PRIMARY KEY (`rate_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `movierating`
--

INSERT INTO `movierating` (`rate_id`, `createtime`, `value`) VALUES
(1, '2020-02-01 00:00:00', 1.5),
(2, '2020-02-01 00:00:00', 2.5),
(3, '2020-03-01 00:00:00', 3.5),
(4, '2020-04-01 00:00:00', 4.5),
(5, '2020-05-01 00:00:00', 5.5);

-- --------------------------------------------------------

--
-- Table structure for table `producealbum`
--

DROP TABLE IF EXISTS `producealbum`;
CREATE TABLE IF NOT EXISTS `producealbum` (
  `albumID` int NOT NULL DEFAULT '0',
  `artistID` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`albumID`,`artistID`) USING BTREE,
  KEY `artistID` (`artistID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `producealbum`
--

INSERT INTO `producealbum` (`albumID`, `artistID`) VALUES
(1, 0),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

-- --------------------------------------------------------

--
-- Table structure for table `producetrack`
--

DROP TABLE IF EXISTS `producetrack`;
CREATE TABLE IF NOT EXISTS `producetrack` (
  `name` varchar(225) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '',
  `artistID` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`name`,`artistID`) USING BTREE,
  KEY `artistID` (`artistID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `producetrack`
--

INSERT INTO `producetrack` (`name`, `artistID`) VALUES
('track_1', 0),
('track_3', 2),
('track_4', 3),
('track_5', 4),
('track_2', 5);

-- --------------------------------------------------------

--
-- Table structure for table `track`
--

DROP TABLE IF EXISTS `track`;
CREATE TABLE IF NOT EXISTS `track` (
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `lyrics` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `track`
--

INSERT INTO `track` (`name`, `lyrics`) VALUES
('track_1', 'lyrics_1'),
('track_2', 'lyrics_2'),
('track_3', 'lyrics_3'),
('track_4', 'lyrics_4'),
('track_5', 'lyrics_5');

-- --------------------------------------------------------

--
-- Table structure for table `trackrating`
--

DROP TABLE IF EXISTS `trackrating`;
CREATE TABLE IF NOT EXISTS `trackrating` (
  `rate_id` int NOT NULL,
  `createtime` datetime DEFAULT NULL,
  `value` double DEFAULT NULL,
  PRIMARY KEY (`rate_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `trackrating`
--

INSERT INTO `trackrating` (`rate_id`, `createtime`, `value`) VALUES
(1, '2020-01-01 00:00:00', 10),
(2, '2020-01-01 00:00:00', 9),
(3, '2020-01-01 00:00:00', 8.8),
(4, '2020-01-01 00:00:00', 6),
(5, '2020-01-01 00:00:00', 5);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int NOT NULL,
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `music_rating_weight` double DEFAULT NULL,
  `movie_rating_weight` double DEFAULT NULL,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `album_r_id` int DEFAULT NULL,
  `album_c_id` int DEFAULT NULL,
  `track_r_id` int DEFAULT NULL,
  `movie_c_id` int DEFAULT NULL,
  `movie_r_id` int DEFAULT NULL,
  `certified_musician` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`,`email`) USING BTREE,
  KEY `album_r_id` (`album_r_id`) USING BTREE,
  KEY `album_c_id` (`album_c_id`) USING BTREE,
  KEY `track_r_id` (`track_r_id`) USING BTREE,
  KEY `movie_c_id` (`movie_c_id`) USING BTREE,
  KEY `movie_r_id` (`movie_r_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `email`, `music_rating_weight`, `movie_rating_weight`, `username`, `password`, `album_r_id`, `album_c_id`, `track_r_id`, `movie_c_id`, `movie_r_id`, `certified_musician`) VALUES
(2147483647, '6@sfu.ca', 0, 0, 'test_6', '123456', NULL, NULL, NULL, NULL, NULL, NULL),
(2147483647, '7@sfu.ca', 0, 0, 'test_7', '123456', NULL, NULL, NULL, NULL, NULL, NULL),
(2147483647, 'fghf', 0, 0, 'ghf', 'fgh', NULL, NULL, NULL, NULL, NULL, NULL),
(2147483647, 'lkljk', 0, 0, '45', 'jjlh', NULL, NULL, NULL, NULL, NULL, NULL);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `act`
--
ALTER TABLE `act`
  ADD CONSTRAINT `act_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `act_ibfk_2` FOREIGN KEY (`actor_id`) REFERENCES `actor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `album`
--
ALTER TABLE `album`
  ADD CONSTRAINT `album_ibfk_1` FOREIGN KEY (`g_id`) REFERENCES `genre` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `album_ibfk_2` FOREIGN KEY (`track_name`) REFERENCES `track` (`name`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `album_ibfk_3` FOREIGN KEY (`c_id`) REFERENCES `albumcomment` (`comment_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `artist`
--
ALTER TABLE `artist`
  ADD CONSTRAINT `artist_ibfk_1` FOREIGN KEY (`g_id`) REFERENCES `genre` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `artist_ibfk_2` FOREIGN KEY (`track_name`) REFERENCES `track` (`name`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `artist_ibfk_3` FOREIGN KEY (`album_id`) REFERENCES `album` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `direct`
--
ALTER TABLE `direct`
  ADD CONSTRAINT `direct_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `direct_ibfk_2` FOREIGN KEY (`director_id`) REFERENCES `director` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `moviecomment`
--
ALTER TABLE `moviecomment`
  ADD CONSTRAINT `moviecomment_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `producealbum`
--
ALTER TABLE `producealbum`
  ADD CONSTRAINT `producealbum_ibfk_1` FOREIGN KEY (`albumID`) REFERENCES `album` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `producealbum_ibfk_2` FOREIGN KEY (`artistID`) REFERENCES `artist` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `producetrack`
--
ALTER TABLE `producetrack`
  ADD CONSTRAINT `producetrack_ibfk_1` FOREIGN KEY (`name`) REFERENCES `track` (`name`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `producetrack_ibfk_2` FOREIGN KEY (`artistID`) REFERENCES `artist` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`album_r_id`) REFERENCES `albumrating` (`rate_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `user_ibfk_2` FOREIGN KEY (`album_c_id`) REFERENCES `albumcomment` (`comment_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `user_ibfk_3` FOREIGN KEY (`track_r_id`) REFERENCES `trackrating` (`rate_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `user_ibfk_4` FOREIGN KEY (`movie_c_id`) REFERENCES `moviecomment` (`comment_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `user_ibfk_5` FOREIGN KEY (`movie_r_id`) REFERENCES `albumrating` (`rate_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
