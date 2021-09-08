/*
Navicat MySQL Data Transfer

Source Server         : 华为云2
Source Server Version : 80026
Source Host           : 139.9.154.77:3306
Source Database       : school

Target Server Type    : MYSQL
Target Server Version : 80026
File Encoding         : 65001

Date: 2021-09-07 23:45:13
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for grade
-- ----------------------------
DROP TABLE IF EXISTS `grade`;
CREATE TABLE `grade` (
  `GradeID` int NOT NULL AUTO_INCREMENT COMMENT '年级编号',
  `GradeName` varchar(50) NOT NULL COMMENT '年级名称',
  PRIMARY KEY (`GradeID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;

-- ----------------------------
-- Records of grade
-- ----------------------------
INSERT INTO `grade` VALUES ('1', '大一');
INSERT INTO `grade` VALUES ('2', '大二');
INSERT INTO `grade` VALUES ('3', '大三');
INSERT INTO `grade` VALUES ('4', '大四');
INSERT INTO `grade` VALUES ('5', '预科班');
