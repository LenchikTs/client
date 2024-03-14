-- s11.AddressHouse:

select 'Исправляем ошибки в кодах городов: ' as ' ';
select concat(format(count(*), 0), ' ошибок исправляется...') as ' ' from AddressHouse
where AddressHouse.KLADRCode = '78000000000';
update AddressHouse
set AddressHouse.KLADRCode = '7800000000000',
    AddressHouse.modifyDatetime = now()
where AddressHouse.KLADRCode = '78000000000';

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
-- а такой вариант написать?
--select concat(format(count(*), 0), ' кодов будет когда-нибудь изменено.') as ' ' from AddressHouse, kladr.ALTNAMES
--where AddressHouse.KLADRStreetCode = ALTNAMES.OLDCODE
--and not exists
--(
--select CODE from kladr.STREET
--where STREET.CODE = ALTNAMES.NEWCODE
--);



select 'Исправляем ошибки в ОКАТО организаций: ' as ' ';
select concat(format(count(*), 0), ' ошибок исправляется...') as ' ' from Organisation
where Organisation.OKATO = '0';
update Organisation
set Organisation.OKATO = '',
    Organisation.modifyDatetime = now()
where Organisation.OKATO = '0';

select 'Исправление ошибок завершено!' as ' '