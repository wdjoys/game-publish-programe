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

 Date: 11/01/2023 15:53:05
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tags
-- ----------------------------
DROP TABLE IF EXISTS `tags`;
CREATE TABLE `tags`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `reg_exp` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Compact;

-- ----------------------------
-- Records of tags
-- ----------------------------
INSERT INTO `tags` VALUES (1, '复古', '复古');
INSERT INTO `tags` VALUES (2, '单职业', '单职');
INSERT INTO `tags` VALUES (3, '三职业', '三职');
INSERT INTO `tags` VALUES (4, '打金', '打金');
INSERT INTO `tags` VALUES (5, '暗黑', '暗黑');
INSERT INTO `tags` VALUES (6, '1.76', '76');
INSERT INTO `tags` VALUES (7, '1.80', '80');
INSERT INTO `tags` VALUES (8, '迷失', '迷失');
INSERT INTO `tags` VALUES (9, '合击', '合击');

SET FOREIGN_KEY_CHECKS = 1;
