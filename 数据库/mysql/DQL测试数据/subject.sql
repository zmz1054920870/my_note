/*
Navicat MySQL Data Transfer

Source Server         : 华为云2
Source Server Version : 80026
Source Host           : 139.9.154.77:3306
Source Database       : school

Target Server Type    : MYSQL
Target Server Version : 80026
File Encoding         : 65001

Date: 2021-09-07 23:44:50
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for subject
-- ----------------------------
DROP TABLE IF EXISTS `subject`;
CREATE TABLE `subject` (
  `SubjectNo` int NOT NULL AUTO_INCREMENT COMMENT '课程编号',
  `SubjectName` varchar(50) DEFAULT NULL COMMENT '课程名称',
  `ClassHour` int DEFAULT NULL COMMENT '学时',
  `GradeID` int DEFAULT NULL COMMENT '年级编号',
  PRIMARY KEY (`SubjectNo`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3;

-- ----------------------------
-- Records of subject
-- ----------------------------
INSERT INTO `subject` VALUES ('1', '高等数学-1', '110', '1');
INSERT INTO `subject` VALUES ('2', '高等数学-2', '110', '2');
INSERT INTO `subject` VALUES ('3', '高等数学-3', '100', '3');
INSERT INTO `subject` VALUES ('4', '高等数学-4', '130', '4');
INSERT INTO `subject` VALUES ('5', 'C语言-1', '110', '1');
INSERT INTO `subject` VALUES ('6', 'C语言-2', '110', '2');
INSERT INTO `subject` VALUES ('7', 'C语言-3', '100', '3');
INSERT INTO `subject` VALUES ('8', 'C语言-4', '130', '4');
INSERT INTO `subject` VALUES ('9', 'Java程序设计-1', '110', '1');
INSERT INTO `subject` VALUES ('10', 'Java程序设计-2', '110', '2');
INSERT INTO `subject` VALUES ('11', 'Java程序设计-3', '100', '3');
INSERT INTO `subject` VALUES ('12', 'Java程序设计-4', '130', '4');
INSERT INTO `subject` VALUES ('13', '数据库结构-1', '110', '1');
INSERT INTO `subject` VALUES ('14', '数据库结构-2', '110', '2');
INSERT INTO `subject` VALUES ('15', '数据库结构-3', '100', '3');
INSERT INTO `subject` VALUES ('16', '数据库结构-4', '130', '4');
INSERT INTO `subject` VALUES ('17', 'C#基础', '130', '1');
