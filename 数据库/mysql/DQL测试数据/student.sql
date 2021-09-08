/*
Navicat MySQL Data Transfer

Source Server         : 华为云2
Source Server Version : 80026
Source Host           : 139.9.154.77:3306
Source Database       : school

Target Server Type    : MYSQL
Target Server Version : 80026
File Encoding         : 65001

Date: 2021-09-05 23:09:15
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `StudentNo` int NOT NULL COMMENT '学号',
  `LoginPwd` varchar(20) DEFAULT NULL,
  `StudentName` varchar(20) DEFAULT NULL COMMENT '学生姓名',
  `Sex` tinyint(1) DEFAULT NULL COMMENT '性别，0或1',
  `GradeId` int DEFAULT NULL COMMENT '年级编号',
  `Phone` varchar(50) NOT NULL COMMENT '联系电话，允许为空',
  `Address` varchar(255) NOT NULL COMMENT '地址，允许为空',
  `BornDate` datetime DEFAULT NULL COMMENT '出生时间',
  `Email` varchar(50) NOT NULL COMMENT '邮箱账号允许为空',
  `IdentityCard` varchar(18) DEFAULT NULL COMMENT '身份证号',
  PRIMARY KEY (`StudentNo`),
  UNIQUE KEY `IdentityCard` (`IdentityCard`),
  KEY `Email` (`Email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES ('1000', '111111', '周丹', '1', '1', '13500000001', '北京海淀区中关村大街1号', '1980-01-01 00:00:00', 'text123@qq.com', '123456198001011234');
INSERT INTO `student` VALUES ('1001', '123456', '赵强', '1', '4', '13800002222', '广东深圳', '1990-01-01 00:00:00', 'text111@qq.com', '123456199001011233');
INSERT INTO `student` VALUES ('1002', '111111', '张三', '1', '1', '18996699512', '重庆万州', '2000-06-03 16:22:03', 'text1123@qq.com', '145567675445436546');
INSERT INTO `student` VALUES ('1003', '3245345', '刘涛', '2', '2', '56446546546', '广东珠海', '2021-09-03 21:46:26', 'tesrfdd@qq.com', '845646765465464654');
INSERT INTO `student` VALUES ('1004', '5446464', '刘氓', '1', '3', '18335456753', '新疆哈密', '2021-09-03 21:47:33', 'test@qq.com', '544654646545646544');
INSERT INTO `student` VALUES ('1005', '5465465', '刘张李', '2', '4', '18546546464', '甘肃兰州', '2021-09-03 21:51:53', 'test@qq.com', '854546432131355122');
INSERT INTO `student` VALUES ('1006', '5446464', '白刘鬼', '2', '4', '19213212311', '宁夏银川', '2021-09-03 21:54:22', 'ydfd@qq.com', '456462132132154564');
INSERT INTO `student` VALUES ('1007', '1231321', '大所诉', '1', '2', '51321231211', '广西南宁', '2021-09-04 22:50:11', 'dfd@qq.com', '411212212121212121');
INSERT INTO `student` VALUES ('1008', '5135213', '放地方', '1', '3', '15131231321', '四川成都', '2021-09-04 22:51:17', 'df1d@qq.com', '454654564564545445');
INSERT INTO `student` VALUES ('1009', '5445454', '地方发', '2', '2', '65454545445', '湖南长沙', '2021-09-04 22:51:34', 'df222@qq.com', '654654564156161541');
INSERT INTO `student` VALUES ('1010', '5415445', '岁的法国', '2', '3', '51456445456', '贵州贵阳', '2021-09-04 22:52:34', 'd22fd@qq.com', '564654654654645644');
INSERT INTO `student` VALUES ('1011', '5435453', '们就不能', null, '3', '54564654645', '湖北武汉', '2021-09-05 22:27:34', 'fdsf@qq.com', '654123132132156411');
