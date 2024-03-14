Внутренняя система отправки оповещений САМСОНа.
Отправляет оповещения, созданные в таблице БД Notificatoin_Log.

Необходимо настроить logrotate скопировав
cp ./notificationTool /etc/logrotate.d/
error.log и notificationTool.log должны быть созданы и находиться по адресу /home/notifier/.samson-vista/
