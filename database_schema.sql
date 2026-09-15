-- Database schema for US Student Email Bot

CREATE DATABASE IF NOT EXISTS `student_email` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `student_email`;

-- User details table
CREATE TABLE IF NOT EXISTS `user_detail_our_email` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `userName` VARCHAR(100) NOT NULL UNIQUE,
  `fullName` VARCHAR(255) NOT NULL,
  `gender` VARCHAR(20),
  `title` VARCHAR(50),
  `race` VARCHAR(50),
  `birthday` VARCHAR(20),
  `ssn` VARCHAR(20),
  `street` VARCHAR(255),
  `city` VARCHAR(100),
  `state` VARCHAR(50),
  `stateFull` VARCHAR(100),
  `zipCode` VARCHAR(20),
  `phoneNumber` VARCHAR(20),
  `mobileNumber` VARCHAR(20),
  `email` VARCHAR(255) NOT NULL UNIQUE,
  `email_pwd` VARCHAR(255),
  `email_server` VARCHAR(255),
  `tag` INT DEFAULT 0,
  `register_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `collect_time` TIMESTAMP,
  INDEX `idx_email` (`email`),
  INDEX `idx_tag` (`tag`),
  INDEX `idx_register_time` (`register_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Email details table
CREATE TABLE IF NOT EXISTS `email_detail` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `stu_id` VARCHAR(50) NOT NULL,
  `edu_email` VARCHAR(255) NOT NULL UNIQUE,
  `edu_pwd` VARCHAR(255) NOT NULL,
  `college_id` INT,
  `collect_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_edu_email` (`edu_email`),
  INDEX `idx_stu_id` (`stu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bot logs table (optional)
CREATE TABLE IF NOT EXISTS `bot_logs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` VARCHAR(100),
  `action` VARCHAR(255),
  `status` VARCHAR(50),
  `message` TEXT,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
