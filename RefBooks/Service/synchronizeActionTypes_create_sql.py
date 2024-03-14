#!/usr/bin/env python
# -*- coding: utf-8 -*-

COMMAND = u"""

select 'Создание временной таблицы для экспортируемых услуг...' as ' ';

CREATE TEMPORARY TABLE IF NOT EXISTS tmpService2ActionType (
`id` INT( 11 ) NOT NULL AUTO_INCREMENT ,
 `code` VARCHAR( 25 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'Код услуги или группы услуг',
 `name` VARCHAR( 255 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'Название услуги или группы услуг',
 `parentCode` VARCHAR( 23 ) CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT 'Код родительского элемента в иерархии',
 `level` TINYINT( 1 ) NOT NULL COMMENT 'Уровень в иерархии',
 `class` TINYINT( 1 ) NOT NULL COMMENT 'Класс типа действий (0-статус, 1-диагностика, 2-лечение, 3-прочие мероприятия) ',
 `ActionType_id` INT( 11 ) NULL ,
 `ActionType_type` TINYINT( 1 ) NOT NULL ,
 `ActionType_Service_id` INT( 11 ) NULL ,
 `ActionType_Service_type` TINYINT( 1 ) NOT NULL ,
 PRIMARY KEY ( `id` ),
 UNIQUE KEY(`code`)
) ENGINE = INNODB CHARACTER SET utf8;

-- предопределенные уровни иерархии:
INSERT IGNORE INTO tmpService2ActionType (
`id` ,
 `code` ,
 `name` ,
 `parentCode` ,
 `level` ,
 `class` ,
 `ActionType_id` ,
 `ActionType_type`
)
VALUES (
'1', '-', 'Услуги', NULL , '1', '3', NULL , '0'
);

CREATE TEMPORARY TABLE IF NOT EXISTS tmpParents (
`id` INT( 11 ) NOT NULL AUTO_INCREMENT ,
 `code` VARCHAR( 25 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'Код услуги или группы услуг',
 `name` VARCHAR( 255 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'Название услуги или группы услуг',
 `parentCode` VARCHAR( 23 ) CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT 'Код родительского элемента в иерархии',
 `level` TINYINT( 1 ) NOT NULL COMMENT 'Уровень в иерархии',
 `class` TINYINT( 1 ) NOT NULL COMMENT 'Класс типа действий (0-статус, 1-диагностика, 2-лечение, 3-прочие мероприятия) ',
 `ActionType_id` INT( 11 ) NULL ,
 `ActionType_type` TINYINT( 1 ) NOT NULL ,
 `ActionType_Service_id` INT( 11 ) NULL ,
 `ActionType_Service_type` TINYINT( 1 ) NOT NULL ,
 PRIMARY KEY ( `id` ),
 UNIQUE KEY(`code`)
) ENGINE = INNODB CHARACTER SET utf8;"""
