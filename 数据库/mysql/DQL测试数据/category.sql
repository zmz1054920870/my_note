/*
Navicat MySQL Data Transfer

Source Server         : 华为云2
Source Server Version : 80026
Source Host           : 139.9.154.77:3306
Source Database       : school

Target Server Type    : MYSQL
Target Server Version : 80026
File Encoding         : 65001

Date: 2021-09-07 23:45:29
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `categoryid` int unsigned NOT NULL AUTO_INCREMENT COMMENT '主题ID',
  `pid` int NOT NULL COMMENT '父ID',
  `categoryName` varchar(50) NOT NULL COMMENT '主题名字',
  PRIMARY KEY (`categoryid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;

-- ----------------------------
-- Records of category
-- ----------------------------
INSERT INTO `category` VALUES ('2', '1', '信息技术');
INSERT INTO `category` VALUES ('3', '1', '软件开发');
INSERT INTO `category` VALUES ('4', '3', '数据库');
INSERT INTO `category` VALUES ('5', '1', '美术设计');
INSERT INTO `category` VALUES ('6', '3', 'web开发');
INSERT INTO `category` VALUES ('7', '5', 'PS技术');
INSERT INTO `category` VALUES ('8', '2', '办公信息');
