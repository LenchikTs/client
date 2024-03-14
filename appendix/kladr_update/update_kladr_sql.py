#!/usr/bin/env python
# -*- coding: utf-8 -*-
COMMAND = u"""
use kladr;

-- ALTNAMES
select 'Updating ALTNAMES...' as ' ';
optimize table ALTNAMES;

-- KLADR
select 'Updating KLADR... ' as ' ';
optimize table KLADR;

-- STREET
select 'Updating STREET... Please wait.' as ' ';
optimize table STREET;

-- DOMA
-- select 'Updating DOMA... Please wait.' as ' ';
-- optimize table DOMA;
-- UPDATE DOMA SET flatHouseList = unwindHouseSpecification(NAME);
-- optimize table FLAT;

-- SOCRBASE
select 'Updating SOCRBASE...' as ' ';

select 'Updating is successfull!' as ' ';"""
