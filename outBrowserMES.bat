

rem set freezer=FreezePython.exe
set freezer=call "c:\Python27\Scripts\cxfreeze.bat"
set main=appendix\mes\main.py 
#set base=--base-name=customWin32GUI.exe
#set base=--base-name=Console.exe
set base=--base-name=Console
set outdir=--target-dir=out
set outexe=--target-name=browserMES.exe
set includepath=--include-path=.
# set includemods=--include-modules=sip,traceback
set includemods=--include-modules=sip,atexit,traceback,codecs,encodings,encodings.aliases,encodings.ascii,encodings.cp1251,encodings.cp866,encodings.utf_8,encodings.mbcs
set excludemods=--exclude-modules=_LWPCookieJar,_MozillaCookieJar
set icon=--icon=icons\Icon2.ico 
rem set copydeps=--no-copy-deps
rem set includefiles=--zip-include=i18n\std_ru.qm
set compress=--compress
%freezer% %base% %outdir% %outexe% %includepath% %includemods% %excludemods% %includefiles% %main% %icon% %copydeps% %compress%

