use kladr;


optimize table DOMA;

optimize table FLAT;

-- ALTNAMES
select 'Updating ALTNAMES...' as ' ';

optimize table ALTNAMES;

-- добавляем в таблицу ALTNAMES информацию об удаленных объектах:
select 'Searching old codes...' as ' ';
insert ignore into ALTNAMES
select k1.CODE as `OLDCODE`, k2.CODE as `NEWCODE`, 'K' as `LEVEL` from KLADR k1, KLADR k2
where right(k2.CODE, 2) = '99'
and k1.CODE = CONCAT(left(k2.CODE, 11), '00');

-- KLADR
select 'Updating KLADR... ' as ' ';

select 'Restoring old information...' as ' ';

-- восстанавливаем инфисы:
update KLADR, KLADR_infis
set KLADR.infis = KLADR_infis.infis
where KLADR.prefix = KLADR_infis.prefix
and KLADR.NAME = KLADR_infis.NAME
and KLADR.SOCR = KLADR_infis.SOCR
and KLADR.STATUS = KLADR_infis.STATUS;

optimize table KLADR;


-- STREET
select 'Updating STREET... Please wait.' as ' ';

-- добавляем в таблицу ALTNAMES информацию об удаленных объектах:
select 'Searching old codes...' as ' ';
insert ignore into ALTNAMES
select s1.CODE as `OLDCODE`, s2.CODE as `NEWCODE`, 'S' as `LEVEL` from STREET s1, STREET s2
where right(s2.CODE, 2) = '99'
and s1.CODE = CONCAT(left(s2.CODE, 15), '00');

-- восстанавливаем инфисы:
select 'Restoring old information...' as ' ';
update STREET, STREET_infis
set STREET.infis = STREET_infis.infis
where STREET.CODE like '78%'
and STREET.NAME = STREET_infis.NAME
and STREET.SOCR = STREET_infis.SOCR;
update STREET
set STREET.infis = '*'
where STREET.CODE not like '78%';
optimize table STREET;


-- DOMA
select 'Updating DOMA... Please wait.' as ' ';
UPDATE DOMA SET flatHouseList = unwindHouseSpecification(NAME);



-- SOCRBASE
select 'Updating SOCRBASE...' as ' ';

-- восстанавливаем инфисы:
select 'Restoring old information...' as ' ';
update SOCRBASE, SOCRBASE_infis
set SOCRBASE.infisCODE = SOCRBASE_infis.infis
where SOCRBASE.`LEVEL` = SOCRBASE_infis.`LEVEL`
and SOCRBASE.SOCRNAME = SOCRBASE_infis.SOCRNAME;

-- Обновляем ИНФИсовские таблицы:
-- infisAREA:
select 'Updating infisAREA...' as ' ';
update infisAREA, ALTNAMES -- обновляем измененные коды
set infisAREA.KLADR = ALTNAMES.NEWCODE
where infisAREA.KLADR = ALTNAMES.OLDCODE
and exists
(select CODE from KLADR where KLADR.CODE = ALTNAMES.NEWCODE); -- обновляем только те, для кого новые коды появились в таблице !!!
select 'Updating infisREGION...' as ' ';
update infisREGION, ALTNAMES -- обновляем измененные коды
set infisREGION.KLADR = ALTNAMES.NEWCODE,
    infisREGION.kladrPrefix = left(ALTNAMES.NEWCODE, 2)
where infisREGION.KLADR = ALTNAMES.OLDCODE
and exists
(select CODE from KLADR where KLADR.CODE = ALTNAMES.NEWCODE); -- обновляем только те, для кого новые коды появились в таблице !!!
select 'Updating infisSTREET...' as ' ';
update infisSTREET, ALTNAMES -- обновляем измененные коды
set infisSTREET.KLADR = ALTNAMES.NEWCODE
where infisSTREET.KLADR = ALTNAMES.OLDCODE
and exists
(select CODE from STREET where STREET.CODE = ALTNAMES.NEWCODE); -- обновляем только те, для кого новые коды появились в таблице !!!


select 'Updating is successfull!' as ' ';