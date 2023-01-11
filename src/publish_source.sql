/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 100137
 Source Host           : 127.0.0.1:3306
 Source Schema         : game-publish

 Target Server Type    : MySQL
 Target Server Version : 100137
 File Encoding         : 65001

 Date: 11/01/2023 16:38:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for publish_source
-- ----------------------------
DROP TABLE IF EXISTS `publish_source`;
CREATE TABLE `publish_source`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `url` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `record_reg_exp` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `located_time` tinyint NOT NULL,
  `located_url` tinyint NOT NULL,
  `located_ip` tinyint NOT NULL,
  `located_name` tinyint NOT NULL,
  `located_route` tinyint NOT NULL,
  `located_description` tinyint NOT NULL,
  `located_service` tinyint NOT NULL,
  `time_reg_exp` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `located_time_h` tinyint NOT NULL,
  `located_time_month` tinyint NOT NULL,
  `located_time_min` tinyint NOT NULL,
  `located_time_d` tinyint NOT NULL,
  `last_run_time` datetime NOT NULL,
  `active` tinyint(1) NOT NULL,
  `charset` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = COMPACT;

-- ----------------------------
-- Records of publish_source
-- ----------------------------
INSERT INTO `publish_source` VALUES (2, 'http://99s.com', 'o\\d\\(\"(.+?)\",\"(.+?)\",\"(.+?)\",\"(.+?)\",\"(.+?)\",\"(.+?)\",\"(.+?)\"', 3, 1, 2, 0, 4, 5, 6, '(\\d)+月(\\d+)日.(?:(\\d+)点)?(?:(\\d+)分)?', 2, 0, 3, 1, '2023-01-11 16:23:34', 1, 'gb2312');

SET FOREIGN_KEY_CHECKS = 1;
