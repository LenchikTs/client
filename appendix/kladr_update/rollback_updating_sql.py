#!/usr/bin/env python
# -*- coding: utf-8 -*-
COMMAND = u"""
select 'Восстановление старой версии КЛАДР...' as ' ';

delete from kladr.KLADR where 1;
insert kladr.KLADR select * from kladr.cpKLADR;

delete from kladr.STREET where 1;
insert kladr.STREET select * from kladr.cpSTREET;

delete from kladr.DOMA where 1;
insert kladr.DOMA select * from kladr.cpDOMA;

delete from kladr.FLAT where 1;
insert kladr.FLAT select * from kladr.cpFLAT;

delete from kladr.ALTNAMES where 1;
insert kladr.ALTNAMES select * from kladr.cpALTNAMES;

delete from kladr.SOCRBASE where 1;
insert kladr.SOCRBASE select * from kladr.cpSOCRBASE;

delete from kladr.infisAREA where 1;
insert kladr.infisAREA select * from kladr.cp_infisAREA;

delete from kladr.infisREGION where 1;
insert kladr.infisREGION select * from kladr.cp_infisREGION;

delete from kladr.infisSTREET where 1;
insert kladr.infisSTREET select * from kladr.cp_infisSTREET;

-- drop table s11.AddressHouse;
-- create table s11.AddressHouse like kladr_copy.AddressHouse;
-- insert s11.AddressHouse select * from kladr_copy.AddressHouse;

select 'Восстановление завершено!' as ' ';"""
