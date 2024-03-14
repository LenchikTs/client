#!/usr/bin/env python
# -*- coding: utf-8 -*-
COMMAND = u"""

select 'Обновляем измененные кода городов: ' as ' ';
update AddressHouse, kladr.ALTNAMES -- обновляем измененные кода городов
set AddressHouse.KLADRCode = ALTNAMES.NEWCODE,
    AddressHouse.modifyDatetime = now()
where AddressHouse.KLADRCode = ALTNAMES.OLDCODE
and exists -- исправляем только те, для которых реально появились новые коды!!!!!!!!!!!!!!!!!!
(
select CODE from kladr.KLADR
where KLADR.CODE = ALTNAMES.NEWCODE
);
select concat(format(count(*), 0), ' измененных кодов.') as ' ' from AddressHouse, kladr.ALTNAMES
where AddressHouse.KLADRCode = ALTNAMES.OLDCODE
and exists
(
select CODE from kladr.KLADR
where KLADR.CODE = ALTNAMES.NEWCODE
);


select 'Обновляем измененные кода улиц: ' as ' ';
update AddressHouse, kladr.ALTNAMES -- обновляем измененные кода улиц
set AddressHouse.KLADRStreetCode = ALTNAMES.NEWCODE,
    AddressHouse.modifyDatetime = now()
where AddressHouse.KLADRStreetCode = ALTNAMES.OLDCODE
and exists -- исправляем только те, для которых реально появились новые коды!!!!!!!!!!!!!!!!!!
(
select CODE from kladr.STREET
where STREET.CODE = ALTNAMES.NEWCODE
);
select concat(format(count(*), 0), ' измененных кодов.') as ' ' from AddressHouse, kladr.ALTNAMES
where AddressHouse.KLADRStreetCode = ALTNAMES.OLDCODE
and exists
(
select CODE from kladr.STREET
where STREET.CODE = ALTNAMES.NEWCODE
);

select 'Обновляем переподчиненные коды нас. пунктов: ' as ' ';
  update AddressHouse ah
    LEFT JOIN kladr.ALTNAMES alt ON alt.OLDCODE = ah.KLADRCode
    set ah.KLADRCode = alt.NEWCODE, ah.modifyDatetime = now()
    WHERE alt.OLDCODE is not NULL
  and exists -- исправляем только те, для которых реально появились новые коды!!!!!!!!!!!!!!!!!!
(
select CODE from kladr.KLADR
where KLADR.CODE = alt.NEWCODE
); 
select 'Обновляем переподчиненные коды улиц: ' as ' ';
update AddressHouse ah
    LEFT JOIN kladr.ALTNAMES alt ON alt.OLDCODE = ah.KLADRStreetCode
    set ah.KLADRStreetCode = alt.NEWCODE, ah.modifyDatetime = now()
    WHERE alt.OLDCODE is not NULL
  and exists -- исправляем только те, для которых реально появились новые коды!!!!!!!!!!!!!!!!!!
(
select CODE from kladr.STREET
where STREET.CODE = alt.NEWCODE
); 

select 'Удаляем недействующие коды нас. пунктов из кладра: ' as ' ';
CREATE TEMPORARY TABLE IF NOT EXISTS kladr_tmp(id int, index(id));
INSERT INTO kladr_tmp(id)
SELECT k1.id from kladr.KLADR k1
where RIGHT(k1.CODE, 2) = '00'
      AND exists(select NULL from kladr.KLADR k2 where k2.CODE = CONCAT(left(k1.CODE, 11), '51'))
      AND NOT exists(select NULL from kladr.ALTNAMES a where a.NEWCODE = k1.CODE);
      
DELETE FROM kladr.KLADR
WHERE id IN (SELECT kladr_tmp.id FROM kladr_tmp);
DROP TEMPORARY TABLE IF EXISTS kladr_tmp;


select 'Удаляем недействующие коды нас. улиц из кладра: ' as ' ';
CREATE TEMPORARY TABLE IF NOT EXISTS street_tmp(code varchar(17), index(code));
INSERT INTO street_tmp(code)
SELECT s1.CODE from kladr.STREET s1
where RIGHT(s1.CODE, 2) = '00'
      AND exists(select NULL from kladr.STREET s2 where s2.CODE = CONCAT(left(s1.CODE, 15), '51'))
      AND NOT exists(select NULL from kladr.ALTNAMES a where a.NEWCODE = s1.CODE);

DELETE FROM kladr.STREET
WHERE CODE IN (SELECT street_tmp.code FROM street_tmp);
DROP TEMPORARY TABLE IF EXISTS street_tmp;


select 'Исправление ошибок завершено!' as ' '"""
