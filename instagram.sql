-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 14, 2024 at 05:40 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `instagram`
--

-- --------------------------------------------------------

--
-- Table structure for table `follows`
--

CREATE TABLE `follows` (
  `id` int(11) NOT NULL,
  `follower_id` int(11) NOT NULL,
  `followed_id` int(11) NOT NULL,
  `follow_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `follows`
--

INSERT INTO `follows` (`id`, `follower_id`, `followed_id`, `follow_date`) VALUES
(15, 8, 7, '2024-07-25 12:20:55'),
(16, 8, 9, '2024-07-25 12:22:31'),
(26, 12, 11, '2024-07-29 03:54:06'),
(27, 12, 7, '2024-07-29 03:54:41'),
(29, 11, 12, '2024-07-29 04:02:14'),
(32, 7, 11, '2024-08-01 03:59:01'),
(33, 7, 9, '2024-08-21 12:43:58'),
(36, 7, 12, '2024-08-27 13:52:40'),
(37, 7, 8, '2024-08-27 14:42:00');

-- --------------------------------------------------------

--
-- Table structure for table `likes`
--

CREATE TABLE `likes` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `like_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `likes`
--

INSERT INTO `likes` (`id`, `user_id`, `post_id`, `like_date`) VALUES
(10, 7, 10, '2024-08-24 19:13:00'),
(11, 7, 8, '2024-08-24 19:25:29'),
(14, 7, 3, '2024-08-24 19:27:31'),
(16, 7, 4, '2024-08-25 06:19:07'),
(19, 7, 7, '2024-08-27 13:36:04'),
(20, 8, 5, '2024-08-27 14:38:50'),
(22, 8, 3, '2024-08-27 14:38:57'),
(23, 8, 8, '2024-08-27 14:39:13'),
(25, 7, 12, '2024-08-27 14:41:11'),
(26, 7, 5, '2024-09-27 07:07:48'),
(27, 7, 13, '2024-09-27 07:10:42'),
(28, 7, 9, '2024-10-10 12:18:12'),
(30, 8, 10, '2024-10-11 08:18:43'),
(31, 8, 9, '2024-10-11 08:18:46'),
(32, 8, 7, '2024-10-11 08:18:50'),
(33, 8, 4, '2024-10-11 08:31:09'),
(37, 8, 13, '2024-10-13 05:08:22'),
(38, 8, 12, '2024-10-13 06:18:45'),
(39, 13, 13, '2024-10-13 08:45:23'),
(40, 13, 15, '2024-10-13 08:45:56'),
(41, 7, 15, '2024-10-13 08:46:41');

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `receiver_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`id`, `sender_id`, `receiver_id`, `message`, `timestamp`) VALUES
(20, 7, 8, 'hhh', '2024-10-12 14:01:13'),
(21, 7, 8, 'hj', '2024-10-12 14:01:33'),
(22, 8, 7, 'Bol', '2024-10-12 14:07:40'),
(23, 8, 7, 'Su kare', '2024-10-12 14:07:46'),
(24, 8, 7, 'Jaymo', '2024-10-12 14:07:51'),
(25, 8, 7, 'F', '2024-10-12 14:07:53'),
(26, 8, 7, 'F', '2024-10-12 14:07:53'),
(27, 8, 7, 'F', '2024-10-12 14:07:54'),
(28, 8, 7, 'F', '2024-10-12 14:07:54'),
(29, 8, 7, 'F', '2024-10-12 14:07:54'),
(30, 8, 7, 'F', '2024-10-12 14:07:54'),
(31, 8, 7, 'F', '2024-10-12 14:07:54'),
(32, 8, 7, 'F', '2024-10-12 14:07:54'),
(33, 8, 7, 'F', '2024-10-12 14:07:55'),
(34, 8, 7, 'F', '2024-10-12 14:07:55'),
(35, 8, 7, 'Hdhdhdhhd', '2024-10-12 14:07:57'),
(36, 8, 7, 'Hdhdh', '2024-10-12 14:08:01'),
(37, 8, 7, 'Hiii', '2024-10-12 14:08:52'),
(38, 7, 8, 'Hello', '2024-10-13 04:55:38'),
(39, 8, 7, 'jaymo k', '2024-10-13 05:19:24'),
(40, 8, 7, '1:29 p.m.', '2024-10-13 07:59:31'),
(41, 7, 8, 'Ok', '2024-10-13 07:59:40'),
(42, 7, 8, '6.46', '2024-10-13 13:16:20'),
(43, 8, 7, 'bol bhai', '2024-10-13 13:16:52');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `caption` text DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  `picture` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`id`, `user_id`, `caption`, `date`, `picture`) VALUES
(3, 8, 'Volcano in monsoon', '2024-07-23 14:56:52', 'uploads/volcano.avif'),
(4, 8, 'Something Amazing', '2024-07-23 14:57:28', 'uploads/photo-1721297014914-b6c0d6d612db.avif'),
(5, 8, 'White Flowers', '2024-07-23 15:23:03', 'uploads/photo-1530092285049-1c42085fd395.jpeg'),
(7, 7, 'Rohan Chaudhari', '2024-07-23 17:18:26', 'uploads/photo-1721297014914-b6c0d6d612db.avif'),
(8, 7, 'Rohan', '2024-07-23 17:42:28', 'uploads/Snapchat-1531021760.jpg'),
(9, 11, 'Picture of PC', '2024-07-29 03:52:46', 'uploads/17222251083946941221371197264045.jpg'),
(10, 11, 'Picture of laptop ???? \r\n', '2024-07-29 03:56:42', 'uploads/17222252829285255138286923805244.jpg'),
(12, 8, 'Nice evening', '2024-08-27 14:40:25', 'uploads/20240818_183659.jpg'),
(13, 7, 'Rainy weather', '2024-09-27 07:10:37', 'uploads/17274209905771161042440707657730.jpg'),
(15, 13, 'My profile picture', '2024-10-13 08:45:53', 'uploads/craiyon_141442_Black_haired_anime_guy_standing_and_looking_over_his_shoulder_to_the_camera.png');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `picture` varchar(255) DEFAULT 'uploads/def.avif',
  `contact` varchar(255) DEFAULT '1234567890',
  `bio` text DEFAULT 'No bio added'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `name`, `email`, `password`, `picture`, `contact`, `bio`) VALUES
(7, 'mr_rohan_06', 'Chaudhari Rohan', 'rohan@gmail.com', 'Rohu 143', 'uploads/cr-logo-design_705304-143.jpg', '1234567890', 'From navsari\r\n'),
(8, 'mr_jerry_112', 'Jigar Chaudhari', 'jigarindonasia12@gmail.com', 'Jerry 123', 'uploads/craiyon_141011_Do_a_profil_picture_of_an_anime_boy.png', '1234567890', 'Free Fire Lover'),
(9, 'mr_rohan_060', 'Chaudhari Rohan', 'rohu@gmail.com', 'Rohan 143', 'uploads/def.avif', '1234567890', 'No bio added'),
(11, 'Harshal ', 'Harsahl ', 'daduchaudharih0000@gmail.com', 'harshal12345', 'uploads/def.avif', '1234567890', 'No bio added'),
(12, 'tambi_222', 'nitesh nadar', 'niteshnadar677@gmail.com', 'tambi197900.com', 'uploads/def.avif', '1234567890', 'No bio added'),
(13, 'Pratham23', 'Partham', 'pratham76@gmail.com', 'greeva', 'uploads/craiyon_141442_Black_haired_anime_guy_standing_and_looking_over_his_shoulder_to_the_camera.png', '1234567890', 'No bio added'),
(15, 'kenil35', 'Kenil Patel', 'kenil@gmail.com', 'Kenil 143', 'uploads/def.avif', '1234567890', 'No bio added');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `follows`
--
ALTER TABLE `follows`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_follow` (`follower_id`,`followed_id`),
  ADD KEY `followed_id` (`followed_id`);

--
-- Indexes for table `likes`
--
ALTER TABLE `likes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_like` (`user_id`,`post_id`),
  ADD KEY `post_id` (`post_id`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sender_id` (`sender_id`),
  ADD KEY `receiver_id` (`receiver_id`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `follows`
--
ALTER TABLE `follows`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `likes`
--
ALTER TABLE `likes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `follows`
--
ALTER TABLE `follows`
  ADD CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`followed_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `likes`
--
ALTER TABLE `likes`
  ADD CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`);

--
-- Constraints for table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
