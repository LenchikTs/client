-- Таблицы с данными

 CREATE TEMPORARY TABLE IF NOT EXISTS `tmpService` (
 `code` VARCHAR( 14 ) NOT NULL COMMENT 'код медицинской услуги',
 `name` VARCHAR( 120 ) NOT NULL COMMENT 'краткое наименование медицинской услуги',
 `name_long` VARCHAR( 250 ) NULL COMMENT 'полное наименование медицинской услуги',
 `kolich` INT( 3 ) NULL COMMENT 'плановая длительность лечения ',
 `var` INT( 2 ) NULL COMMENT 'допустимое отклонение от плановой длительности лечения',
 `ed` VARCHAR( 10 ) NULL COMMENT 'единица измерения',
 `uet` DOUBLE NULL COMMENT 'количество УЕТ',
 `code_base` VARCHAR( 14 ) NULL COMMENT 'код базовой услуги',
 `datn` DATE NULL COMMENT 'дата начала действия',
 `dato` DATE NULL COMMENT 'дата окончания действия',
 `is_stand` VARCHAR( 1 ) NULL COMMENT 'Признак услуги для контроля выполнения',
 `not_oms` VARCHAR( 1 ) NULL COMMENT 'Признак  услуги в системе ОМС (0-в системе ОМС;1-не в системе ОМС)',
 `mes_id` INT( 11 ) NULL ,
 `mes_type` TINYINT( 1 ) NULL ,
 `mrbService_id` INT( 11 ) NULL ,
 `mrbService_type` TINYINT( 1 ) NULL ,
  UNIQUE (`code`),
  INDEX ( `is_stand` ( 1 ) )
 ) ENGINE = MYISAM DEFAULT CHARSET=utf8;

CREATE TEMPORARY TABLE IF NOT EXISTS `tmpStandart` (
 `code` VARCHAR( 14 ) NOT NULL COMMENT 'код стандарта',
 `name` VARCHAR( 120 ) NOT NULL COMMENT 'краткое наименование стандарта',
 `name_long` VARCHAR( 250 ) NULL COMMENT 'полное наименование стандарта',
 `uet` DOUBLE NULL COMMENT 'количество УЕТ',
 `mes_id` INT( 11 ) NULL ,
 `mes_type` TINYINT( 1 ) NULL ,
 `kolich` INT( 3 ) NULL COMMENT 'плановая длительность лечения ',
 `var` INT( 2 ) NULL COMMENT 'допустимое отклонение от плановой длительности лечения',
  UNIQUE (`code`)
) ENGINE = MYISAM DEFAULT CHARSET=utf8;


CREATE TEMPORARY TABLE IF NOT EXISTS `tmpServiceStandart` (
`code` VARCHAR( 14 ) NOT NULL COMMENT 'код стандарта оказания медицинской помощи',
 `code_pr` VARCHAR( 14 ) NOT NULL COMMENT 'код простой ,сложной и комплексной медицинской услуги',
 `kol` INT( 3 ) NOT NULL COMMENT 'кратность',
 `proc` INT( 3 ) NOT NULL COMMENT 'процент применяемости',
 `code_block` VARCHAR( 1 ) NULL COMMENT 'Код блока (лечение/диагностика)',
 `MesService_id` INT( 11 ) NULL ,
 `MesService_type` TINYINT( 1 ) NULL 
) ENGINE = MYISAM DEFAULT CHARSET=utf8;

CREATE TEMPORARY TABLE IF NOT EXISTS `tmpMKBStandart` (
`mkbx` VARCHAR( 5 ) NOT NULL COMMENT 'Код МКБ',
 `kstand` VARCHAR( 14 ) NOT NULL COMMENT 'Код стандарта оказания  медицинской помощи',
 `MesMKB_id` INT( 11 ) NULL ,
 `MesMKB_type` TINYINT( 1 ) NULL 
) ENGINE = MYISAM DEFAULT CHARSET=utf8;

-- временная таблица для лекарств

CREATE TEMPORARY TABLE IF NOT EXISTS `tmpMedicament` (
  `CODETRN` varchar(10) NOT NULL COMMENT 'Код торгового наименования',
  `NAMETRNS` varchar(254) NOT NULL COMMENT 'Наименование торгового наименования, краткое',
  `NAMETRNF` varchar(254) NOT NULL COMMENT 'Наименование торгового наименования, полное',
  `CODEFTG` varchar(3) NOT NULL COMMENT 'Код фармакотерапевтических групп',
  `CODEATH` varchar(10) NOT NULL COMMENT 'Код АТХ',
  `CODEMNN` varchar(10) NOT NULL COMMENT 'Код международного непатентованного наименования',
  `LEK_FORM` varchar(254) NULL COMMENT 'Лекарственная форма',
  `ED_IZM` varchar(254) NOT NULL COMMENT 'Единица измерения',
  `DATN` date NULL COMMENT 'Дата начала действия',
  `DATO` date NULL COMMENT 'Дата окончания действия',
  `CENAUP` float(10) NOT NULL COMMENT 'Стоимость упаковки',
  `PROIZV` varchar(254) NULL COMMENT 'Производитель',
  `mrbMedicament_id` int(11) NULL,
  `mrbMedicament_type` tinyint(1) NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- временная таблица для вхождения услуг в лекарства

 CREATE TEMPORARY TABLE IF NOT EXISTS `tmpMedicamentStandart` (
 `KSTAND` VARCHAR( 14 ) NOT NULL COMMENT 'Код стандарта ОМП',
 `CODETRN` VARCHAR( 10 ) NOT NULL COMMENT 'Код торгового наименования',
 `CH_NAZN` FLOAT( 7 ) NOT NULL COMMENT 'Частота назначения',
 `DOZA` FLOAT( 7 ) NOT NULL COMMENT 'Разовая доза',
 `VVEDEN` VARCHAR( 30 ) NOT NULL COMMENT 'Путь введения',
 `KOL` INT( 5 ) NOT NULL COMMENT 'Кратность',
 `KURS` INT( 5 ) NOT NULL COMMENT 'Курс',
 `OOD` FLOAT( 7 ) NOT NULL COMMENT 'ООД',
 `EKD` FLOAT( 7 ) NOT NULL COMMENT 'ЭКД',
 `MES_medicament_id` INT( 11 ) NULL ,
 `MES_medicament_type` TINYINT( 1 ) NULL 
 ) ENGINE = MYISAM DEFAULT CHARSET=utf8;



-- Таблицы со вспомогательными объектами

CREATE TEMPORARY TABLE IF NOT EXISTS `tmpSpeciality` (
  `code` varchar(3) NOT NULL,
  `name` varchar(100) NOT NULL,
  `mrbMESGRoup_id` INT( 11 ) NULL,
  `sertification_code` VARCHAR( 8 ) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO `tmpSpeciality` (`code`, `name`, `mrbMESGRoup_id`, `sertification_code`) VALUES
('001', 'акушерство и гинекология', NULL, '27'),
('002', 'аллергология и иммунология', NULL, '28'),
('003', 'анестезиология и реаниматология', NULL, '59'),
('004', 'гастроэнтерология', NULL, '29'),
('005', 'гематология', NULL, '30'),
('006', 'генетика', NULL, '00'),
('007', 'гериатрия', NULL, '31'),
('008', 'дерматовенерология', NULL, '32'),
('009', 'детская онкология', NULL, '33'),
('010', 'детская хирургия', NULL, '35'),
('011', 'детская эндокринология', NULL, '34 '),
('012', 'диабетология', NULL, '34'),
('013', 'диетология', NULL, '60'),
('014', 'инфекционные болезни', 6, '36'),
('015', 'кардиология', 1, '37'),
('016', 'клиническая лабораторная диагностика', NULL, '00'),
('017', 'клиническая фармакология', NULL, '00'),
('018', 'колопроктология', NULL, '50'),
('019', 'лабораторная генетика', NULL, '00'),
('020', 'лечебная физкультура и спорт', NULL, '57'),
('021', 'социальная гигиена, санитария и эпидемио', NULL, '00'),
('022', 'мануальная терапия', NULL, '43'),
('023', 'неврология', 2, '38'),
('024', 'нейрохирургия', NULL, '51'),
('025', 'нефрология', NULL, '45'),
('026', 'общая врачебная практика (семейная медиц', NULL, '60'),
('027', 'онкология', NULL, '33'),
('028', 'оториноларингология', 5, '39'),
('029', 'офтальмология', 4, '40'),
('031', 'педиатрия', NULL, '43'),
('032', 'неонатология', NULL, '55'),
('033', 'профпатология', NULL, '00'),
('034', 'психотерапия', NULL, '00'),
('035', 'психиатрия', NULL, '41'),
('036', 'Психиатрия - наркология', NULL, '42'),
('037', 'пульмонология', 3, '46'),
('038', 'радиология', NULL, '00'),
('039', 'рентгенология', NULL, '00'),
('040', 'ревматология', NULL, '47'),
('041', 'рефлексотерапия', NULL, '00'),
('042', 'сексология', NULL, '27'),
('043', 'сердечно- сосудистая хирургия', 1, '52'),
('044', 'скорая медицинская помощь', NULL, '00'),
('045', 'судебно- медицинская экспертиза', NULL, '00'),
('046', 'сурдология- оториноларингология', 5, '39'),
('047', 'терапия', NULL, '43'),
('048', 'токсикология', NULL, '44'),
('049', 'торакальная хирургия', NULL, '53'),
('050', 'травматология и ортопедия', NULL, '48'),
('051', 'трансфузиология', NULL, '00'),
('052', 'ультразвуковая диагностика', NULL, '00'),
('053', 'урология', NULL, '56'),
('054', 'физиотерапия', NULL, '00'),
('055', 'фтизиатрия', NULL, '49'),
('056', 'функциональная диагностика', NULL, '00'),
('057', 'хирургия', NULL, '35'),
('058', 'эндокринология', NULL, '34'),
('059', 'эндоскопия', NULL, '00'),
('060', 'бактериология', 6, '36'),
('061', 'вирусология', 6, '36'),
('062', 'эпидемиология', 6, '36'),
('063', 'ортодонтия', NULL, '54'),
('064', 'стоматология детская', NULL, '54'),
('065', 'стоматология терапевтическая', NULL, '54'),
('066', 'стоматология ортопедическая', NULL, '54'),
('067', 'стоматология хирургическая', NULL, '54'),
('068', 'челюстно- лицевая хирургия', NULL, '54'),
('069', 'прочие', NULL, '00'),
('070', 'гипер-(гипо) барическая оксигенация', NULL, '00');


CREATE TEMPORARY TABLE IF NOT EXISTS `tmpAgeGroup` (
`code` VARCHAR( 1 ) NOT NULL ,
 `mes_code` VARCHAR( 8 ) NOT NULL ,
 `name` VARCHAR( 128 ) NOT NULL 
) ENGINE = MYISAM DEFAULT CHARSET=utf8;

INSERT INTO `tmpAgeGroup` (`code` , `mes_code` , `name` )
VALUES ('0', '0', 'все'),
 ('1', '2', 'дети'),
 ('2', '1', 'взрослые');


CREATE TEMPORARY TABLE IF NOT EXISTS `tmpStateBadness` (
`code` VARCHAR( 1 ) NOT NULL ,
 `mes_code` VARCHAR( 8 ) NOT NULL ,
 `name` VARCHAR( 128 ) NOT NULL 
) ENGINE = MYISAM DEFAULT CHARSET=utf8;
INSERT INTO `tmpStateBadness` (`code` , `mes_code` , `name` )
VALUES ('0', '0', 'любая'),
	 ('1', '1', 'первая / легкая /минимальная активность'),
	 ('2', '2', 'вторая / средней тяжести / слабовыраженная'),
	 ('3', '5', 'третья / тяжелая / умеренная'),
	 ('4', '3', 'четвертая / крайне тяжелая /выраженная');

CREATE TEMPORARY TABLE IF NOT EXISTS `tmpDiseaseClass` (
`ClassID` VARCHAR( 8 ) NOT NULL ,
 `begMKB` VARCHAR( 8 ) NOT NULL ,
 `endMKB` VARCHAR( 8 ) NOT NULL ,
 `code` VARCHAR( 8 ) NOT NULL ,
 `name` VARCHAR( 128 ) NOT NULL 
) ENGINE = MYISAM DEFAULT CHARSET=utf8;

INSERT INTO `tmpDiseaseClass` (`ClassID`, `begMKB`, `endMKB`, `code`, `name`) VALUES
('I', 'A00', 'A00', '02', 'особо опасные инфекции'),
('I', 'A01', 'A09', '01', 'инфекционные и паразитарные заболевания'),
('I', 'A15', 'A19', '03', 'туберкулез'),
('I', 'A20', 'A22', '02', 'особо опасные инфекции'),
('I', 'A23', 'A49', '01', 'инфекционные и паразитарные заболевания'),
('I', 'A50', 'A64', '04', 'венерические заболевания'),
('I', 'A65', 'B02', '01', 'инфекционные и паразитарные заболевания'),
('I', 'B03', 'B04', '02', 'особо опасные инфекции'),
('I', 'B05', 'B19', '01', 'инфекционные и паразитарные заболевания'),
('I', 'B20', 'B24', '05', 'ВИЧ-инфекция'),
('II', 'C00', 'D48', '06', 'новообразования'),
('III', 'D50', 'D77', '07', 'болезни крови и кроветворных органов'),
('III', 'D80', 'D89', '08', 'нарушения иммунитета'),
('IV', 'E00', 'E35', '09', 'болезни эндокринной системы'),
('IV', 'E40', 'E90', '10', 'расстройства питания и нарушения обмена'),
('V', 'F00', 'F99', '11', 'психические расстройства и расстройства поведения'),
('VI', 'G00', 'G99', '12', 'болезни нервной системы'),
('VII', 'H00', 'H59', '13', 'болезни глаза и его придаточного аппарата'),
('VIII', 'H60', 'H95', '14', 'болезни ЛОР-органов'),
('IX', 'I00', 'I99', '15', 'болезни системы кровообращения'),
('X', 'J00', 'J99', '16', 'болезни органов дыхания'),
('XI', 'K00', 'K93', '17', 'болезни органов пищеварения'),
('XII', 'L00', 'L99', '18', 'болезни кожи и подкожной клетчатки'),
('XIII', 'M00', 'M99', '19', 'болезни костно-мышечной системы и соединительной ткани'),
('XIV', 'N00', 'N99', '20', 'болезни мочеполовой системы'),
('XV', 'O00', 'O99', '21', 'беременность, роды и послеродовой период'),
('XVI', 'P00', 'P96', '21', 'беременность, роды и послеродовой период'),
('XVII', 'Q00', 'Q99', '21', 'беременность, роды и послеродовой период'),
('XVIII', 'R00', 'R99', '00', 'не определен'),
('XIX', 'S00', 'T35', '22', 'травмы'),
('XIX', 'T36', 'T65', '23', 'отравления'),
('XIX', 'T66', 'T98', '00', 'не определен'),
('XX', 'V01', 'Y98', '00', 'не определен'),
('XXI', 'Z00', 'Z99', '00', 'не определен');







