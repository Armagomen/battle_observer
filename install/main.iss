#define MyAppName "Battle Observer"
#define MyAppPublisher "Armagomen, Inc."
#define MyAppURL "https://github.com/Armagomen/battle_observer"
#define MyAppUpdatesURL MyAppURL+"/releases/latest/"
#define WOT_VERSION_PATTERN "1.*"
#define APP_FILE_PATTERN "mod_battle_observer_v"
#define APP_DIR_UNINST "battle_observer_uninst"
#define OPENWGUTILS_DIR_SRC "dll"
#define OPENWGUTILS_DIR_UNINST APP_DIR_UNINST

#include "scripts\openwg.utils.iss"
#include "scripts\code.iss"
//#include "scripts\splash.iss"

#ifndef MyAppVersion
  #define MyAppVersion "1.0.0.0"
#endif

[Setup]
AppId={{E4911938-A29D-4904-8878-99DEEBDE03D6}
AppName={#MyAppName}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL=https://discord.gg/Nma5T5snKW
AppUpdatesURL={#MyAppUpdatesURL}
AppVerName={#MyAppName} {#MyAppVersion}
AppVersion={#MyAppVersion}
AppendDefaultDirName=no
DefaultDirName={sd}\{#MyAppName}
DefaultGroupName={#MyAppName}
DirExistsWarning=no
DisableProgramGroupPage=yes
OutputBaseFilename={#APP_FILE_PATTERN}{#MyAppVersion}
OutputDir=..\..\
SetupIconFile=img\BattleObserver_icon.ico
WizardSmallImageFile=img\small.bmp
WizardImageFile=img\big.bmp
ShowComponentSizes=no
UninstallFilesDir={app}\{#APP_DIR_UNINST}
VersionInfoVersion={#MyAppVersion}
WizardResizable=no
WizardStyle=modern


[Run]
Filename: "https://donatua.com/to/armagomen"; Description: "{cm:open_donate}"; Flags: postinstall nowait shellexec;
Filename: "https://www.patreon.com/armagomen"; Description: "{cm:open_patreon}"; Flags: postinstall nowait shellexec;
Filename: "https://www.paypal.com/donate/?hosted_button_id=VJCUNYNBXBEG8"; Description: "PayPal"; Flags: postinstall nowait shellexec unchecked;
Filename: "https://discord.gg/Nma5T5snKW"; Description: "DISCORD"; Flags: postinstall nowait shellexec unchecked;


[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"; LicenseFile: "..\EULA_EN.txt"; 
Name: "uk"; MessagesFile: "compiler:Languages\Ukrainian.isl"; LicenseFile: "..\EULA_UK.txt";

[Icons]
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"; IconFilename: "{uninstallexe}";

#include "scripts\messages\uk.iss"
#include "scripts\messages\en.iss"
#include "scripts\components.iss"
//#include "scripts\preview.iss"

