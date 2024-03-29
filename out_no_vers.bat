rem set freezer=FreezePython.exe
set freezer=call "c:\Python27\Scripts\cxfreeze.bat"

set main=s11main.py
rem set base=--base-name=customWin32GUI.exe
set base=--base-name=Win32GUI
set outdir=--target-dir=out
set outexe=--target-name=samson.exe
set includepath=--include-path=.
set includemods=--include-modules=sip,traceback,codecs,encodings,encodings.aliases,encodings.ascii,encodings.cp1251,encodings.cp866,encodings.koi8_r,encodings.utf_8,encodings.mbcs,encodings.idna,encodings.utf_16_be,datetime,time,_strptime,email.iterators,email.generator
set excludemods=--exclude-modules=_LWPCookieJar,_MozillaCookieJar,pydoc,doctest,collections._weakref,collections.sys

set icon=--icon=icons\Icon2.ico 
rem set copydeps=--no-copy-deps
rem set includefiles=--zip-include=i18n\std_ru.qm, i18n\qt_ru_lib.qm
set compress=--compress
%freezer% %base% %outdir% %outexe% %includepath% %includemods% %excludemods% %includefiles% %main% %icon% %copydeps% %compress%


set base=--base-name=Console
set outexe=--target-name=samson-console.exe
%freezer% %base% %outdir% %outexe% %includepath% %includemods% %excludemods% %includefiles% %main% %icon% %copydeps% %compress%

rem set main=s11util.py
rem set base=--base-name=customWin32GUI.exe
rem set outexe=--target-name=s11util.exe
rem FreezePython.exe %base% %outdir% %outexe% %includepath% %includemods% %includefiles% %main%