@Echo off
set ModVer=1.31.2

set WotVer=1.11.1.0
REM set WotVer="1.11.1.0 Common Test"

set ModsDir=D:\Games\World_of_Tanks_RU\mods\
REM set ModsDir=E:\Games\World_of_Tanks_CT\mods\

"python.exe" newCompileall.py -f -q -d scripts mod\res\scripts

set ModFile=%ModsDir%%WotVer%\armagomen.battleObserver_%ModVer%.wotmod
set API=%ModsDir%%WotVer%\polarfox.vxSettingsApi*
set API2=%ModsDir%%WotVer%\poliroid.modslistapi*
set ZipArh=..\BattleObserver_%ModVer%_WOT_%WotVer%.zip
set ToExclude=-x!*.db -x!*.log -x!vxSettingsApi -x!res_mods -x!logs -x!*ShuraBB*
set AutoUpdate=..\AutoUpdate.zip

DEL %ModsDir%%WotVer%\armagomen.battleObserver*
DEL %ModsDir%%WotVer%\temp*
DEL %ModsDir%%WotVer%\readme*
DEL %ZipArh%
DEL %lastUpdate%

"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx0 -x!*.py -x!*.cmd %ModFile% .\mod\*
"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %ToExclude% %ZipArh% %ModsDir%
"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %AutoUpdate% %ModFile% %API%
REM "%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %AutoUpdate% %ModFile%

set lastUpdateOld=..\BattleObserver_LastUpdate.zip
set ZipArhOld=..\BO_%ModVer%_WOT_%WotVer%.zip
"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %ToExclude% %ZipArhOld% %ModsDir%
"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %lastUpdateOld% %ModFile% %API%
REM "%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %lastUpdateOld% %ModFile%

DEL /s /q *.pyc
exit