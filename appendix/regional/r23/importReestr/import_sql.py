#!/usr/bin/env python
# -*- coding: utf-8 -*-

COMMAND = u"""


--select 'Создание вспомогательных функций' as ' ';
SET SQL_SAFE_UPDATES = 0;
--DELIMITER //
--DROP FUNCTION IF EXISTS `getMedicamentName`//
--CREATE -- DEFINER=`root`@`localhost`
--FUNCTION `getMedicamentName`
-- ( aName VARCHAR(254) CHARSET utf8
-- ) RETURNS VARCHAR(254)
--    NO SQL
--    DETERMINISTIC
--    COMMENT 'returns name of medicament'
--BEGIN
--    RETURN aName;
--END //

--DROP FUNCTION IF EXISTS `getMedicamentDosage`//
--CREATE -- DEFINER=`root`@`localhost`
--FUNCTION `getMedicamentDosage`
-- ( aName VARCHAR(254) CHARSET utf8
-- ) RETURNS VARCHAR(254)
--    NO SQL
--    DETERMINISTIC
--    COMMENT 'returns dosage of medicament'
--BEGIN
--	DECLARE comma_pos INT(2);
--	SET comma_pos = instr(aName, ',');
--	IF comma_pos > 0 THEN
--		RETURN substr(aName from comma_pos + 1);
--	ELSE
--		RETURN '';
--	END IF;
--END //
--DELIMITER ;

select 'Импорт стандартов МЭС...' as ' ';
-- импортируем те, у которых code начинается на G

-- создаем отдельную табличку для стандартов и отделяем их от услуг - так удобнее:
insert ignore into tmpStandart(code, name, name_long, uet, mes_id, mes_type, kolich, var)
select	code,
	name,
	name_long,
	uet,
	mes_id,
	mes_type,
  kolich,
  var
from tmpService
where left(code, 1) = 'G';

update tmpStandart
set mes_type = 0
where mes_type is NULL;

select 'Установление соответствий для стандартов...' as ' ';
-- устанавливаем соответствие по коду
update tmpStandart, mes.MES
set tmpStandart.mes_id = mes.MES.id,
    tmpStandart.mes_type = 2,
    mes.MES.avgDuration = tmpStandart.kolich,
    mes.MES.minDuration = tmpStandart.kolich - tmpStandart.var,
    mes.MES.maxDuration = tmpStandart.kolich + tmpStandart.var
where tmpStandart.code = mes.MES.code
and tmpStandart.mes_type = 0;

select 'Добавление стандартов...' as ' ';
update tmpStandart
set mes_type = 5
where mes_type = 0;

insert into mes.MES(group_id, code, name, descr, KSGNorm, avgDuration, minDuration, maxDuration)
select distinct
	tmpSpeciality.mrbMESGRoup_id as group_id,
	tmpStandart.code,
	tmpStandart.name,
	tmpStandart.name_long as descr,
	uet as KSGNorm, -- ????????????
  tmpStandart.kolich,
  tmpStandart.kolich - tmpStandart.var,
  tmpStandart.kolich + tmpStandart.var
from tmpStandart
left join tmpSpeciality on tmpSpeciality.code = substr(tmpStandart.code from 2 for 3)
where mes_type = 5;

select 'Установление соответствий для добавленных стандартов...' as ' ';
update tmpStandart, mes.MES
set tmpStandart.mes_id = mes.MES.id,
    tmpStandart.mes_type = 2
where tmpStandart.code = mes.MES.code
and tmpStandart.mes_type = 5;

select 'Импорт услуг МЭС...' as ' ';
-- импортируем те, у которых is_stand = 0

update tmpService
set mrbService_type = 0
where mrbService_type is NULL;

select 'Установление соответствий для услуг...' as ' ';
-- устанавливаем соответствие услуг по коду с учётом идентичности русских в msrService и английских в источнике А и В

update tmpService
left join rbServiceType on rbServiceType.section = left(tmpService.code, 1)
                       and rbServiceType.code = substr(tmpService.code from 2 for 2)
left join rbServiceGroup on rbServiceGroup.id = rbServiceType.group_id
left join mes.mrbServiceGroup on mes.mrbServiceGroup.code = rbServiceGroup.regionalCode,
mes.mrbService
set tmpService.mrbService_id = mes.mrbService.id,
    tmpService.mrbService_type = 2,
    mes.mrbService.group_id = (case
                                 when mes.mrbServiceGroup.id is null then 55
                                 else mes.mrbServiceGroup.id
                               end)
where tmpService.code = mes.mrbService.code;

select 'Добавление услуг...' as ' ';
-- импортируем те, у которых is_stand = 0
update tmpService
set mrbService_type = 5
where left(code, 1) != 'S'
and mrbService_type = 0;

-- обновляем наименования действующих услуг
update tmpService
left join mes.mrbService m on m.code = tmpService.code and m.deleted = 0
set m.name = tmpService.name_long
where m.id is not null and substr(tmpService.code, 1, 1) not in  ('S', 'G')
and tmpService.dato is null;

insert into mes.mrbService(group_id, code, name, doctorWTU, paramedicalWTU)
select	distinct
  (case
     when mes.mrbServiceGroup.id is null then 55
     else mes.mrbServiceGroup.id
   end) as group_id,
	tmpService.code,
	name_long as name,
	uet as doctorWTU,
	0 as paramedicalWTU -- другого выхода нет!!!!!!!
from tmpService
left join mes.mrbService m2 on m2.code = tmpService.code and m2.deleted = 0
left join rbServiceType on rbServiceType.section = left(tmpService.code, 1)
			and rbServiceType.code = substr(tmpService.code from 2 for 2)
left join rbServiceGroup on rbServiceGroup.id = rbServiceType.group_id
left join mes.mrbServiceGroup on mes.mrbServiceGroup.code = rbServiceGroup.regionalCode
where m2.id is null and substr(tmpService.code, 1, 1) not in  ('S', 'G');

--select 'Удаление временных функций...' as ' ';

--DROP FUNCTION `getMedicamentName`;


update mes.MES m
left join tmpService s on s.code = m.code
set m.descr = s.name_long,
m.name = s.name,
m.endDate = s.dato
where s.code is not null and left(m.code, 1) in ('S','G');


CALL mes.UpdateMesfSpr69;
SET SQL_SAFE_UPDATES = 1;
select 'Импорт завершён!' as ' ';

"""
