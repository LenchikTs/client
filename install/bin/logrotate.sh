#!/bin/bash
yesterday=`date '+%Y-%m-%d' -d "yesterday"` # вчерашняя дата

echo "Очистка старых логов" 

# AriadnaExchange
find /var/log/AriadnaExchange/ -type f -mtime +7 -exec gzip {} \;
find /var/log/AriadnaExchange/ -type f -mtime +60 -exec rm {} \;

# ODIIExchange
find /var/log/ODIIExchange/ -type f -mtime +0 -exec gzip {} \;
find /var/log/ODIIExchange/ -type f -mtime +6 -exec rm {} \;

# downloadRecipeLLO
find /var/log/downloadRecipeLLO/ -type f -mtime +7 -exec gzip {} \;
find /var/log/downloadRecipeLLO/ -type f -mtime +60 -exec rm {} \;

# WarrantNumberUpdater
mv /var/log/Warrant/WarrantNumberUpdater.log /var/log/Warrant/WarrantNumberUpdater_$yesterday.log
find /var/log/Warrant/ -type f -mtime +7 -exec gzip {} \;
find /var/log/Warrant/ -type f -mtime +60 -exec rm {} \;
		
# Holter
find /var/log/Holter/ -type f -mtime +7 -exec gzip {} \;
find /var/log/Holter/ -type f -mtime +60 -exec rm {} \;
		
