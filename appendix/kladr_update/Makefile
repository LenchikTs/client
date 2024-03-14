PY_STRING_BEGIN1 = "\#!/usr/bin/env python"
PY_STRING_BEGIN2 = "\# -*- coding: utf-8 -*-"
PY_STRING_BEGIN3 = "COMMAND = u\"\"\""
PY_STRING_END = "\"\"\""

all: clear_sql.py create_kladr_sql.py create_okato_sql.py create_copy_sql.py rollback_updating_sql.py test_sql.py update_kladr_sql.py restore_parent_prefix_sql.py update_okato_sql.py update_s11_sql.py 

%_sql.py: %.sql
	echo $(PY_STRING_BEGIN1) > $@
	echo $(PY_STRING_BEGIN2) >> $@
	echo $(PY_STRING_BEGIN3) >> $@
	cat $< >> $@
	echo $(PY_STRING_END) >> $@