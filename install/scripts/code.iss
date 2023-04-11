[Files]
//Source: "img\splashscreen.png"; Flags: dontcopy noencryption deleteafterinstall
//Source: "img\splashscreen_uninst.png"; DestDir: "{app}\{#APP_DIR_UNINST}"; Flags: noencryption;

[Code]

//
// Globals
//

var
  WotList: TNewComboBox;


//
// Checks
//

function CHECK_IsLesta(): Boolean;
var
  Flavour: Integer;
begin
  Flavour := WotList_Selected_Record(WotList).LauncherFlavour
  Result := Flavour = 4;
end;



//
// Placeholders
//

function PH_Folder_Mods(s: String): String;
begin
  Result := WotList_Selected_Record(WotList).PathMods;
end;

function PH_Folder_Resmods(s: String): String;
begin
  Result := WotList_Selected_Record(WotList).PathResmods;
end;



//
// Initialize
//


//function InitializeSetup: Boolean;
//begin
//  ExtractTemporaryFile('splashscreen.png');
//  SPLASHSCREEN_ShowSplashScreenW(ExpandConstant('{tmp}\splashscreen.png'), 3);
//  Result := True;
//end;


//function InitializeUninstall: Boolean;
//begin
//  SPLASHSCREEN_ShowSplashScreenW(ExpandConstant('{app}\{#APP_DIR_UNINST}\splashscreen_uninst.png'), 3);
//  Result := True;
//end;


procedure InitializeWizard();
begin
  WotList := WotList_Create(WizardForm.DirEdit.Parent,
      WizardForm.DirEdit.Left,
      WizardForm.DirEdit.Top,
      WizardForm.DirBrowseButton.Left + WizardForm.DirBrowseButton.Width,
      WizardForm.DirEdit.Height
  );
  WotList.ItemIndex := WOT_ClientFind(WizardForm.DirEdit.Text);

  if (WotList.ItemIndex = -1) and (WotList.Items.Count > 1) then
    WotList.ItemIndex := 0;
  WotList.OnChange(WotList);

  WizardForm.DirEdit.Visible := False;
  WizardForm.DirBrowseButton.Visible := False;
end;



//
// CurPageChanged
//

procedure CurPageChanged_wpSelectDir();
begin
end;


procedure CurPageChanged_wpSelectComponents();
var
  Index: Integer;
  IsLesta: Boolean;
  ItemCaption: String;
begin
  IsLesta := CHECK_IsLesta();

  for Index := 0 to WizardForm.ComponentsList.Items.Count - 1 do
  begin
    ItemCaption := WizardForm.ComponentsList.ItemCaption[Index];
    if ((pos('Lesta', ItemCaption) <> 0) and (not IsLesta)) or ((pos('WG', ItemCaption) <> 0) and IsLesta) then
    begin
        WizardForm.ComponentsList.Checked[Index] := false; 
        WizardForm.ComponentsList.ItemEnabled[Index] := false;   
    end;
  end;
end;


procedure CurPageChanged(CurPage: Integer);
begin
  case CurPage of
    wpSelectDir: CurPageChanged_wpSelectDir();
    wpSelectComponents: CurPageChanged_wpSelectComponents();
  end
end;



//
// CurUninstallStepChanged
//

procedure CurUninstallStepChanged_usUninstall();
begin
  OPENWG_DllUnload();
  OPENWG_DllDelete();
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  case CurUninstallStep of
    usUninstall: CurUninstallStepChanged_usUninstall();
  end
end;



//
// DeinitializeUninstall
//

procedure DeinitializeUninstall();
begin
end;



//
// NextButtonClick
//

function NextButtonClick_wpSelectDir(): Boolean;
begin
  Result := True;

  // check for version
  if not WotList_Selected_VersionMatch(WotList, '{#WOT_VERSION_PATTERN}') then
  begin
    MsgBox(ExpandConstant('{cm:version_not_match}'), mbError, MB_OK);
    Result := False;
    Exit;
  end;

  // check for running client
  if WotList_Selected_IsStarted(WotList) then
  begin
    if (MsgBox(ExpandConstant('{cm:client_started}'), mbConfirmation, MB_YESNO) = IDYES) then 
      WotList_Selected_Terminate(WotList)
    else
      Result := False;
  end;
end;


function NextButtonClick(CurPage: Integer): Boolean;
begin
  Result := True;

  case CurPage of
    wpSelectDir: Result := NextButtonClick_wpSelectDir();
  end;
end;

