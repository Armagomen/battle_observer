[Files]
Source: img\splashscreen.png; Flags: dontcopy noencryption deleteafterinstall
Source: dll\isgsg.dll; Flags: ignoreversion dontcopy nocompression deleteafterinstall


[Code]
procedure ShowSplashScreen(p1:HWND;p2:AnsiString;p3,p4,p5,p6,p7:integer;p8:boolean;p9:Cardinal;p10:integer); external 'ShowSplashScreen@files:isgsg.dll stdcall delayload';

<event('InitializeWizard')>
procedure SplashScreen();
begin
  ExtractTemporaryFile('splashscreen.png');
  ExtractTemporaryFile('isgsg.dll');
  ShowSplashScreen(WizardForm.Handle,ExpandConstant('{tmp}\splashscreen.png'),500,2000,500,0,255,False,$FFFFFF,4);
end;

