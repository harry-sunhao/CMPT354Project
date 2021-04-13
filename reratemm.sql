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
-- Table structure for table `Act`
--

DROP TABLE IF EXISTS `Act`;
CREATE TABLE IF NOT EXISTS `Act` (
  `movie_id` int NOT NULL,
  `actor_id` int NOT NULL,
  PRIMARY KEY (`movie_id`,`actor_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `Act`
--

INSERT INTO `Act` (`movie_id`, `actor_id`) VALUES
(5, 1),
(4, 2),
(2, 4),
(1, 5),
(2, 5),
(3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `Actor`
--

DROP TABLE IF EXISTS `Actor`;
CREATE TABLE IF NOT EXISTS `Actor` (
  `id` int NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `country` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `date_of_birth` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `Actor`
--

INSERT INTO `Actor` (`id`, `name`, `country`, `date_of_birth`) VALUES
(1, 'Jackie Chan', 'Hong Kong', '19540407'),
(2, 'Robert Downey Jr.', 'United States of America', '19650404'),
(3, 'Takeru Satoh', 'Japan', '19890321'),
(4, 'Hyun Bin', 'Korea', '19820925'),
(5, 'Fan Bingbing', 'China', '19810916');

-- --------------------------------------------------------

--
-- Table structure for table `Album`
--

DROP TABLE IF EXISTS `Album`;
CREATE TABLE IF NOT EXISTS `Album` (
  `id` int NOT NULL,
  `cover` LONGBLOB DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `album_or_ep` int DEFAULT NULL,
  `releaseDate` datetime DEFAULT NULL,
  `detailedInfo` text CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `Album`
--

INSERT INTO `Album` (`id`, `cover`, `name`, `album_or_ep`, `releaseDate`, `detailedInfo`) VALUES
(1, NULL, 'album_1', 1, '2020-01-01 00:00:00', 'info1'),
(2, NULL, 'album_2', 1, '2020-01-02 00:00:00', 'info2'),
(3, NULL, 'album_3', 1, '2020-01-03 00:00:00', 'info3'),
(4, NULL, 'album_4', 0, '2020-01-04 00:00:00', 'info4'),
(5, NULL, 'album_5', 1, '2020-01-05 00:00:00', 'info5');

-- --------------------------------------------------------

--
-- Table structure for table `AlbumArtist`
--

DROP TABLE IF EXISTS `AlbumArtist`;
CREATE TABLE IF NOT EXISTS `AlbumArtist` (
  `album_id` int NOT NULL,
  `artist_id` int NOT NULL,
  PRIMARY KEY (`album_id`,`artist_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `AlbumArtist`
--

INSERT INTO `AlbumArtist` (`album_id`, `artist_id`) VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 1),
(5, 2);

-- --------------------------------------------------------

--
-- Table structure for table `AlbumComment`
--

DROP TABLE IF EXISTS `AlbumComment`;
CREATE TABLE IF NOT EXISTS `AlbumComment` (
  `comment_id` int NOT NULL,
  `content` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `createtime` datetime DEFAULT NULL,
  `album_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`comment_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `AlbumComment`
--

INSERT INTO `AlbumComment` (`comment_id`, `content`, `createtime`, `album_id`, `user_id`) VALUES
(1, '{content1:\"content1\",content2:\"conten2\"}', '2019-01-01 00:00:00', 1, 31703000),
(2, '{content1:\"content1\",content2:\"conten2\"}', '2019-01-02 00:00:00', 1, 31703001),
(3, '{content1:\"content1\",content2:\"conten2\"}', '2019-01-03 00:00:00', 1, 31703003),
(4, '{content1:\"content1\",content2:\"conten2\"}', '2019-01-04 00:00:00', 1, 31703003),
(5, '{content1:\"content1\",content2:\"conten2\"}', '2019-01-05 00:00:00', 1, 31703004);

-- --------------------------------------------------------

--
-- Table structure for table `AlbumRating`
--

DROP TABLE IF EXISTS `AlbumRating`;
CREATE TABLE IF NOT EXISTS `AlbumRating` (
  `rate_id` int NOT NULL,
  `createtime` datetime DEFAULT NULL,
  `value` int DEFAULT NULL,
  `album_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`rate_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `AlbumRating`
--

INSERT INTO `AlbumRating` (`rate_id`, `createtime`, `value`, `album_id`, `user_id`) VALUES
(1, '2020-03-01 00:00:00', 9, 1, 31703000),
(2, '2020-03-02 00:00:00', 10, 1, 31703001),
(3, '2020-03-03 00:00:00', 8, 2, 31703002),
(4, '2020-03-04 00:00:00', 9, 2, 31703003),
(5, '2020-03-05 00:00:00', 8, 3, 31703003);

-- --------------------------------------------------------

--
-- Table structure for table `Artist`
--

DROP TABLE IF EXISTS `Artist`;
CREATE TABLE IF NOT EXISTS `Artist` (
  `id` int NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `portrait` LONGBLOB DEFAULT NULL,
  `detailedinfo` text CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `company` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `country` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `Artist`
--

INSERT INTO `Artist` (`id`, `name`, `portrait`, `detailedinfo`, `company`, `country`) VALUES
(1, 'Pink Floyd', NULL, 'info1', 'Columbia Records', 'British'),
(2, 'b', NULL, 'info2', 'MicroSoft', 'Canada'),
(3, 'c', NULL, 'info3', 'MicroSoft', 'Canada'),
(4, 'd', NULL, 'info4', 'SFU', 'Canada'),
(5, 'e', NULL, 'info5', 'SFU', 'Canada');

-- --------------------------------------------------------

--
-- Table structure for table `Direct`
--

DROP TABLE IF EXISTS `Direct`;
CREATE TABLE IF NOT EXISTS `Direct` (
  `movie_id` int NOT NULL,
  `director_id` int NOT NULL,
  PRIMARY KEY (`movie_id`,`director_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `Direct`
--

INSERT INTO `Direct` (`movie_id`, `director_id`) VALUES
(5, 1),
(4, 2),
(3, 3),
(2, 4),
(1, 5);

-- --------------------------------------------------------

--
-- Table structure for table `Director`
--

DROP TABLE IF EXISTS `Director`;
CREATE TABLE IF NOT EXISTS `Director` (
  `id` int NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `country` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `date_of_birth` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `Director`
--

INSERT INTO `Director` (`id`, `name`, `country`, `date_of_birth`) VALUES
(1, 'director_1', 'country_1', '19700201'),
(2, 'director_2', 'country_2', '19700202'),
(3, 'director_3', 'country_3', '19700301'),
(4, 'director_4', 'country_4', '19700203'),
(5, 'director_5', 'country_5', '19700204');

-- --------------------------------------------------------

--
-- Table structure for table `Genre`
--

DROP TABLE IF EXISTS `Genre`;
CREATE TABLE IF NOT EXISTS `Genre` (
  `id` int NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `album_track_artist_movie` int DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `Genre`
--

INSERT INTO `Genre` (`id`, `name`, `album_track_artist_movie`) VALUES
(1, 'genre_1', 1),
(2, 'genre_2', 2),
(3, 'genre_3', 3),
(4, 'genre_4', 4),
(5, 'genre_5', 1);

-- --------------------------------------------------------

--
-- Table structure for table `Movie`
--

DROP TABLE IF EXISTS `Movie`;
CREATE TABLE IF NOT EXISTS `Movie` (
  `id` int NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `release_date` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `country` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `detailed_information` text CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `director_id` int DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `Movie`
--

INSERT INTO `Movie` (`id`, `title`, `release_date`, `country`, `detailed_information`, `director_id`) VALUES
(1, 'movie_1', '20180505', 'China', 'movie_info_1', 1),
(2, 'movie_2', '20180502', 'China', 'movie_info_2', 1),
(3, 'movie_3', '20180503', 'China', 'movie_info_3', 2),
(4, 'movie_4', '20180504', 'China', 'movie_info_4', 3),
(5, 'movie_5', '20180505', 'China', 'movie_info_5', 4);

-- --------------------------------------------------------

--
-- Table structure for table `MovieComment`
--

DROP TABLE IF EXISTS `MovieComment`;
CREATE TABLE IF NOT EXISTS `MovieComment` (
  `comment_id` int NOT NULL,
  `createtime` datetime DEFAULT NULL,
  `content` text CHARACTER SET utf8 COLLATE utf8_bin,
  `movie_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`comment_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `MovieComment`
--

INSERT INTO `MovieComment` (`comment_id`, `createtime`, `content`, `movie_id`, `user_id`) VALUES
(1, '2020-01-01 00:00:00', 'comment_1', 1, 31703001),
(2, '2020-02-01 00:00:00', 'comment_2', 2, 31703001),
(3, '2020-03-01 00:00:00', 'comment_3', 2, 31703002),
(4, '2020-04-01 00:00:00', 'comment_4', 4, 31703003),
(5, '2020-05-01 00:00:00', 'comment_5', 5, 31703004);

-- --------------------------------------------------------

--
-- Table structure for table `MovieRating`
--

DROP TABLE IF EXISTS `MovieRating`;
CREATE TABLE IF NOT EXISTS `MovieRating` (
  `rate_id` int NOT NULL,
  `createtime` datetime DEFAULT NULL,
  `value` int DEFAULT NULL,
  `movie_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`rate_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `MovieRating`
--

INSERT INTO `MovieRating` (`rate_id`, `createtime`, `value`, `movie_id`, `user_id`) VALUES
(1, '2020-02-01 00:00:00', 7, 1, 31703001),
(2, '2020-02-01 00:00:00', 6, 2, 31703003),
(3, '2020-03-01 00:00:00', 8, 3, 31703003),
(4, '2020-04-01 00:00:00', 5, 4, 31703004),
(5, '2020-05-01 00:00:00', 10, 5, 31703004);

-- --------------------------------------------------------

--
-- Table structure for table `TrackArtist`
--

DROP TABLE IF EXISTS `TrackArtist`;
CREATE TABLE IF NOT EXISTS `TrackArtist` (
  `track_name` varchar(225) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `album_id` int NOT NULL,
  `artist_id` int NOT NULL,
  PRIMARY KEY (`track_name`, `album_id`, `artist_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `TrackArtist`
--

INSERT INTO `TrackArtist` (`track_name`, `album_id`, `artist_id`) VALUES
('track_1', 1, 1),
('track_2', 1, 1),
('track_3', 1, 1),
('track_4', 1, 1),
('track_1', 2, 1),
('track_1', 5, 2);

-- --------------------------------------------------------

--
-- Table structure for table `Track`
--

DROP TABLE IF EXISTS `Track`;
CREATE TABLE IF NOT EXISTS `Track` (
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `album_id` int NOT NULL,
  PRIMARY KEY (`name`, `album_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `Track`
--

INSERT INTO `Track` (`name`, `album_id`) VALUES
('track_1', 1),
('track_2', 1),
('track_3', 1),
('track_4', 1),
('track_1', 2),
('track_1', 5);

-- --------------------------------------------------------

--
-- Table structure for table `TrackRating`
--

DROP TABLE IF EXISTS `TrackRating`;
CREATE TABLE IF NOT EXISTS `TrackRating` (
  `rate_id` int NOT NULL,
  `createtime` datetime DEFAULT NULL,
  `value` int DEFAULT NULL,
  `track_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `album_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`rate_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `TrackRating`
--

INSERT INTO `TrackRating` (`rate_id`, `createtime`, `value`, `track_name`, `album_id`, `user_id`) VALUES
(1, '2020-01-01 00:00:00', 10, 'track_1', 1, 31703001),
(2, '2020-01-01 00:00:00', 9, 'track_1', 1, 31703001),
(3, '2020-01-01 00:00:00', 8, 'track_1', 1, 31703001),
(4, '2020-01-01 00:00:00', 6, 'track_2', 1, 31703001),
(5, '2020-01-01 00:00:00', 5, 'track_2', 1, 31703001);

-- --------------------------------------------------------

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
CREATE TABLE IF NOT EXISTS `User` (
  `id` int NOT NULL,
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `music_rating_weight` double DEFAULT NULL,
  `movie_rating_weight` double DEFAULT NULL,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `certification_information` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE (`email`),
  UNIQUE (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`id`, `email`, `music_rating_weight`, `movie_rating_weight`, `username`, `password`, `certification_information`) VALUES
(31703000, '6@sfu.ca', 7, 10, 'user0', '123456', 'Keyboard of Band Re-tros.'),
(31703001, '7@sfu.ca', 5, 5, 'user1', '123456', NULL),
(31703002, 'fghf', 5, 5, 'user2', 'fgh', NULL),
(31703003, 'lkljk', 5, 5, 'user3', 'jjlh', NULL),
(31703004, 'fghf', 5, 5, 'user4', 'fgh', NULL),
(31703005, 'lkljk', 5, 5, 'user5', 'jjlh', NULL);

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
