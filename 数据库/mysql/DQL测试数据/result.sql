/*
Navicat MySQL Data Transfer

Source Server         : 华为云2
Source Server Version : 80026
Source Host           : 139.9.154.77:3306
Source Database       : school

Target Server Type    : MYSQL
Target Server Version : 80026
File Encoding         : 65001

Date: 2021-09-07 23:45:02
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for result
-- ----------------------------
DROP TABLE IF EXISTS `result`;
CREATE TABLE `result` (
  `StudentNo` int NOT NULL COMMENT '学号',
  `SubjectNo` int NOT NULL COMMENT '课程编号',
  `ExamDate` datetime NOT NULL COMMENT '考试日期',
  `StudentResult` int NOT NULL COMMENT '考试成绩',
  KEY `SubjectNo` (`SubjectNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- ----------------------------
-- Records of result
-- ----------------------------
INSERT INTO `result` VALUES ('1000', '9', '2013-11-11 16:00:00', '85');
INSERT INTO `result` VALUES ('1000', '2', '2013-11-12 16:00:00', '85');
INSERT INTO `result` VALUES ('1000', '3', '2013-11-11 09:00:00', '68');
INSERT INTO `result` VALUES ('1000', '4', '2013-11-13 16:00:00', '98');
INSERT INTO `result` VALUES ('1000', '5', '2013-11-14 16:00:00', '58');
INSERT INTO `result` VALUES ('1001', '1', '2021-09-03 19:26:55', '66');
INSERT INTO `result` VALUES ('1001', '2', '2021-09-03 19:27:15', '99');
INSERT INTO `result` VALUES ('1001', '3', '2021-09-03 19:27:33', '44');
INSERT INTO `result` VALUES ('1001', '4', '2021-09-03 19:27:47', '98');
INSERT INTO `result` VALUES ('1001', '5', '2021-09-03 19:28:01', '78');
INSERT INTO `result` VALUES ('1001', '6', '2021-09-03 19:28:16', '89');
INSERT INTO `result` VALUES ('1002', '1', '2021-09-03 19:28:27', '44');
INSERT INTO `result` VALUES ('1002', '2', '2021-09-03 19:28:37', '11');
INSERT INTO `result` VALUES ('1002', '3', '2021-09-03 19:28:51', '11');
INSERT INTO `result` VALUES ('1002', '9', '2021-09-03 19:29:01', '11');
INSERT INTO `result` VALUES ('1002', '5', '2021-09-03 19:29:12', '35');
INSERT INTO `result` VALUES ('1002', '13', '2021-09-03 19:29:24', '88');
INSERT INTO `result` VALUES ('1003', '1', '2021-09-03 19:30:01', '48');
INSERT INTO `result` VALUES ('1003', '2', '2021-09-03 19:30:14', '38');
INSERT INTO `result` VALUES ('1003', '3', '2021-09-03 19:30:25', '81');
INSERT INTO `result` VALUES ('1003', '4', '2021-09-03 19:30:35', '67');
INSERT INTO `result` VALUES ('1003', '5', '2021-09-03 19:30:45', '82');
INSERT INTO `result` VALUES ('1003', '6', '2021-09-03 19:30:59', '68');
INSERT INTO `result` VALUES ('1004', '1', '2021-09-14 19:31:12', '78');
INSERT INTO `result` VALUES ('1004', '2', '2021-09-08 19:31:27', '77');
INSERT INTO `result` VALUES ('1004', '3', '2021-09-03 19:31:36', '57');
INSERT INTO `result` VALUES ('1004', '4', '2021-09-03 19:31:43', '87');
INSERT INTO `result` VALUES ('1004', '5', '2021-09-03 19:31:50', '87');
INSERT INTO `result` VALUES ('1004', '6', '2021-09-03 19:32:00', '87');
INSERT INTO `result` VALUES ('1005', '1', '2021-09-04 22:53:22', '79');
INSERT INTO `result` VALUES ('1006', '1', '2021-09-04 22:54:21', '81');
INSERT INTO `result` VALUES ('1007', '1', '2021-09-04 22:54:30', '82');
INSERT INTO `result` VALUES ('1008', '1', '2021-09-04 22:54:38', '35');
INSERT INTO `result` VALUES ('1009', '1', '2021-09-04 22:54:47', '100');
INSERT INTO `result` VALUES ('1010', '1', '2021-09-04 22:54:57', '55');
