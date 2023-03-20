@Echo off
set ModVersion=1.40.31
set GameVersion=1.20.0.1
set GameInstalled_ModsDir=C:\Games\World_of_Tanks_EU\mods\%GameVersion%
set OutputDir=..\output_data\mods\%GameVersion%

REM set GameVersion="1.18.1.0 Common Test"
REM set GameInstalled_ModsDir=C:\Games\World_of_Tanks_CT\mods

"python.exe" bo_compile_all.py -f -q -d scripts mod\res\scripts

set ModFile=%OutputDir%\armagomen.battleObserver_%ModVersion%.wotmod
set ZipArh=..\BattleObserver_WOT_EU.zip
set AutoUpdate=..\AutoUpdate.zip

DEL %OutputDir%\armagomen.battleObserver*
DEL %GameInstalled_ModsDir%\armagomen.battleObserver*
DEL %ZipArh%
DEL %AutoUpdate%

"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx0 -x!*.py %ModFile% .\mod\*
"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %ZipArh% ..\output_data\*
"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %AutoUpdate% %ModFile%

Xcopy %ModFile% %GameInstalled_ModsDir% /e /i /d

DEL /s /q *.pyc
exit