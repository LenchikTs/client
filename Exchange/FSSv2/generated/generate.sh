#!/bin/bash
# Собственно генерация
wsdl2py -b ../wsdl/fixed/FileOperationsLnService.wsdl

# Запрет strip для TC.String
#
# Обнаружено, что ZSI при получении '<greeting>   hello!  </greeting>
# помещает в .Greeting 'hello!' а не '   hello!  '
# возможности изменить поведение параметрами парсера
# или изменением в wsdl/xsd не найдено.
#
# Joshua Boverhof по этому поводу писал (2009-11-21):
#       Sounds like a bug ( if you're using generated typecodes (wsdl2py) )
#       You can add the keyword argument to the string typecode:
#       String(...,strip=False)
#       to turn this behavior off.  Let me know if that fixes the problem.
# https://sourceforge.net/p/pywebsvcs/mailman/message/24023835/
#
# Joshua Boverhof получил подтверждение что всё ок, но
# вносить изменения в генерацию кода не стал.
#
# Поэтому исправляем вызов конструктора самостоятельно,
# для простоты рег.выражения добавляя параметр в начале -

sed -i -r -e 's/TC\.String\(/TC\.String\(strip=False, /g' *_types.py

# По моему мнению такое вот обрезание пробелов противоречит затеям XML
# и нужно только в редких случаях неаккуратной ручной подготовки примеров.
# Но как в 2001 году Rich Salz выпустил код с удалением пробелов,
# так и висит немного покачаваясь :(

echo -n >fssns.py
echo '###########################################' >> fssns.py
echo '#'                                           >> fssns.py
echo '# namespaces'                                >> fssns.py
echo '#'                                           >> fssns.py
echo '###########################################' >> fssns.py
echo ''                                            >> fssns.py

echo "FSSMO    = 'http://www.fss.ru/integration/types/eln/mo/v01'" >> fssns.py
echo "FSSELN   = 'http://www.fss.ru/integration/types/eln/v01'"    >> fssns.py
echo "FSSFAULT = 'http://www.fss.ru/integration/types/fault/v01'"  >> fssns.py
echo "fssNsDict = {'mo':FSSMO, 'eln':FSSELN, 'fault': FSSFAULT}"   >> fssns.py

sed -i -r -e 's!"http://www.fss.ru/integration/types/eln/mo/v01"!FSSMO!g'   FileOperationsLnService*.py
sed -i -r -e 's!"http://www.fss.ru/integration/types/eln/v01"!FSSELN!g'     FileOperationsLnService*.py
sed -i -r -e 's!"http://www.fss.ru/integration/types/fault/v01"!FSSFAULT!g' FileOperationsLnService*.py

sed -i -r -e '/from ZSI.generate.pyclass import pyclass_type/afrom fssns import FSSMO, FSSELN, FSSFAULT' FileOperationsLnService_types.py
sed -i -r -e '/from ZSI.generate.pyclass import pyclass_type/afrom fssns import FSSMO, FSSELN, FSSFAULT' FileOperationsLnService_client.py
sed -i -r -e '/from ZSI.ServiceContainer import ServiceSOAPBinding/afrom fssns import FSSMO, FSSELN, FSSFAULT' FileOperationsLnService_server.py

