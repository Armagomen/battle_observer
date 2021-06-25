@Echo off
set ModVer=1.33.5

set WotVer=1.13.0.0
set ModsDir=C:\Games\World_of_Tanks_RU\mods\

REM set WotVer="1.13.0.0 Common Test"
REM set ModsDir=D:\Games\World_of_Tanks_CT\mods\

"python.exe" bo_compile_all.py -f -q -d scripts mod\res\scripts

set ModFile=%ModsDir%%WotVer%\armagomen.battleObserver_%ModVer%.wotmod
set API=%ModsDir%%WotVer%\polarfox.vxSettingsApi*
set API2=%ModsDir%%WotVer%\poliroid.modslistapi*
set ZipArh=..\BattleObserver_%ModVer%_WOT_%WotVer%.zip
set ToExclude=-x!*.db -x!*.log -x!res_mods -x!logs -x!*andre_v* -x!*protanki*
set AutoUpdate=..\AutoUpdate.zip

DEL %ModsDir%%WotVer%\armagomen.battleObserver*
DEL %ModsDir%%WotVer%\temp*
DEL %ModsDir%%WotVer%\readme*
DEL ..\BattleObserver_*
DEL %AutoUpdate%

"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx0 -x!*.py -x!*.cmd %ModFile% .\mod\*
"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %ToExclude% %ZipArh% %ModsDir%
"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %AutoUpdate% %ModFile%
REM "%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %AutoUpdate% %ModFile%

DEL /s /q *.pyc
exit