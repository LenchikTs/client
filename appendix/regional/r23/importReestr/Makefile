PY_STRING_BEGIN = "\#!/usr/bin/env python\n\# -*- coding: utf-8 -*-\n\nCOMMAND = u\"\"\"\n"
PY_STRING_END = "\"\"\""

all: create_sql.py import_sql.py

%_sql.py: %.sql
	echo $(PY_STRING_BEGIN) > $@
	cat $< >> $@
	echo $(PY_STRING_END) >> $@