[Code]

<event('InitializeWizard')>
procedure SetWizardForm();  
begin  
  WizardForm.Width:=700;  
  WizardForm.Height:=500;
  WizardForm.WizardSmallBitmapImage.Width := 60;
  WizardForm.WizardSmallBitmapImage.Height := 60;
  WizardForm.WizardSmallBitmapImage.Left := 600;

  WizardForm.PageNameLabel.AutoSize := True;
  WizardForm.PageDescriptionLabel.AutoSize := True;  
end;


{open wg utils}
var
  WotList: TNewComboBox;

function CHECK_IsLesta(): Boolean;
var
  Flavour: Integer;
begin
  Flavour := WotList_Selected_Record(WotList).LauncherFlavour
  Result := Flavour = 4;
end;

function PH_Folder_Mods(s: String): String;
begin
  Result := WotList_Selected_Record(WotList).PathMods;
end;

function PH_Folder_Resmods(s: String): String;
begin
  Result := WotList_Selected_Record(WotList).PathResmods;
end;

<event('InitializeWizard')>
procedure ClientFind();
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


<event('CurPageChanged')> 
procedure onCurPageChanged(CurPage: Integer);
begin
  case CurPage of
    wpSelectDir: CurPageChanged_wpSelectDir();
    wpSelectComponents: CurPageChanged_wpSelectComponents();
  end
end;



// CurUninstallStepChanged
procedure CurUninstallStepChanged_usUninstall();
begin
  OPENWG_DllUnload();
  OPENWG_DllDelete();
end;
<event('CurUninstallStepChanged')> 
procedure onCurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  case CurUninstallStep of
    usUninstall: CurUninstallStepChanged_usUninstall();
  end
end;


// NextButtonClick
function NextButtonClick_wpSelectDir(): Boolean;
begin
  Result := True;
  // check for version
  // if CHECK_IsLesta() and not WotList_Selected_VersionMatch(WotList, '{#VERSION_PATTERN_LESTA}') then
  // begin
  //   Result := False;
  //   MsgBox(ExpandConstant('{cm:version_not_match_lesta}'), mbError, MB_OK);
  //   Exit;
  // end;
  
  // if not CHECK_IsLesta() and not WotList_Selected_VersionMatch(WotList, '{#VERSION_PATTERN_WG}') then
  // begin
  //   Result := False;
  //   MsgBox(ExpandConstant('{cm:version_not_match_wg}'), mbError, MB_OK);
  //   Exit;
  // end;
  
  if WotList_Selected_IsStarted(WotList) then
  begin
    if (MsgBox(ExpandConstant('{cm:client_started}'), mbConfirmation, MB_YESNO) = IDYES) then 
      WotList_Selected_Terminate(WotList)
    else
      Result := False;
  end;
end;

<event('NextButtonClick')> 
function onNextButtonClick(CurPage: Integer): Boolean;
begin
  Result := True;

  case CurPage of
    wpSelectDir: Result := NextButtonClick_wpSelectDir();
  end;
end;

