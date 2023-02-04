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

 Date: 04/02/2023 14:03:57
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
-- Records of publish_source
-- ----------------------------
INSERT INTO `publish_source` VALUES (2, '99s', 'http://99s.com', 'o\\d\\(\"(.+?)\",\"(.+?)\",\"(.+?)\",\"(.+?)\",\"(.+?)\",\"(.+?)\",\"(.+?)\"', 3, 1, 2, 0, 4, 5, 6, '(\\d)+月(\\d+)日.(?:(\\d+)点)?(?:(\\d+)分)?', 2, 0, 3, 1, '2023-02-03 23:30:33', 1, 'gb2312');
INSERT INTO `publish_source` VALUES (3, 'zhaosf', 'https://zhaosf.tsbxsw.com', '<td><a target=\"_blank\" href=\"(.+?)\">(.+?)<[\\w\\W]+?\">(.+?)</a[\\w\\W]+?\">(.+?)\\n[\\w\\W]+?<td>(.+?)</td>[\\w\\W]+?>(.+?)<span [\\w\\W]+?td>(.+?)</td>', 3, 0, 2, 1, 4, 5, 6, '(?:今日|(?:(\\d)+月)?(?:(\\d+)日/))(?:(\\d+):)?(\\d+)?', 2, 0, 3, 1, '2023-02-03 23:30:38', 1, 'utf-8');

SET FOREIGN_KEY_CHECKS = 1;
