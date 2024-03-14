use kladr;

select 'Создание временных таблиц...' as ' ';

-- сохраняем инфисы:
create temporary table KLADR_infis (
`NAME` VARCHAR( 40 ) NOT NULL ,
`SOCR` VARCHAR( 10 ) NOT NULL ,
`prefix` VARCHAR( 2 ) NOT NULL ,
`STATUS` VARCHAR( 1 ) NOT NULL,
`infis` VARCHAR( 5 ) NOT NULL ,
PRIMARY KEY ( `prefix`, `NAME`, `SOCR`, `STATUS` )) ENGINE = MYISAM DEFAULT CHARSET = utf8;  
insert ignore into KLADR_infis (NAME, SOCR, prefix, STATUS, infis)
select distinct NAME, SOCR, prefix, STATUS, infis from KLADR;

-- сохраняем инфисы:
create temporary table STREET_infis (
`NAME` VARCHAR( 40 ) NOT NULL ,
`SOCR` VARCHAR( 10 ) NOT NULL ,
`infis` VARCHAR( 5 ) NOT NULL ,
PRIMARY KEY ( `NAME`, `SOCR` )) ENGINE = MYISAM DEFAULT CHARSET = utf8;  
insert ignore into STREET_infis (NAME, SOCR, infis)
select distinct NAME, SOCR, infis from STREET
where CODE like '78%'; -- нам нужны инфисы только для питерских улиц

-- сохраняем инфисы:
create temporary table SOCRBASE_infis (
`LEVEL` VARCHAR( 5 ) NOT NULL ,
`SOCRNAME` VARCHAR( 29 ) NOT NULL ,
`infis` VARCHAR( 3 ) NOT NULL)
ENGINE = MYISAM DEFAULT CHARSET = utf8;
insert ignore into SOCRBASE_infis
select distinct `LEVEL`, `SOCRNAME`, `infisCODE` from SOCRBASE;