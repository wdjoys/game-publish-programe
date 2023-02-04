/*
 Navicat Premium Data Transfer

 Source Server         : locakhost
 Source Server Type    : MariaDB
 Source Server Version : 100128
 Source Host           : localhost:3306
 Source Schema         : game-publish

 Target Server Type    : MariaDB
 Target Server Version : 100128
 File Encoding         : 65001

 Date: 04/02/2023 14:03:48
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for publish_source
-- ----------------------------
DROP TABLE IF EXISTS `publish_source`;
CREATE TABLE `publish_source`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `url` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `record_reg_exp` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `located_time` tinyint(4) NOT NULL,
  `located_url` tinyint(4) NOT NULL,
  `located_ip` tinyint(4) NOT NULL,
  `located_name` tinyint(4) NOT NULL,
  `located_route` tinyint(4) NOT NULL,
  `located_description` tinyint(4) NOT NULL,
  `located_service` tinyint(4) NOT NULL,
  `time_reg_exp` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `located_time_h` tinyint(4) NOT NULL,
  `located_time_month` tinyint(4) NOT NULL,
  `located_time_min` tinyint(4) NOT NULL,
  `located_time_d` tinyint(4) NOT NULL,
  `last_run_time` datetime NOT NULL,
  `active` tinyint(1) NOT NULL,
  `charset` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for server_tag
-- ----------------------------
DROP TABLE IF EXISTS `server_tag`;
CREATE TABLE `server_tag`  (
  `server_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  INDEX `2`(`server_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for servers_ad
-- ----------------------------
DROP TABLE IF EXISTS `servers_ad`;
CREATE TABLE `servers_ad`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NULL DEFAULT NULL,
  `url` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '地址',
  `ip` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT 'ip',
  `name` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '服务器名称',
  `route` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '线路',
  `description` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '介绍',
  `service` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '客服',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `timestamp`(`timestamp`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 36207 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for servers_ad_count
-- ----------------------------
DROP TABLE IF EXISTS `servers_ad_count`;
CREATE TABLE `servers_ad_count`  (
  `source` int(11) NULL DEFAULT NULL,
  `game` int(11) NULL DEFAULT NULL,
  `count` int(11) NULL DEFAULT NULL,
  INDEX `1`(`game`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for tags
-- ----------------------------
DROP TABLE IF EXISTS `tags`;
CREATE TABLE `tags`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `reg_exp` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
