@Echo off
set ModVer=1.29.0

set WotVer=1.9.1.0
REM set WotVer="1.8.0.0 Common Test"

set ModsDir=E:\Games\World_of_Tanks_RU\mods\
REM set ModsDir=F:\Games\World_of_Tanks_CT\mods\

"python.exe" newCompileall.py -f -q -d scripts mod\res\scripts

set ModFile=%ModsDir%%WotVer%\armagomen.battleObserver_%ModVer%.wotmod
set API=%ModsDir%%WotVer%\polarfox.vxSettingsApi*
set API2=%ModsDir%%WotVer%\poliroid.modslistapi*
set ZipArh=..\BO_%ModVer%_WOT_%WotVer%.zip
set ToExclude=-x!*.db -x!*.log -x!vxSettingsApi -x!res_mods -x!logs -x!*ShuraBB*
set lastUpdate=..\BattleObserver_LastUpdate.zip

DEL %ModsDir%%WotVer%\armagomen.battleObserver*
DEL %ModsDir%%WotVer%\temp*
DEL %ModsDir%%WotVer%\readme*
DEL %ZipArh%
DEL %lastUpdate%

"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx0 -x!*.py -x!*.cmd %ModFile% .\mod\*
"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %ToExclude% %ZipArh% %ModsDir%

"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %lastUpdate% %ModFile% %API% %API2%
REM "%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %lastUpdate% %ModFile%
exit