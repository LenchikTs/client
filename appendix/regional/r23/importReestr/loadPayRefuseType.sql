--
-- Импорт причин отказа оплаты счетов для Мурманска
--  данные выбраны из sp15c.dbf в текстовый файл
--

CREATE TEMPORARY TABLE `PRT` (
`code` VARCHAR(3),
`name` VARCHAR(120),
`comment` VARCHAR(254)
) ENGINE = InnoDB DEFAULT CHARSET=utf8 COMMENT = 'Справочник причин отказа оплаты счетов' ;


LOAD DATA LOCAL INFILE 'payRefuseType.txt'
    INTO TABLE `PRT`
    CHARACTER SET cp1251
    FIELDS TERMINATED BY '\t' OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES;

INSERT INTO `rbPayRefuseType` (code, name, finance_id, rerun)
    SELECT	`code`, 
		`name`,
		(SELECT `id` FROM `rbFinance` WHERE `code`='2') AS `finance_id`,
		'1' as `rerun`
    FROM PRT;
