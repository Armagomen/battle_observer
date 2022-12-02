@Echo off
set ModVersion=1.40.08
set GameVersion=1.19.0.1
set GameInstalled_ModsDir=C:\Games\World_of_Tanks_EU\mods

REM set GameVersion="1.18.1.0 Common Test"
REM set GameInstalled_ModsDir=C:\Games\World_of_Tanks_CT\mods

"python.exe" bo_compile_all.py -f -q -d scripts mod\res\scripts

set ModFile=..\output_data\mods\%GameVersion%\armagomen.battleObserver_%ModVersion%.wotmod
set ZipArh=..\BattleObserver_WOT_EU.zip
set AutoUpdate=..\AutoUpdate.zip

DEL ..\output_data\mods\%GameVersion%\armagomen.battleObserver*
DEL %GameInstalled_ModsDir%\%GameVersion%\armagomen.battleObserver*
DEL %ZipArh%
DEL %AutoUpdate%

"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx0 -x!*.py -x!*.cmd %ModFile% .\mod\*
"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %ZipArh% ..\output_data\*
"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %AutoUpdate% %ModFile%

Xcopy ..\output_data\mods %GameInstalled_ModsDir% /e /i /d

DEL /s /q *.pyc
exit