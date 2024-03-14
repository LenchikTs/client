-- восстанавливаем parent и prefix:
-- delimiter //
-- drop function if exists getParent//
-- create function getParent(aCode varchar(13))
-- returns varchar(13)
-- language SQL
-- deterministic
-- comment 'Get parent code from KLADR code'
-- begin
--     declare length int default 11;
--     declare parent_code varchar(11);
--     
--     if left(aCode, 2) = '00' then -- это военная часть
-- 	return '001';
--     end if;
--     -- обрезаем код пункта:
--     if substr(aCode from 9 for 3) != '000' then
-- 	set length = 8;
--     elseif substr(aCode from 6 for 3) != '000' then
-- 	set length = 5;
--     elseif substr(aCode from 3 for 3) != '000' then
-- 	set length = 2;
--     else
-- 	return '';
--     end if;
--     set parent_code = insert('00000000000', 1, length, left(aCode, length));
--     -- обрезаем лишние нули:
--     if substr(parent_code from 6 for 3) != '000' then
-- 	set length = 8;
--     elseif substr(parent_code from 3 for 3) != '000' then
-- 	set length = 5;
--     elseif substr(parent_code from 1 for 2) != '00' then
-- 	set length = 3;
--     else
-- 	set length = 0;
--     end if;
--     set parent_code = left(parent_code, length);
    
--     return parent_code;
-- end;
-- //
-- delimiter ;

-- update KLADR set parent = getParent(CODE);
-- update KLADR set prefix = if(substr(CODE from 9 for 3) != '000', '8', if(substr(CODE from 6 for 3) != '000', '5', if(substr(CODE from 3 for 3) != '000', '2', '0'))); -- временно сохраняем длину в поле prefix
-- update KLADR set `parent` = if(left(CODE, 2) = '00', '001', insert('00000000000', 1, prefix, left(CODE, prefix)));
-- update KLADR set prefix = if(substr(`parent` from 6 for 3) != '000', '8', if(substr(`parent` from 3 for 3) != '000', '5', if(substr(`parent` from 1 for 2) != '00', '3', '0')));
-- update KLADR set `parent` = if(`parent` != '001', left(`parent`, prefix), '001');

UPDATE KLADR
SET parent = SUBSTR(CODE, 1,
CASE
WHEN CODE LIKE '0010000000000' THEN 0
WHEN CODE LIKE '001%' THEN 3
WHEN CODE LIKE '__000000000__' THEN 0
WHEN CODE LIKE '_____000000__' THEN 3
WHEN CODE LIKE '__000___000__' THEN 3
WHEN CODE LIKE '__000000_____' THEN 3
WHEN CODE LIKE '________000__' THEN 5
WHEN CODE LIKE '_____000_____' THEN 5
WHEN CODE LIKE '_____________' THEN 8
ELSE 0
END );

update KLADR set prefix = left(CODE, 2);
