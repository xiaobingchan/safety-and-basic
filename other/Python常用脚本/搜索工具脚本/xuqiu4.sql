CREATE TABLE `s_data`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '表id',
  `company_id` int(11) NOT NULL DEFAULT 0 COMMENT '公司id',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '数据名称',
  `department` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '所属部门',
  `period` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '周期（天、周、月、季等）',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '统计数据' ROW_FORMAT = Dynamic;


CREATE TABLE `s_data_value`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '表id',
  `data_id` int(11) NOT NULL DEFAULT 0 COMMENT 's_data表id',
  `data_time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '时间数据',
  `value` float NOT NULL DEFAULT 0 COMMENT '数值',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '统计数据值' ROW_FORMAT = Dynamic;