

--select 'Создание вспомогательных функций' as ' ';

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
-- импортируем те, у которых is_stand = 1

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
where left(code, 1) = 'S';

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
-- or (tmpService.code like 'A%' and mes.mrbService.code like 'А%'
-- and substr(tmpService.code from 2) = substr(mes.mrbService.code from 2))
-- or (tmpService.code like 'B%' and mes.mrbService.code like 'В%'
-- and substr(tmpService.code from 2) = substr(mes.mrbService.code from 2))
-- or (tmpService.code like 'D%' and mes.mrbService.code like 'Д%'
-- and substr(tmpService.code from 2) = substr(mes.mrbService.code from 2))
-- or (tmpService.code like 'F%' and mes.mrbService.code like 'Ф%'
-- and substr(tmpService.code from 2) = substr(mes.mrbService.code from 2));

select 'Добавление услуг...' as ' ';
-- импортируем те, у которых is_stand = 0
update tmpService
set mrbService_type = 5
where left(code, 1) != 'S'
and mrbService_type = 0;

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
left join rbServiceType on rbServiceType.section = left(tmpService.code, 1)
			and rbServiceType.code = substr(tmpService.code from 2 for 2)
left join rbServiceGroup on rbServiceGroup.id = rbServiceType.group_id
left join mes.mrbServiceGroup on mes.mrbServiceGroup.code = rbServiceGroup.regionalCode
where mrbService_type = 5;

select 'Установление соответствий для добавленных услуг...' as ' ';
update tmpService, mes.mrbService
set tmpService.mrbService_id = mes.mrbService.id,
    tmpService.mrbService_type = 2
where left(tmpService.code, 1) != 'S'
and tmpService.code = mes.mrbService.code
and tmpService.mrbService_type = 5;








select 'Очищаем базу включений услуг в стандарты...' as ' ';
delete from mes.MES_service;

select 'Импорт включений услуг в стандарты...' as ' ';

update tmpServiceStandart
set MesService_type = 0
where MesService_type is NULL;


select 'Установление соответствий для включений услуг в стандарты...' as ' ';
-- соответствие по коду стандарта, коду услуги и группировке.
-- Группировка: 0 - не задано (NULL), 1 - лечение (l) , 2 - диагностика (d)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
update tmpServiceStandart
left join tmpStandart on tmpStandart.code = tmpServiceStandart.code
left join tmpService on (tmpService.code = tmpServiceStandart.code_pr),
mes.MES_service
set tmpServiceStandart.MesService_id = mes.MES_service.id,
tmpServiceStandart.MesService_type = 2
where mes.MES_service.master_id = tmpStandart.mes_id
and mes.MES_service.service_id = tmpService.mrbService_id
and mes.MES_service.groupCode = 0 --((mes.MES_service.groupCode = 0 and tmpServiceStandart.code_block is NULL)
	--or (mes.MES_service.groupCode = 1 and tmpServiceStandart.code_block = 'l')
	--or (mes.MES_service.groupCode = 2 and tmpServiceStandart.code_block = 'd'))
and tmpServiceStandart.MesService_type = 0;

select 'Добавление включений услуг в стандарты...' as ' ';
update tmpServiceStandart
set MesService_type = 5
where MesService_type = 0;

insert into mes.MES_service(master_id, service_id, groupCode, averageQnt, necessity)
select tmpStandart.mes_id as master_id,
	tmpService.mrbService_id as service_id,
	0 as groupCode, --if(code_block = 'l', 1, if(code_block = 'd', 2, 0)) as groupCode,
	kol as averageQnt,
	proc*0.01 as necessity
from tmpServiceStandart
left join tmpStandart on tmpStandart.code = tmpServiceStandart.code
left join tmpService on (tmpService.code =  tmpServiceStandart.code_pr)
where tmpService.mrbService_id is not NULL
and MesService_type = 5;

select 'Установление соответствий для добавленных включений услуг в стандарты...' as ' ';
update tmpServiceStandart
left join tmpStandart on tmpStandart.code = tmpServiceStandart.code
left join tmpService on (tmpService.code =  tmpServiceStandart.code_pr),
mes.MES_service
set tmpServiceStandart.MesService_id = mes.MES_service.id,
tmpServiceStandart.MesService_type = 2
where mes.MES_service.master_id = tmpStandart.mes_id
and mes.MES_service.service_id = tmpService.mrbService_id
and ((mes.MES_service.groupCode = 0 and tmpServiceStandart.code_block is NULL)
	or (mes.MES_service.groupCode = 1 and tmpServiceStandart.code_block = 'l')
	or (mes.MES_service.groupCode = 2 and tmpServiceStandart.code_block = 'd'))
and tmpServiceStandart.MesService_type = 5;

select 'Для услуг с множественным включением в стандарты оставляем одну с максимальной применяемостью' as ' ';
delete from mes.MES_service
where mes.MES_service.id in
      (select deletedRecs.id
       from (select ms1.id
             from mes.MES_service ms1
             where exists(select *
                          from mes.MES_service ms2
                          where ms1.id <> ms2.id and
                                ms1.master_id = ms2.master_id and
                                ms1.service_id = ms2.service_id and
                                (ms1.necessity < ms2.necessity or
                                 (abs(ms1.necessity - ms2.necessity) < 0.0001 and
                                  ms1.id < ms2.id)))) as deletedRecs);











select 'Импорт кодов МКБ в стандартах...' as ' ';
update tmpMKBStandart
set MesMKB_type = 0
where MesMKB_type is NULL;

select 'Установление соответствий для кодов МКБ в стандартах...' as ' ';
-- соответствие, как ни удивительно, устанавливаем по стандарту и коду МКБ:)
update tmpMKBStandart
left join tmpStandart on tmpMKBStandart.kstand = tmpStandart.code,
mes.MES_mkb
set tmpMKBStandart.MesMKB_id = mes.MES_mkb.id,
tmpMKBStandart.MesMKB_type = 2
where tmpStandart.mes_id = mes.MES_mkb.master_id
and tmpMKBStandart.mkbx = mes.MES_mkb.mkb
and tmpMKBStandart.MesMKB_type = 0;

select 'Добавление кодов МКБ в стандартах...' as ' ';
update tmpMKBStandart
set MesMKB_type = 5
where MesMKB_type = 0;

insert into mes.MES_mkb(master_id, mkb)
select	tmpStandart.mes_id,
	tmpMKBStandart.mkbx
from tmpMKBStandart
left join tmpStandart on tmpMKBStandart.kstand = tmpStandart.code
where tmpStandart.mes_id is not null
and MesMKB_type = 5;


select 'Установление соответствий для добавленных кодов МКБ в стандартах...' as ' ';
update tmpMKBStandart
left join tmpStandart on tmpMKBStandart.kstand = tmpStandart.code,
mes.MES_mkb
set tmpMKBStandart.MesMKB_id = mes.MES_mkb.id,
tmpMKBStandart.MesMKB_type = 2
where tmpStandart.mes_id = mes.MES_mkb.master_id
and tmpMKBStandart.mkbx = mes.MES_mkb.mkb
and tmpMKBStandart.MesMKB_type = 5;


select 'Определение моделей пациента...' as ' ';
update tmpStandart
left join tmpSpeciality on tmpSpeciality.code = substr(tmpStandart.code from 2 for 3)
left join mes.MES on tmpStandart.mes_id = mes.MES.id and tmpStandart.mes_type = 2
left join tmpStateBadness on tmpStateBadness.code = substr(mes.MES.code from 7 for 1)
left join tmpAgeGroup on tmpAgeGroup.code = substr(mes.MES.code from 9 for 1)
left join mes.MES_mkb on mes.MES_mkb.master_id = mes.MES.id
left join tmpDiseaseClass on (left(mes.MES_mkb.mkb, 3) >= tmpDiseaseClass.begMKB and left(mes.MES_mkb.mkb, 3) <= tmpDiseaseClass.endMKB)
set mes.MES.patientModel = concat(if(exists(select * from mes.MES_mkb where master_id = mes.MES.id and left(mes.MES_mkb.mkb, 1) in('A', 'T')), 'Н', 'С'), '.',
			 'И', '.',
			 tmpDiseaseClass.code, '.',
			 tmpSpeciality.sertification_code, '.',
			 '5', '.',
			 tmpStateBadness.mes_code, '.',
			 tmpAgeGroup.mes_code, '.',
			 '0', '.',
			 '0', '.',
			 'Х')
where mes.MES.patientModel = '';




select 'Импорт лекарств...' as ' ';
update tmpMedicament
set mrbMedicament_type = 0
where mrbMedicament_type is NULL;

-- хитрый финт ушами: для разбора названия используем ненужные поля CODEATH и CODEMNN:
update tmpMedicament
set CODEATH = instr(tmpMedicament.NAMETRNS, ','),
    CODEMNN = instr(tmpMedicament.NAMETRNS, ',№');

select 'Установление соответствий для лекарств...' as ' ';
-- устанавливаем соответствие по торговому наименованию
update tmpMedicament, mes.mrbMedicament
set tmpMedicament.mrbMedicament_id = mes.mrbMedicament.id,
tmpMedicament.mrbMedicament_type = 2
where tmpMedicament.mrbMedicament_type = 0
and tmpMedicament.NAMETRNF = mes.mrbMedicament.tradeName;
--and tmpMedicament.CENAUP = mes.mrbMedicament.packPrice;

select 'Добавление лекарств...' as ' ';
-- добавляем все???
update tmpMedicament
set mrbMedicament_type = 5
where mrbMedicament_type = 0;

insert into mes.mrbMedicament(code, name, tradeName, dosage, form, dosageForm_id, packSize, packPrice, unitPrice)
select CODETRN as code,
tmpMedicament.NAMETRNF as name,
tmpMedicament.NAMETRNF as tradeName,
if(CODEATH > 0, substr(tmpMedicament.NAMETRNS from CODEATH+1), '') as dosage,
LEK_FORM as form,
mes.mrbMedicamentDosageForm.id as dosageForm_id,
if(CODEMNN > 0, substr(tmpMedicament.NAMETRNS from CODEMNN + 2), 1) as packSize,
round(CENAUP, 2) as packPrice,
0 as unitPrice
from tmpMedicament
left join mes.mrbMedicamentDosageForm on mes.mrbMedicamentDosageForm.code = '0'
where mrbMedicament_type = 5;

select 'Установление соответствий для добавленных лекарств...' as ' ';
update tmpMedicament, mes.mrbMedicament
set tmpMedicament.mrbMedicament_id = mes.mrbMedicament.id,
tmpMedicament.mrbMedicament_type = 2
where tmpMedicament.mrbMedicament_type = 5
and left(tmpMedicament.NAMETRNF, instr(tmpMedicament.NAMETRNF, ',')-1) = mes.mrbMedicament.tradeName
and tmpMedicament.CENAUP = mes.mrbMedicament.packPrice;

-- почистим дозировки от номеров 
update mes.mrbMedicament
set dosage = left(dosage, instr(dosage, ',№')-1)
where instr(dosage, ',№') > 0;

-- установим цены:
update mes.mrbMedicament
set unitPrice = round(packPrice / packSize, 2)
where unitPrice = 0;


select 'Очищаем базу включений лекарств в стандарты...' as ' ';
delete from mes.MES_medicament;

select 'Импорт вхождений лекарств в стандарты...' as ' ';
update tmpMedicamentStandart
set Mes_medicament_type = 0
where Mes_medicament_type is NULL;

select 'Установление соответствий для вхождений лекарств в стандарты...' as ' ';
-- устанавливаем соответствие по id стандарта и коду медикамента
update tmpMedicamentStandart
	left join tmpStandart on tmpMedicamentStandart.KSTAND = tmpStandart.CODE, 
	mes.MES_medicament
	left join mes.MES on mes.MES_medicament.master_id = mes.MES.id
set 	tmpMedicamentStandart.Mes_medicament_id = mes.MES_medicament.id,
	tmpMedicamentStandart.Mes_medicament_type = 2
where	tmpMedicamentStandart.Mes_medicament_type = 0
	and tmpStandart.mes_id = mes.MES.id
	and tmpStandart.mes_type = 2
	and tmpMedicamentStandart.CODETRN = mes.MES_medicament.medicamentCode;


select 'Добавление вхождений лекарств в стандарты...' as ' ';
-- добавляем всё:
update tmpMedicamentStandart
set Mes_medicament_type = 5
where Mes_medicament_type = 0;

-- изврат для проверки работы!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
--update tmpMedicamentStandart
--set KSTAND = 'S06910000001'
--where KSTAND = 'S01510002004';

insert into mes.MES_medicament(master_id, medicamentCode, dosage, dosageForm_id, averageQnt, necessity)
select	tmpStandart.mes_id as master_id,
	tmpMedicamentStandart.CODETRN as medicamentCode,
	round(DOZA, 2) as dosage,
	mes.mrbMedicamentDosageForm.id as dosageForm_id,
	KURS as averageQnt,
	round(CH_NAZN, 2) as necessity
from tmpMedicamentStandart
left join tmpStandart on tmpMedicamentStandart.KSTAND = tmpStandart.CODE
left join mes.mrbMedicamentDosageForm on mes.mrbMedicamentDosageForm.code = '0'
where Mes_medicament_type = 5;

select 'Установление соответствий для добавленных вхождений лекарств в стандарты...' as ' ';
update tmpMedicamentStandart
	left join tmpService on tmpMedicamentStandart.KSTAND = tmpService.CODE, 
	mes.MES_medicament
	left join mes.MES on mes.MES_medicament.master_id = mes.MES.id
set 	tmpMedicamentStandart.Mes_medicament_id = mes.MES_medicament.id,
	tmpMedicamentStandart.Mes_medicament_type = 2
where	tmpMedicamentStandart.Mes_medicament_type = 0
	and tmpService.mes_id = mes.MES.id
	and tmpService.mes_type = 5
	and tmpMedicamentStandart.CODETRN = mes.MES_medicament.medicamentCode;





--select 'Удаление временных функций...' as ' ';

--DROP FUNCTION `getMedicamentName`;


select 'Импорт завершён!' as ' ';