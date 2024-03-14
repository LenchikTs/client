#!/bin/bash
#echo '11' | sudo -S sudo yum list qtsoap* ;
echo --------$(date +%Y%m%d-%T) Start Dopinstall.sh--------
DIR=/opt/client/install

#uname -a > LinuxVersion
#if grep "redos.client 4.19" LinuxVersion ; then 
#	echo "====РЕД ОС====" 	
#	pip install $DIR/RedOS/suds-0.4.tar.gz
#fi
#
#if grep "depo 4.9" LinuxVersion ; then 
#	echo "====Дебиан====" 
#fi
#
## Установка pyxb для работы клиента

#Проверка на РЕД ОС 7.3.2
#if grep 7.3.2 /etc/os-release
#	pip install $DIR/RedOS/suds-0.4.tar.gz
#fi

## Подходит для всех ОС
#pip2 list --format=legacy > $DIR/pip2.list || exit 601  #не работает на 7,3,1
pip2 list > $DIR/pip2.list || exit 601

if ! grep "PyXB" $DIR/pip2.list ; then 
	pip2 install $DIR/PyXB-1.2.6.tar.gz || exit 601
fi

if ! grep "numpy" $DIR/pip2.list ; then 
	pip2 install $DIR/numpy-1.16.6-cp27-cp27mu-manylinux1_x86_64.whl || exit 601
fi

if ! grep "Pillow" $DIR/pip2.list ; then 
	pip2 install $DIR/Pillow-6.2.2-cp27-cp27mu-manylinux1_x86_64.whl || exit 601
fi

if ! grep "scipy" $DIR/pip2.list ; then 
	pip2 install $DIR/scipy-1.2.3-cp27-cp27mu-manylinux1_x86_64.whl || exit 601
fi

if ! grep "pyBarcode" $DIR/pip2.list ; then 
	pip2 install $DIR/pyBarcode-0.8b1-cp27-none-any.whl || exit 601
fi

# Установить шрифты
dirfonts=/usr/share/fonts

if [ ! -f $dirfonts/code39/code39.ttf ]; then
	echo "install fonts code39 and Code128..."
	mkdir -p $dirfonts/code39
	cp $DIR/code39/code39.ttf   $dirfonts/code39/
	mkdir -p $dirfonts/Code128
	cp $DIR/Code128/Code128.ttf  $dirfonts/Code128/
fi

if [ ! -f $dirfonts/pt-root/pt-root-ui_regular.ttf ]; then
	echo "install fonts pt-root..."
	mkdir -p $dirfonts/pt-root
	cp $DIR/pt-root/*.ttf $dirfonts/pt-root/
fi

# Чиним проверку орфографии
cat /etc/os-release > LinuxVersion
if grep "RED OS" LinuxVersion ; then 
	echo "====РЕД ОС====" 
	echo "Чиним проверку орфографии"	
	rm -f /usr/lib64/libhunspell.so
	ln -s /usr/lib64/libhunspell-1.7.so.0.0.1 /usr/lib64/libhunspell.so
fi


echo --------$(date +%Y%m%d-%T) End Dopinstall.sh--------






