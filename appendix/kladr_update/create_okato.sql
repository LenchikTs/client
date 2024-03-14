use kladr;

select 'Создание временных таблиц...' as ' ';

CREATE temporary table `tmpOKATO` (
    `P0` CHAR( 2 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `P1` CHAR( 3 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `P2` CHAR( 3 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `P3` CHAR( 3 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `S` CHAR( 1 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `NAME` VARCHAR( 80 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `infis` VARCHAR( 8 ) CHARACTER SET ucs2 COLLATE ucs2_general_ci NOT NULL,
     PRIMARY KEY ( `P0` , `P1` , `P2` )
      ) ENGINE = MYISAM;

-- ALTER TABLE `tmpOKATO` 
-- ADD PRIMARY KEY ( `P0` , `P1` , `P2` );
