select 'Backuping kladr...' as ' ';

drop table if exists kladr.cpKLADR ;
create table kladr.cpKLADR like kladr.KLADR;
insert kl dr.cpKLADR select * from kladr.KLADR;

drop table if exists kladr.cpSTREET;
create table kladr.cpSTREET like kladr.STREET;
insert kladr.cpSTREET select * from kladr.STREET;

drop table if exists kladr.cpDOMA;
create table kladr.cpDOMA like kladr.DOMA;
insert kladr.cpDOMA select * from kladr.DOMA;

drop table if exists kladr.cpFLAT;
create table kladr.cpFLAT like kladr.FLAT;
insert kladr.cpFLAT select * from kladr.FLAT;

drop table if exists kladr.cpALTNAMES;
create table kladr.cpALTNAMES like kladr.ALTNAMES;
insert kladr.cpALTNAMES select * from kladr.ALTNAMES;

drop table if exists kladr.cpSOCRBASE;
create table kladr.cpSOCRBASE like kladr.SOCRBASE;
insert kladr.cpSOCRBASE select * from kladr.SOCRBASE;

drop table if exists kladr.cpOKATO;
create table kladr.cpOKATO like kladr.OKATO;
insert kladr.cpOKATO select * from kladr.OKATO;

drop table if exists kladr.cp_infisAREA;
create table kladr.cp_infisAREA like kladr.infisAREA;
insert kladr.cp_infisAREA select * from kladr.infisAREA;

drop table if exists kladr.cp_infisREGION;
create table kladr.cp_infisREGION like kladr.infisREGION;
insert kladr.cp_infisREGION select * from kladr.infisREGION;

drop table if exists kladr.cp_infisSTREET;
create table kladr.cp_infisSTREET like kladr.infisSTREET;
insert kladr.cp_infisSTREET select * from kladr.infisSTREET;

-- drop table if exists kladr.cpAddressHouse;
-- create table kladr.cpAddressHouse like s11.AddressHouse;
-- insert kladr_copy.AddressHouse select * from s11.AddressHouse;
