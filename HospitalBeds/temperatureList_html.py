#!/usr/bin/env python
# -*- coding: utf-8 -*-

CONTENT = u"""

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
    
<html>
<head>
<!--Главный скрипт-->
{: clients = dict([])}
{for: event in events}
	{ clients.data.setdefault(event.bedCode, []).append(event)}
{end:}

{: client_num = 0}
{for: bed_name in clients.data}
	{: client_num += len(clients.data[bed_name])}
{end:}
{: rooms = clients.data.keys()}
{: rooms.sort()}
{: NUMSTR = 55}
{: num_pages = (len(events) + len(rooms)-2)/(NUMSTR*2) + 1}
{: finances = [u'Б', u'ОМС', u'ДМС', u'ПМУ', u'ВМП']}
<!--Конец главного скрипта-->

<meta name="qrichtext" content="1" />
</head>
<body style=" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;">
<center>Присутствующие на отделении {orgStructure} (температурный лист) на {currentDate} {client_num} пациентов на отделении.</center>

{for: current_page in xrange(num_pages)}
{if: current_page > 0}

<!--НОВАЯ СТРАНИЦА-->
<p style="page-break-after: always"><font color=#FFFFFF>.</font></p>
{end:}


<table cellpadding=0 cellspacing=0 width=100% border="1">
<tr><td width=50%>
<table width=100% border=1>
<tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td></tr>
<tr><td>И</td><td>Др. город</td><td>ФИО</td><td>утро</td><td>вечер</td><td>питание</td></tr>
{: current_number = 0}
{for: bed_name in rooms}
{if: len(bed_name)}
{if: current_number >=  NUMSTR*2*current_page and current_number < NUMSTR*2*current_page + NUMSTR}
<tr><td colspan=5 align=center><b>{bed_name}</b></td></tr>
{end:}
{: current_number = current_number + 1}
{end:}
{for: event in clients.data[bed_name]}
{if: current_number >=  NUMSTR*2*current_page and current_number <  NUMSTR*2*current_page + NUMSTR}
<tr>
<!--источник финансирования -->
{if: event.finance != u'целевой'}
<td>{event.finance}</td>
{else:}
<td>{u'ВМП' if event.action[u"Квота"].value.type.class_ == 0 else u'СМП'}</td>
{end:}
<!-- местный/неместный -->
{if: event.client.locAddress.KLADRCode[:2] == '78'}
<td></td> 
{else:}
<td>+<!--{event.client.locAddress.city[:24]} --></td>
{end:}
<!--ФИО-->
<td>{event.client.shortName}</td>
<!--утро и вечер не заполняем -->
<td></td><td></td>
<!--питание -->
<td>{event.feed}</td>
</tr>
{end:}
{: current_number = current_number + 1}
{end:}
{end:}
</table></td>

<td width=50%><table width=100% border=1>
<tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td></tr>
<tr><td>И</td><td>Др. город</td><td>ФИО</td><td>утро</td><td>вечер</td><td>питание</td></tr>
{: current_number = 0}
{for: bed_name in rooms}
{if: len(bed_name)}
{if: current_number >= NUMSTR*2*current_page + NUMSTR and current_number < NUMSTR*2*current_page + NUMSTR*2}
<tr><td colspan=5 align=center><b>{bed_name}</b></td></tr>
{end:}
{: current_number = current_number + 1}
{end:}
{for: event in clients.data[bed_name]}
{if: current_number >=  NUMSTR*2*current_page + NUMSTR and current_number <  NUMSTR*2*current_page + NUMSTR*2}
<tr>
<!--источник финансирования -->
{if: event.finance != u'целевой'}
<td>{event.finance}</td>
{else:}
<td>{u'ВМП' if event.action[u"Квота"].value.type.class_ == 0 else u'СМП'}</td>
{end:}
<!-- местный/неместный -->
{if: event.client.locAddress.KLADRCode[:2] == '78'}
<td></td> 
{else:}
<td> + <!--{event.client.locAddress.city[:24]} --></td>
{end:}
<!--ФИО-->
<td>{event.client.shortName}</td>
<!--утро и вечер не заполняем -->
<td></td><td></td>
<!--питание -->
<td>{event.feed}</td>
</tr>
{end:}
{: current_number = current_number + 1}
{end:}
{end:}
</table></td>
</tr></table>
{end:}
</body>
</html>"""
