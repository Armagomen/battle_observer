@Echo off

set "ModVersion="
for /f "tokens=3 delims=<>" %%a in (
    'find /i "<version>" ^< ".\mod\meta.xml"'
) do set "ModVersion=%%a"

set sources=.\mod
set GameVersion=2.0.0.2
set GameInstalled_ModsDir=C:\Games\World_of_Tanks_EU\mods\%GameVersion%
REM set GameInstalled_ModsDir=C:\Games\World_of_Tanks_CT\mods\%GameVersion% Common Test

"C:\Python27\python.exe" bo_compile_all.py -f -d scripts %sources%\res\scripts

set OutputDir=..\output_data
set ModFile=%OutputDir%\armagomen.battleObserver_%ModVersion%.wotmod
set AutoUpdate=..\AutoUpdate.zip

DEL ..\mod_battle_observer_*
DEL %OutputDir%\armagomen.battleObserver*
DEL %AutoUpdate%
DEL %GameInstalled_ModsDir%\armagomen.battleObserver*
DEL %GameInstalled_ModsDir%\me.poliroid.modslistapi*
DEL %GameInstalled_ModsDir%\polarfox.vxSettingsApi*

"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx0 -x!*.py %ModFile% %sources%\*
"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 -x!armagomen.battle_observer_icons* %AutoUpdate% %OutputDir%\*

Xcopy %OutputDir% %GameInstalled_ModsDir% /e /i /d

"%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" /DMyAppVersion=%ModVersion% .\install\main.iss

DEL /s /q *.pyc

exit