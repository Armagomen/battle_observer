@Echo off

set "ModVersion="
for /f "tokens=3 delims=<>" %%a in (
    'find /i "<version>" ^< ".\mod\meta.xml"'
) do set "ModVersion=%%a"

set sources=.\mod
set GameVersion=1.24.1.2
set GameInstalled_ModsDir=C:\Games\World_of_Tanks_EU\mods\%GameVersion%
set OutputDir=..\output_data

REM set GameVersion="1.24.1.0 Common Test"
REM set GameInstalled_ModsDir=C:\Games\World_of_Tanks_CT\mods

"python.exe" bo_compile_all.py -f -d scripts %sources%\res\scripts

set ModFile=%OutputDir%\armagomen.battleObserver_%ModVersion%.wotmod
set AutoUpdate=..\AutoUpdate.zip

DEL ..\mod_battle_observer_*
DEL %OutputDir%\armagomen.battleObserver*
DEL %GameInstalled_ModsDir%\armagomen.battleObserver*
DEL %AutoUpdate%

"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx0 -x!*.py %ModFile% %sources%\*
"%ProgramFiles%\7-Zip\7z.exe" a -tzip -r -mx9 %AutoUpdate% %OutputDir%\*

Xcopy %OutputDir% %GameInstalled_ModsDir% /e /i /d

"%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" /DMyAppVersion=%ModVersion% .\install\main.iss

DEL /s /q *.pyc

REM exit