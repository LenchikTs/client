#!/usr/bin/env python
# -*- coding: utf-8 -*-
COMMAND = u"""

select 'Неправильные коды населенных пунктов в таблице s11.AddressHouse:' as ' ';
select concat(format(count(distinct KLADRCode, NAME), 0), ' кодов.') from AddressHouse
join kladr.KLADR on AddressHouse.KLADRCode = kladr.KLADR.CODE
where not exists
(select CODE from kladr.KLADR where AddressHouse.KLADRCode = KLADR.CODE);

select distinct KLADRCode, NAME from AddressHouse
join kladr.KLADR on AddressHouse.KLADRCode = kladr.KLADR.CODE
where not exists
(select CODE from kladr.KLADR where AddressHouse.KLADRCode = KLADR.CODE);


select 'Неправильные коды улиц в таблице s11.AddressHouse:' as ' ';
select concat(format(count(distinct KLADRStreetCode, NAME ), 0), ' кодов.') from AddressHouse
join kladr.STREET on AddressHouse.KLADRStreetCode = kladr.STREET.CODE
where KLADRStreetCode != '' and not exists -- Код улицы может быть пустой строкой!
(select CODE from kladr.STREET where AddressHouse.KLADRStreetCode = STREET.CODE);

select distinct KLADRStreetCode, NAME from AddressHouse
join kladr.STREET on AddressHouse.KLADRStreetCode = kladr.STREET.CODE
where KLADRStreetCode != '' and not exists -- Код улицы может быть пустой строкой!
(select CODE from kladr.STREET where AddressHouse.KLADRStreetCode = STREET.CODE);


select 'Неправильные коды OKATO в таблице s11.Organisation:' as ' ';
select concat(format(count(distinct OKATO, NAME), 0), ' кодов:') from Organisation
join kladr.OKATO on (OKATO.P0 = substr(Organisation.OKATO from 1 for 2)
 and (OKATO.P1 = substr(Organisation.OKATO from 3 for 3) or OKATO.P1 + '000' = substr(Organisation.OKATO from 3 for 3))
 and (OKATO.P2 = substr(Organisation.OKATO from 6 for 3) or OKATO.P2 + '000' = substr(Organisation.OKATO from 6 for 3)))
where OKATO != '' and not exists -- код ОКАТО организации может быть пустым!!!
(select CODE from kladr.OKATO
 where OKATO.P0 = substr(Organisation.OKATO from 1 for 2)
 and (OKATO.P1 = substr(Organisation.OKATO from 3 for 3) or OKATO.P1 + '000' = substr(Organisation.OKATO from 3 for 3))
 and (OKATO.P2 = substr(Organisation.OKATO from 6 for 3) or OKATO.P2 + '000' = substr(Organisation.OKATO from 6 for 3))
);

select distinct OKATO, NAME from Organisation
join kladr.OKATO on (OKATO.P0 = substr(Organisation.OKATO from 1 for 2)
 and (OKATO.P1 = substr(Organisation.OKATO from 3 for 3) or OKATO.P1 + '000' = substr(Organisation.OKATO from 3 for 3))
 and (OKATO.P2 = substr(Organisation.OKATO from 6 for 3) or OKATO.P2 + '000' = substr(Organisation.OKATO from 6 for 3)))
where OKATO != '' and not exists -- код ОКАТО организации может быть пустым!!!
(select CODE from kladr.OKATO
 where OKATO.P0 = substr(Organisation.OKATO from 1 for 2)
 and (OKATO.P1 = substr(Organisation.OKATO from 3 for 3) or OKATO.P1 + '000' = substr(Organisation.OKATO from 3 for 3))
 and (OKATO.P2 = substr(Organisation.OKATO from 6 for 3) or OKATO.P2 + '000' = substr(Organisation.OKATO from 6 for 3))
);








select 'Неправильные коды КЛАДР в таблице infisAREA:' as ' ';
select concat(format(count(*), 0), ' кодов.') from kladr.infisAREA
where KLADR != '' and not exists -- Код населенного пункта может быть пустой строкой!
(select CODE from kladr.KLADR where infisAREA.KLADR = KLADR.CODE);

select KLADR, NAME from kladr.infisAREA
where KLADR != '' and not exists -- Код населенного пункта может быть пустой строкой!
(select CODE from kladr.KLADR where infisAREA.KLADR = KLADR.CODE);


select 'Неправильные коды КЛАДР в таблице infisREGION:' as ' ';
select concat(format(count(*), 0), ' кодов.') from kladr.infisREGION
where KLADR != '' and not exists -- Код населенного пункта может быть пустой строкой!
(select CODE from kladr.KLADR where infisREGION.KLADR = KLADR.CODE);

select KLADR, NAME from kladr.infisREGION
where KLADR != '' and not exists -- Код населенного пункта может быть пустой строкой!
(select CODE from kladr.KLADR where infisREGION.KLADR = KLADR.CODE);


select 'Неправильные коды КЛАДР в таблице infisSTREET:' as ' ';
select concat(format(count(*), 0), ' кодов.') from kladr.infisSTREET
where KLADR != '' and left(KLADR, 3) != '001' and not exists -- Код улицы может быть пустой строкой!
(select CODE from kladr.STREET where infisSTREET.KLADR = STREET.CODE);

select KLADR, NAME from kladr.infisSTREET
where KLADR != '' and left(KLADR, 3) != '001' and not exists -- Код улицы может быть пустой строкой!
(select CODE from kladr.STREET where infisSTREET.KLADR = STREET.CODE);




select 'Неправильные коды ОКАТО в таблице KLADR:' as ' ';
select concat(format(count(distinct OCATD, NAME), 0), ' кодов:') from kladr.KLADR
where (KLADR.prefix = '47' or KLADR.prefix = '78') and not exists
(
select NAME from kladr.OKATO where 
`OKATO`.P0 = substr(`KLADR`.OCATD from 1 for 2)
and (`OKATO`.P1 = substr(`KLADR`.OCATD from 3 for 3) or `OKATO`.P1 + '000' = substr(`KLADR`.OCATD from 3 for 3))
and (`OKATO`.P2 = substr(`KLADR`.OCATD from 6 for 3) or `OKATO`.P2 + '000' = substr(`KLADR`.OCATD from 6 for 3))
--and `OKATO`.P3 = substr(`KLADR`.OCATD from 9 for 3)
);

select distinct OCATD, NAME from kladr.KLADR
where (KLADR.prefix = '47' or KLADR.prefix = '78') and not exists
(
select NAME from kladr.OKATO where 
`OKATO`.P0 = substr(`KLADR`.OCATD from 1 for 2)
and (`OKATO`.P1 = substr(`KLADR`.OCATD from 3 for 3) or `OKATO`.P1 + '000' = substr(`KLADR`.OCATD from 3 for 3))
and (`OKATO`.P2 = substr(`KLADR`.OCATD from 6 for 3) or `OKATO`.P2 + '000' = substr(`KLADR`.OCATD from 6 for 3))
--and `OKATO`.P3 = substr(`KLADR`.OCATD from 9 for 3)
);




select 'Неправильные коды ОКАТО в таблице STREET:' as ' ';
select concat(format(count(distinct OCATD, NAME), 0), ' кодов:') from kladr.STREET
where (CODE like '47%' or CODE like '78%') and 
OCATD != '' and not exists -- Код OKATO для улицы может быть пустой строкой!
(
select NAME from kladr.OKATO where 
`OKATO`.P0 = substr(`STREET`.OCATD from 1 for 2)
and (`OKATO`.P1 = substr(`STREET`.OCATD from 3 for 3) or `OKATO`.P1 + '000' = substr(`STREET`.OCATD from 3 for 3))
and (`OKATO`.P2 = substr(`STREET`.OCATD from 6 for 3) or `OKATO`.P2 + '000' = substr(`STREET`.OCATD from 6 for 3))
--and `OKATO`.P3 = substr(`STREET`.OCATD from 9 for 3)
);

select distinct OCATD, NAME from kladr.STREET
where (CODE like '47%' or CODE like '78%') and 
OCATD != '' and not exists -- Код OKATO для улицы может быть пустой строкой!
(
select NAME from kladr.OKATO where 
`OKATO`.P0 = substr(`STREET`.OCATD from 1 for 2)
and (`OKATO`.P1 = substr(`STREET`.OCATD from 3 for 3) or `OKATO`.P1 + '000' = substr(`STREET`.OCATD from 3 for 3))
and (`OKATO`.P2 = substr(`STREET`.OCATD from 6 for 3) or `OKATO`.P2 + '000' = substr(`STREET`.OCATD from 6 for 3))
--and `OKATO`.P3 = substr(`STREET`.OCATD from 9 for 3)
);


select 'Неправильные коды ОКАТО в таблице DOMA:' as ' ';
select concat(format(count(distinct OCATD, NAME), 0), ' кодов:') from kladr.DOMA
where (CODE like '47%' or CODE like '78%') and not exists
(
select NAME from kladr.OKATO where 
`OKATO`.P0 = substr(`DOMA`.OCATD from 1 for 2)
and (`OKATO`.P1 = substr(`DOMA`.OCATD from 3 for 3) or `OKATO`.P1 + '000' = substr(`DOMA`.OCATD from 3 for 3))
and (`OKATO`.P2 = substr(`DOMA`.OCATD from 6 for 3) or `OKATO`.P2 + '000' = substr(`DOMA`.OCATD from 6 for 3))
--and `OKATO`.P3 = substr(`DOMA`.OCATD from 9 for 3)
);

select distinct OCATD, NAME from kladr.DOMA
where (CODE like '47%' or CODE like '78%') and not exists
(
select NAME from kladr.OKATO where 
`OKATO`.P0 = substr(`DOMA`.OCATD from 1 for 2)
and (`OKATO`.P1 = substr(`DOMA`.OCATD from 3 for 3) or `OKATO`.P1 + '000' = substr(`DOMA`.OCATD from 3 for 3))
and (`OKATO`.P2 = substr(`DOMA`.OCATD from 6 for 3) or `OKATO`.P2 + '000' = substr(`DOMA`.OCATD from 6 for 3))
--and `OKATO`.P3 = substr(`DOMA`.OCATD from 9 for 3)
);




select 'Новые коды в таблице ALTNAMES, которые ссылаются на несуществующие объекты:' as ' ';
select concat(format(count(*), 0), ' кодов.') from kladr.ALTNAMES 
where not exists
(select CODE from kladr.KLADR where ALTNAMES.NEWCODE = KLADR.CODE
union
select CODE from kladr.STREET where ALTNAMES.NEWCODE = STREET.CODE
union
select CODE from kladr.DOMA where ALTNAMES.NEWCODE = DOMA.CODE);

select NEWCODE from kladr.ALTNAMES 
where not exists
(select CODE from kladr.KLADR where ALTNAMES.NEWCODE = KLADR.CODE
union
select CODE from kladr.STREET where ALTNAMES.NEWCODE = STREET.CODE
union
select CODE from kladr.DOMA where ALTNAMES.NEWCODE = DOMA.CODE);"""
