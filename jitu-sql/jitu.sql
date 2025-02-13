/*
 Navicat Premium Data Transfer

 Source Server         : Localhost
 Source Server Type    : MySQL
 Source Server Version : 50726
 Source Host           : localhost:3306
 Source Schema         : jitu

 Target Server Type    : MySQL
 Target Server Version : 50726
 File Encoding         : 65001

 Date: 13/02/2025 15:55:54
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for pic_folder_list
-- ----------------------------
DROP TABLE IF EXISTS `pic_folder_list`;
CREATE TABLE `pic_folder_list`  (
  `pid` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '文件夹 id',
  `pic_folder_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_german2_ci NULL DEFAULT NULL COMMENT '文件夹名称',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`pid`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_german2_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pic_folder_list
-- ----------------------------
INSERT INTO `pic_folder_list` VALUES (1, '默认相册', '2025-02-13 00:00:00');

-- ----------------------------
-- Table structure for pic_list
-- ----------------------------
DROP TABLE IF EXISTS `pic_list`;
CREATE TABLE `pic_list`  (
  `pid` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '图片 ID',
  `uuid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_german2_ci NULL DEFAULT NULL COMMENT '图片 UUID',
  `pic_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_german2_ci NULL DEFAULT NULL COMMENT '图片保存位置',
  `pic_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_german2_ci NULL DEFAULT NULL COMMENT '图片名称',
  `pic_original_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_german2_ci NULL DEFAULT NULL COMMENT '图片原始名称',
  `pic_file_size` bigint(20) NULL DEFAULT NULL COMMENT '图片文件大小',
  `pic_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_german2_ci NULL DEFAULT NULL COMMENT '图片类型',
  `pic_size` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_german2_ci NULL DEFAULT NULL COMMENT '图片尺寸大小',
  `pic_suffix` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_german2_ci NULL DEFAULT NULL COMMENT '图片后缀名',
  `upload_time` datetime(0) NULL DEFAULT NULL COMMENT '图片上传时间',
  PRIMARY KEY (`pid`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8mb4 COLLATE = utf8mb4_german2_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pic_list
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
