@Echo off
set ModVer=1.39.8

set WotVer=1.18.1.0
set ModsDir=C:\Games\World_of_Tanks_EU\mods

REM set WotVer="1.18.1.0 Common Test"
REM set ModsDir=C:\Games\World_of_Tanks_CT\mods

"python.exe" bo_compile_all.py -f -q -d scripts mod\res\scripts

set ModFile=%ModsDir%\%WotVer%\armagomen.battleObserver_%ModVer%.wotmod
set ZipArh=..\BattleObserver_%ModVer%_WOT_%WotVer%.zip
set ToExclude=-x!*.db -x!*.log -x!res_mods -x!logs -x!other -x!protanki
DEL %ModsDir%\%WotVer%\armagomen.battleObserver*
DEL %ModsDir%\%WotVer%\temp*
DEL %ModsDir%\%WotVer%\readme*
DEL ..\BattleObserver_*
DEL ..\AutoUpdate.zip

"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx0 -x!*.py -x!*.cmd %ModFile% .\mod\*
"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %ToExclude% %ZipArh% %ModsDir%\%WotVer%\ %ModsDir%\configs\
"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %ToExclude% ..\AutoUpdate.zip %ModsDir%\%WotVer%\*

DEL /s /q *.pyc
exit