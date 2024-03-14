use kladr;

-- OKATO
select 'Updating OKATO... Please wait.' as ' ';

select 'Storing old information...' as ' ';

-- delimiter //
-- drop function if exists getOKATOCode//
-- create function getOKATOCode(P0 char(2), P1 char(3), P2 char(3))
-- returns varchar(8)
-- language SQL
-- deterministic
-- comment 'Get OKATO code from P0, P1, P2 components'
-- begin
-- if P2 = '000' then
--    if P1 = '000' then
--	return P0;
--    else
--	return concat(P0, P1);
--    end if;
-- else
--    return concat(P0, P1, P2);
-- end if;
-- end;
-- //
-- delimiter ;

update `tmpOKATO`
set infis = '';
-- Сохраняем инфисы, сначала пытаясь определить их по имени, потом по кодам, потом по таблице KLADR Петербурга и Лен. области
update `tmpOKATO`, `OKATO`
set `tmpOKATO`.infis = `OKATO`.infis
where `tmpOKATO`.NAME  = `OKATO`.NAME;
update `tmpOKATO`, `OKATO`
set `tmpOKATO`.infis = `OKATO`.infis
where `tmpOKATO`.P0 = `OKATO`.P0
--and getOKATOCode(`tmpOKATO`.P0, `tmpOKATO`.P1, `tmpOKATO`.P2) = `OKATO`.CODE;
and if(tmpOKATO.P2 = '000', if(tmpOKATO.P1 = '000', tmpOKATO.P0, concat(tmpOKATO.P0, tmpOKATO.P1)), concat(tmpOKATO.P0, tmpOKATO.P1, tmpOKATO.P2)) = `OKATO`.CODE;
update `tmpOKATO`, `KLADR`
set `tmpOKATO`.infis = `KLADR`.infis
where ((`tmpOKATO`.P0 = '40' and `KLADR`.prefix = '78') or (`tmpOKATO`.P0 = '41' and `KLADR`.prefix = '47'))
and `tmpOKATO`.P1 = substr(`KLADR`.OCATD from 3 for 3)
and `tmpOKATO`.P2 = substr(`KLADR`.OCATD from 6 for 3)
and `tmpOKATO`.P3 = substr(`KLADR`.OCATD from 9 for 3)
and `tmpOKATO`.infis = ''
and `KLADR`.infis != '';

select 'Updating table...' as ' ';
delete from OKATO where 1;
insert into OKATO (CODE, NAME, P0, P1, P2, `CHECK`, infis)
--select distinct getOKATOCode(P0, P1, P2),
select distinct if(P2 = '000', if(P1 = '000', P0, concat(P0, P1)), concat(P0, P1, P2)),
		NAME,
		P0,
		if(P1='000', '', P1),
		if(P2='000', '', P2),
		' ', -- CHECK не заполняем!!!
		infis
from tmpOKATO
where P0 in ('03', '40', '41', '45', '47', '63'); -- импортируем только Краснодарский край, Питер, Лен. область, Москву, Мурманскую область, Саратовскую область;
-- нули заменяем на пустые строки

-- KLADR
--select 'Updating KLADR... Please wait.' as ' ';


select 'Updating is successfull!' as ' ';