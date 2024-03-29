# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from StatReportF12Able_2021 import CStatReportF12Able_2021

MainRows = [
    ( u'Зарегистрировано заболеваний - всего', u'1.0', u'A00-T98'),
    ( u'в том числе: некоторые инфекционные и паразитарные болезни', u'2.0', u'A00-B99'),
    ( u'из них: кишечные инфекции', u'2.1', u'A00-A09'),
    ( u'менингококковая инфекция', u'2.2', u'A39'),
    ( u'вирусный гепатит', u'2.3', u'B15-B19'),
    ( u'из них хронический вирусный гепатит С', u'2.3.1', u'B18.2'),
    ( u'новообразования', u'3.0', u'C00-D48'),
    ( u'из них: злокачественные новообразования', u'3.1', u'C00-C96'),
    ( u'из них: злокачественные новообразования лимфоидной, кроветворной и родственных им тканей', u'3.1.1', u'C81-C96'),
    ( u'доброкачественные новобразования', u'3.2', u'D10-D36'),
    ( u'из них лейомиома матки', u'3.2.1', u'D25'),
    ( u'болезни крови, кроветворных органов и отдельные нарушения, вовлекающие иммунный механизм', u'4.0', u'D50-D89'),
    ( u'из них: анемии', u'4.1', u'D50-D64'),
    ( u'из них апластические анемии', u'4.1.1', u'D60-D61'),
    ( u'нарушения свертываемости крови, пурпуа и другие гемморагические состояния', u'4.2', u'D65-D69'),
    ( u'из них: диссеминированное внутрисосудистое свертывание крови (синдром дефибринации)', u'4.2.1', u'D66-D68'),
    ( u'отдельные нарушения, вовлекающие иммунный механизм', u'4.3', u'D80-D89'),
    ( u'болезни эндокринной системы, расстройства питания и нарушения обмена веществ', u'5.0', u'E00-E89'),
    ( u'из них: болезни щитовидной железы', u'5.1', u'E00-E07'),
    ( u'из них: синдром врожденной йодной недостаточности', u'5.1.1', u'E00'),
    ( u'эндемический зоб, связанный с йодной недостаточностью', u'5.1.2', u'E01.0-2'),
    ( u'субклинический гипотиреоз вследствие йодной недостаточности и другие формы гипотиреоза', u'5.1.3', u'E02, E03'),
    ( u'другие формы нетоксического зоба', u'5.1.4', u'E04'),
    ( u'тиреотоксикоз (гипертиреоз)', u'5.1.5', u'E05'),
    ( u'тиреоидит', u'5.1.3', u'E06'),
    ( u'сахарный диабет', u'5.2', u'E10-E14'),
    ( u'из него с поражением глаз', u'5.2.1', u'E10.3, E11.3, E12.3, E13.3, E14.3'),
    ( u'из него (из стр. 5.2):сахарный диабет I типа', u'5.2.2', u'E10'),
    ( u'сахарный диабет II типа', u'5.2.3', u'E11'),
    ( u'гиперфункция гипофиза', u'5.3', u'E22'),
    ( u'гипопитуитаризм', u'5.4', u'E23.0'),
    ( u'несахарный диабет', u'5.5', u'E23.2'),
    ( u'адреногенитальные расстройства', u'5.6', u'E25'),
    ( u'дисфункция яичников', u'5.7', u'E28'),
    ( u'дисфункция яичек', u'5.8', u'E29'),
    ( u'ожирение', u'5.9', u'E66'),
    ( u'фенилкетонурия', u'5.10', u'E70.0'),
    ( u'нарушения обмена галактозы (галактоземия)', u'5.11', u'E74.2'),
    ( u'болезнь Гоше', u'5.12', u'E75.2'),
    ( u'нарушения обмена гликозамигликанов (мукополисахаридоз)', u'5.13', u'E76'),
    ( u'муковисцидоз', u'5.14', u'E84'),
    ( u'психические расстройства и расстройства поведения', u'6.0', u'F01, F03-F99'),
    ( u'из них: психические расстройства и расстройства поведения, связанные с употреблением психоактивных веществ', u'6.1', u'F10-F19'),
    ( u'психические расстройства не связанные с употреблением психоактивных веществ, за исключением расстройств, классифицированных в других рубриках МКБ-10 (код со знаком *)', u'6.2', u'F01, F03-F09, F20-F99'),
    ( u'из них: детский аутизм, атипичный аутизм, синдродезинтегративное расстройство детского возраста', u'6.2.1', u'F84.0-3'),
    ( u'болезни нервной системы', u'7.0', u'G00-G98'),
    ( u'из них: воспалительные болезни центральной нервной системы', u'7.1', u'G00-G09'),
    ( u'из них: бактериальный менингит', u'7.1.1', u'G00'),
    ( u'из них: энцефалит, миелит и энцефаломиелит', u'7.1.2', u'G04'),
    ( u'системные атрофии, поражающие преимущественно нервную систему', u'7.2', u'G10-G12'),
    ( u'экстрапирамидные и другие двигательные нарушения', u'7.3', u'G20, G21, G23-G25'),
    ( u'другие экстрапирамидные и двигательные нарушения', u'7.3.2', u'G25'),
    ( u'другие дегенеративные болезни нервной системы', u'7.4', u'G30-G31'),
    ( u'демиелинизирующие болезни центральной нервной системы', u'7.5', u'G35-G37'),
    ( u'из них: рассеянный склероз', u'7.5.1', u'G35'),
    ( u'эпизодические и пароксизмальные расстройства', u'7.6', u'G40-G47'),
    ( u'из них: эпилепсия, эпилептический статус', u'7.6.1', u'G40-G41'),
    ( u'преходящие транзиторные церебральные ишемические приступы (атаки) и родственные синдромы', u'7.6.2', u'G45'),
    ( u'поражения отдельных нервов, нервных корешков и сплетений, полиневропатии и другие поражения периферической нервной  системы', u'7.7', u'G50-G64'),
    ( u'из них: синдром Гийена-Барре', u'7.7.1', u'G61.0'),
    ( u'болезни нервно-мышечного синапса и мышц', u'7.8', u'G70-G73'),
    ( u'из них: миастения ', u'7.8.1', u'G70.0, 2'),
    ( u'мышечная дистрофия Дюшенна', u'7.8.2', u'G71.0'),
    ( u'церебральный паралич и другие паралитические синдромы', u'7.9', u'G80-G83'),
    ( u'из них: церебральный паралич', u'7.9.1', u'G80'),
    ( u'расстройства вегетативной(автономной) нервной системы', u'7.10', u'G90'),
    ( u'сосудистые миелопатии', u'7.11', u'G95.1'),
    ( u'болезни глаза и его придаточного аппарата', u'8.0', u'H00-H59'),
    ( u'из них: конъюнктивит', u'8.1', u'H10'),
    ( u'кератит', u'8.2', u'H16'),
    ( u'из них язва роговицы', u'8.2.1', u'H16.0'),
    ( u'катаракта', u'8.3', u'H25-H26'),
    ( u'хориоретинальное воспаление', u'8.4', u'H30'),
    ( u'отслойка сетчатки с разрывом сетчатки', u'8.5', u'H33.0'),
    ( u'преретинопатия', u'8.6', u'H35.1'),
    ( u'дегенерация макулы и заднего полюса', u'8.7', u'H35.3'),
    ( u'глаукома', u'8.8', u'H40'),
    ( u'дегенеративная миопия', u'8.9', u'H46'),
    ( u'болезни зрительного нерва и зрительных путей', u'8.10', u'H46-H48'),
    ( u'атрофия зрительного нерва', u'8.10.1', u'H47.2'),
    ( u'болезни мышц глаза, нарушения содружественного движения глаз, аккомодации и рефракции', u'8.11', u'H49-H52'),
    ( u'из них миопия', u'8.11.1', u'H52.1'),
    ( u'астигматизм', u'8.11.2', u'H52.2'),
    ( u'слепота и пониженное зрение', u'8.12', u'H54'),
    ( u'из них: слепота обоих глаз', u'8.12.1', u'H54.0'),
    ( u'болезни уха и сосцевидного отростка', u'9.0', u'H60-H95'),
    ( u'из них: болезни наружного уха', u'9.1', u'H60-H62'),
    ( u'болезни среднего уха и сосцевидного отростка', u'9.2', u'H65-H66, H68-H74'),
    ( u'из них: острый средний отит', u'9.2.1', u'H65.0, H65.1, H66.0'),
    ( u'хронический средний отит', u'9.2.2', u'H65.2-4, H66.1-3'),
    ( u'болезни слуховой (евстахиевой) трубы', u'9.2.3', u'H68-H69'),
    ( u'перфорация барабанной перепонки', u'9.2.4', u'H72'),
    ( u'другие болезни среднего уха и сосцевидного отростка', u'9.2.5', u'H74'),
    ( u'болезни внутреннего уха', u'9.3', u'H80-H81, H83'),
    ( u'из них: отосклероз', u'9.3.1', u'H80'),
    ( u'болезнь Меньера', u'9.3.2', u'H81.0'),
    ( u'кондуктивная и нейросенсорная потеря слуха', u'9.4', u'H90'),
    ( u'из них: кондуктивная потеря слуха двусторонняя', u'9.4.1', u'H90.0'),
    ( u'нейросенсорная потеря слуха двусторонняя', u'9.4.2', u'H90.3'),
    ( u'болезни системы кровообращения', u'10.0', u'I00-I99'),
    ( u'из них: острая ревматическая лихорадка', u'10.1', u'I00-I02'),
    ( u'хронические ревматические болезни сердца', u'10.2', u'I05-I09'),
    ( u'из них: ревматические поражения клапанов', u'10.2.1', u'I05-I08'),
    ( u'болезни, характеризующиеся повышенным кровяным давлением', u'10.3', u'I10-I13'),
    ( u'из них: эссенциальная гипертензия', u'10.3.1', u'I10'),
    ( u'гипертензивная болезнь сердца (гипертоническая болезнь с преимущественным поражением сердца)', u'10.3.2', u'I11'),
    ( u'гипертензивная (гипертоническая) болезнь с преимущественным поражением почек с почечной недостаточностью', u'10.3.3', u'I12'),
    ( u'гипертензивная (гипертоническая) болезнь с преимущественным поражением сердца и почек', u'10.3.4', u'I13'),
    ( u'ишемические болезни сердца', u'10.4', u'I20-I25'),
    ( u'из них: стенокардия', u'10.4.1', u'I20'),
    ( u'из нее: нестабильная стенокардия', u'10.4.1.1', u'I20.0'),
    ( u'острый инфаркт миокарда', u'10.4.2', u'I21'),
    ( u'повторный инфаркт миокарда', u'10.4.3', u'I22'),
    ( u'другие формы острой ишемической болезни сердца', u'10.4.4', u'I24'),
    ( u'хроническая ишемическая болезнь сердца', u'10.4.5', u'I25'),
    ( u'из нее постинфарктный кардиосклероз', u'10.4.5.1', u'I25.8'),
    ( u'легочная эмболия', u'10.5', u'I30-I51'),
    ( u'из них: острый перикардит', u'10.5.1', u'I30'),
    ( u'из них: острый и подострый эндокардит', u'10.5.2', u'I33'),
    ( u'острый миокардит', u'10.5.3', u'I40'),
    ( u'кардиомиопатия', u'10.5.4', u'I42'),
    ( u'цереброваскулярные болезни', u'10.6', u'I60-I69'),
    ( u'из них: субарахноидальное кровоизлияние', u'10.6.1', u'I60'),
    ( u'внутримозговое и другое внутречерепное кровоизлияние', u'10.6.2', u'I61, I62'),
    ( u'инфаркт мозга', u'10.6.3', u'I63'),
    ( u'инсульт, не уточненный как кровоизлияние или инфаркт (инсульт церебральный)', u'10.6.4', u'I64'),
    ( u'закупорка и стеноз прецеребральных, церебральных артерий, не приводящие к инфаркту мозга ', u'10.6.5', u'I65- I66'),
    ( u'другие цереброваскулярные болезни', u'10.6.6', u'I67'),
    ( u'последствия церереброваскулярных болезней', u'10.6.7', u'I69'),
    ( u'эндартериит, тромбангиит облитерирующий', u'10.7', u' I70.2, I73.1'),
    ( u'болезни вен, лимфатических сосудов и лимфатических узлов', u'10.8', u'I80-I83, I85-I89'),
    ( u'из них: флебит и тромбофлебит', u'10.8.1', u'I80'),
    ( u'тромбоз портальной вены', u'10.8.2', u'I81'),
    ( u'варикозное расширение вен нижних конечностей', u'10.8.3', u'I83'),
    ( u'болезни органов дыхания', u'11.0', u'J00-J98'),
    ( u'из них: острые респираторные инфекции верхних дыхательных путей', u'11.1', u'J00-J06'),
    ( u'из них: острый ларингит и трахеит', u'11.1.1', u'J04'),
    ( u'острый обструктивный ларингит (круп) и эпиглоттит', u'11.1.2', u'J05'),
    ( u'грипп', u'11.2', u'J09-J11'),
    ( u'пневмония', u'11.3', u'J12-J16, J18'),
    ( u'острые респираторные инфекции нижних дыхательных путей', u'11.4', u'J20-J22'),
    ( u'аллергический ринит (поллиноз)', u'11.5', u'J30.1'),
    ( u'хронические болезни миндалин и аденоидов, перитонзиллярный абсцесс', u'11.6', u'J35-J36'),
    ( u'бронхит хронический и неуточненный, эмфизема', u'11.7', u'J40-J43'),
    ( u'другая хроническая обструктивная легочная болезнь ', u'11.8', u'J44'),
    ( u'бронхоэктатическая болезнь', u'11.9', u'J47'),
    ( u'астма, астматический статус', u'11.10', u'J45, J46'),
    ( u'другие интерстициальные легочные болезни, гнойные и некротические состояния нижних дыхательных путей, другие болезни плевры', u'11.11', u'J84-J90, J92-J94'),
    ( u'болезни органов пищеварения', u'12.0', u'K00-K92'),
    ( u'из них: язвенная болезнь желудка и 12-ти перстной кишки', u'12.1', u'K25-K26'),
    ( u'гастрит и дуоденит', u'12.2', u'K29'),
    ( u'грыжи', u'12.3', u'K40-K46'),
    ( u'неинфекционный энтерит и колит', u'12.4', u'K50-K52'),
    ( u'из них болезнь Крона', u'12.4.1', u'K50'),
    ( u'Язвенный колит', u'12.4.2', u'K51'),
    ( u'другие болезни кишечника', u'12.5', u'K55-K63'),
    ( u'из них: паралитический илеус и непроходимость кишечника без грыжи', u'12.5.1', u'K56'),
    ( u'геморрой', u'12.6', u'K64'),
    ( u'болезни печени', u'12.7', u'K70-K76'),
    ( u'из них: фиброз и цирроз печени', u'12.7.1', u'K74'),
    ( u'болезни желчного пузыря, желчевыводящих путей', u'12.8', u'K80-K83'),
    ( u'болезни поджелудочной железы', u'12.9', u'K85-K86'),
    ( u'из них: острый панкреатит', u'12.9.1', u'K85'),
    ( u'болезни кожи и подкожной клетчатки', u'13.0', u'L00-L98'),
    ( u'атопический дерматит', u'13.1', u'L20'),
    ( u'контактный дерматит', u'13.2', u'L23-L25'),
    ( u'другие дерматиты (экзема)', u'13.3', u'L30'),
    ( u'псориаз', u'13.4', u'L40'),
    ( u'из него: псориаз артропатический', u'13.4.1', u'L40.5'),
    ( u'дискоидная красная волчанка', u'13.5', u'L93.0'),
    ( u'локализованная склеродермия', u'13.6', u'L94.0'),
    ( u'болезни костно-мышечной системы и соединительной ткани', u'14.0', u'M00-M99'),
    ( u'из них: артропатии', u'14.1', u'M00-M25'),
    ( u'из них: реактивные артропатии', u'14.1.1', u'M02'),
    ( u'серопозитивный и серонегативный артриты', u'14.1.2', u'M05, M06'),
    ( u'артрозы', u'14.1.4', u'M15-M19'),
    ( u'системные поражения соединительной ткани', u'14.2', u'M30-M35'),
    ( u'из них: системная красная волчанка', u'14.2.1', u'M32'),
    ( u'деформирующие дорсопатии', u'14.3', u'M40-M43'),
    ( u'спондилопатии', u'14.4', u'M45-M48'),
    ( u'из них: анкилозирующий спондилит', u'14.4.1', u'M45'),
    ( u'поражения синовиальных оболочек и сухожилий', u'14.5', u'M65-M67'),
    ( u'остеопатии и хондропатии', u'14.6', u'M80-M94'),
    ( u'из них остеопороз с патологическим переломом', u'14.6.1', u'M80'),
    ( u'остеопороз без патологического перелома', u'14.6.2', u'M81'),
    ( u'болезни мочеполовой системы', u'15.0', u'N00-N99'),
    ( u'из них: гломерулярные, тубулоинтерстициальные болезни почек, другие болезни почки и мочеточника', u'15.1', u'N00-N07, N09-N15, N25-N28'),
    ( u'почечная недостаточность', u'15.2', u'N17-N19'),
    ( u'мочекаменная болезнь', u'15.3', u'N20-N21, N23'),
    ( u'другие болезни мочевой системы', u'15.4', u'N30-N32, N34-N36, N39'),
    ( u'болезни предстательной железы', u'15.5', u'N40-N42'),
    ( u'мужское бесплодие', u'15.6', u'N46'),
    ( u'доброкачественная дисплазия молочной железы', u'15.7', u'N60'),
    ( u'воспалительные болезни женских тазовых органов', u'15.8', u'N70-N73, N75-N76'),
    ( u'из них сальпингит и оофорит', u'15.8.1', u'N70'),
    ( u'эндометриоз', u'15.9', u'N80'),
    ( u'эрозия и эктропион шейки матки', u'15.10', u'N86'),
    ( u'расстройства менструаций', u'15.11', u'N91 - N94'),
    ( u'женское бесплодие', u'15.12', u'N97'),
    ( u'беременность, роды и послеродовой период', u'16.0', u'O00-O99'),
    ( u'отдельные состояния, возникающие в перинатальном периоде', u'17.0', u'P00-P04'),
    ( u'врожденные аномалии (пороки развития), деформации и хромосомные нарушения', u'18.0', u'Q00-Q99'),
    ( u'из них: врожденные аномалии нервной системы', u'18.1', u'Q00-Q07'),
    ( u'врожденные аномалии глаза', u'18.2', u'Q10-Q15'),
    ( u'врожденные аномалии системы кровообращения', u'18.3', u'Q20-Q28'),
    ( u'врожденные аномалии женских половых органов', u'18.4', u'Q50-Q52'),
    ( u'неопределенность пола и псевдогермафродитизм', u'18.5', u'Q56'),
    ( u'врожденные деформации бедра ', u'18.6', u'Q65'),
    ( u'врожденный ихтиоз', u'18.7', u'Q80'),
    ( u'нейрофиброматоз', u'18.8', u'Q85.0'),
    ( u'синдром Дауна', u'18.9', u'Q90'),
    ( u'симптомы, признаки и отклонения от нормы, выявленные при клинических и лабораторных исследованиях, не классифицированные в других рубриках', u'19.0', u'R00-R99'),
    ( u'травмы, отравления и некоторые другие последствия воздействия внешних причин', u'20.0', u'S00-T98'),
    ( u'из них: открытые укушенные раны (только с кодом внешней причины W54)', u'20.1', u'S01, S11, S21, S31, S41, S51, S61, S71, S81, S91'),
    ( u'COVID-19', u'21.0', u'U07.1, U07.2')
]

CompRows = [
    ( u'Всего', u'1.0', u'Z00-Z99'),
    ( u'из них: обращения в медицинские организации для медицинского осмотра и обследования', u'1.1', u'Z00-Z13'),
    ( u'из них: обращения в связи с получением медицинских документов', u'1.1.1', u'Z02.7'),
    ( u'наблюдение при подозрении на COVID-19', u'1.1.2', u'Z03.8'),
    ( u'скрининговое обследование с целью выявления COVID-19', u'1.1.3', u'Z11.5'),
    ( u'потенциальная опасность для здоровья, связанная с инфекционными болезнями', u'1.2', u'Z20-Z29'),
    ( u'из них: контакт с больным COVID-19', u'1.2.1', u'Z20.8'),
    ( u'из них: носительство возбудителя инфекционной болезни', u'1.2.2', u'Z22'),
    ( u'из них: носительство возбудителя COVID-19', u'1.2.3', u'Z22.8'),
    ( u'обращения в медицинские организации в связи с обстоятельствами, относящимися к репродуктивной функции', u'1.3', u'Z30-Z39'),
    ( u'обращения в медицинские организации в связи с необходимостью проведения специфических процедур и получения медицинской помощи', u'1.4', u'Z40-Z54'),
    ( u'из них: помощь, включающая использование реабилитационных процедур', u'1.4.1', u'Z50'),
    ( u'из них: реабилитация лиц, страдающих алкоголизмом', u'1.4.1.1', u'Z50.2'),
    ( u'реабилитация лиц, страдающих наркоманиями', u'1.4.1.2', u'Z50.3'),
    ( u'лечение, включающее другие виды реабилитационных процедур, реабилитация при курении', u'1.4.1.3', u'Z50.8'),
    ( u'паллиативная помощь', u'1.4.2', u'Z51.5'),
    ( u'потенциальная опасность для здоровья, связанная с социально-экономическими и психосоциальными обстоятельствами', u'1.5', u'Z55-Z65'),
    ( u'обращения в медицинские организации в связи с другими обстоятельствами', u'1.6', u'Z70-Z76'),
    ( u'из них: обращения в учреждения здравоохранения для получения других консультаций и медицинских советов, не классифицированные в других рубриках', u'1.6.1', u'Z71'),
    ( u'консультирование и наблюдение по поводу алкоголизма', u'1.6.1.1', u'Z71.4'),
    ( u'консультирование и наблюдение по поводу наркомании', u'1.6.1.2', u'Z71.5'),
    ( u'консультирование и наблюдение по поводу курения', u'1.6.1.3', u'Z71.6'),
    ( u'из них: проблемы, связанные с образом жизни:', u'1.6.2', u'Z72'),
    ( u'из них: употребление табака', u'1.6.2.1', u'Z72.0'),
    ( u'употребление алкоголя', u'1.6.2.2', u'Z72.1'),
    ( u'использование наркотиков', u'1.6.2.3', u'Z72.2'),
    ( u'склонность к азартным играм и пари', u'1.6.2.4', u'Z72.6'),
    ( u'потенциальная опасность для здоровья, связанная с личным или семейным анамнезом и определенными обстоятельствами, влияющими на здоровье', u'1.7', u'Z80-Z99'),
    ( u'из них: заболевания в семейном анамнезе', u'1.7.1', u'Z80-Z84'),
    ( u'из них: наличие илеостомы, колостомы', u'1.7.1', u'Z93.2, Z93.3')
]

class CStatReportF12Able_2022(CStatReportF12Able_2021):
    def build(self, params):
        return CStatReportF12Able_2021.build(self, params, MainRows, CompRows)
