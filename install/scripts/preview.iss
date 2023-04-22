[Files]

Source: img\test.bmp; Flags: dontcopy



[Code]

var
  CompLabel: TLabel;
  CompImage: TBitmapImage;
  LoadingImage: Boolean;
  LastMouse: TPoint;

function GetCursorPos(var lpPoint: TPoint): BOOL; external 'GetCursorPos@user32.dll stdcall';
function SetTimer(hWnd: longword; nIDEvent, uElapse: LongWord; lpTimerFunc: LongWord): LongWord; external 'SetTimer@user32.dll stdcall';
function ScreenToClient(hWnd: HWND; var lpPoint: TPoint): BOOL; external 'ScreenToClient@user32.dll stdcall';
function ClientToScreen(hWnd: HWND; var lpPoint: TPoint): BOOL; external 'ClientToScreen@user32.dll stdcall';
function ListBox_GetItemRect(const hWnd: HWND; const Msg: Integer; Index: LongInt; var Rect: TRect): LongInt; external 'SendMessageW@user32.dll stdcall';  

const
  LB_GETITEMRECT = $0198;
  LB_GETTOPINDEX = $018E;



procedure HoverComponentChanged(Index: Integer);
var 
  Description: string;
  Image: string;
  ImagePath: string;
begin
    
    Image := 'test.bmp';
    Description := 'This is the description of Main Files';

  //case Index of
  //  0: begin Description := 'This is the description of Main Files'; Image := 'main.bmp'; end;
  //  1: begin Description := 'This is the description of Additional Files'; Image := 'additional.bmp'; end;
  //  2: begin Description := 'This is the description of Help Files'; Image := 'help.bmp'; end;
  //else
  //  Description := 'Move your mouse over a component to see its description.';
  //end;
  CompLabel.Caption := Description;

  if Image <> '' then
  begin
    { The ExtractTemporaryFile pumps the message queue, prevent recursion }
    if not LoadingImage then
    begin
      LoadingImage := True;
      try
        ImagePath := ExpandConstant('{tmp}\' + Image);
        if not FileExists(ImagePath) then
        begin
          ExtractTemporaryFile(Image);
        end;
        CompImage.Bitmap.LoadFromFile(ImagePath);
      finally
        LoadingImage := False;
      end;
    end;
    CompImage.Visible := True;
  end
    else
  begin
    CompImage.Visible := False;
  end;
end;

function FindControl(Parent: TWinControl; P: TPoint): TControl;
var
  Control: TControl;
  WinControl: TWinControl;
  I: Integer;
  P2: TPoint;
begin
  for I := 0 to Parent.ControlCount - 1 do
  begin
    Control := Parent.Controls[I];
    if Control.Visible and
       (Control.Left <= P.X) and (P.X < Control.Left + Control.Width) and
       (Control.Top <= P.Y) and (P.Y < Control.Top + Control.Height) then
    begin
      if Control is TWinControl then
      begin
        P2 := P;
        ClientToScreen(Parent.Handle, P2);
        WinControl := TWinControl(Control);
        ScreenToClient(WinControl.Handle, P2);
        Result := FindControl(WinControl, P2);
        if Result <> nil then Exit;
      end;

      Result := Control;
      Exit;
    end;
  end;

  Result := nil;
end;

function PointInRect(const Rect: TRect; const Point: TPoint): Boolean;
begin
  Result :=
    (Point.X >= Rect.Left) and (Point.X <= Rect.Right) and
    (Point.Y >= Rect.Top) and (Point.Y <= Rect.Bottom);
end;

function ListBoxItemAtPos(ListBox: TCustomListBox; Pos: TPoint): Integer;
var
  Count: Integer;
  ItemRect: TRect;
begin
  Result := SendMessage(ListBox.Handle, LB_GETTOPINDEX, 0, 0);
  Count := ListBox.Items.Count;
  while Result < Count do
  begin
    ListBox_GetItemRect(ListBox.Handle, LB_GETITEMRECT, Result, ItemRect);
    if PointInRect(ItemRect, Pos) then Exit;
    Inc(Result);
  end;
  Result := -1;
end;

procedure HoverTimerProc(H: LongWord; Msg: LongWord; IdEvent: LongWord; Time: LongWord);
var
  P: TPoint;
  Control: TControl; 
  Index: Integer;
begin
  GetCursorPos(P);
  if P <> LastMouse then { just optimization }
  begin
    LastMouse := P;
    ScreenToClient(WizardForm.Handle, P);

    if (P.X < 0) or (P.Y < 0) or
       (P.X > WizardForm.ClientWidth) or (P.Y > WizardForm.ClientHeight) then
    begin
      Control := nil;
    end
      else
    begin
      Control := FindControl(WizardForm, P);
    end;

    Index := -1;
    if (Control = WizardForm.ComponentsList) and
       (not WizardForm.TypesCombo.DroppedDown) then
    begin
      P := LastMouse;
      ScreenToClient(WizardForm.ComponentsList.Handle, P);
      Index := ListBoxItemAtPos(WizardForm.ComponentsList, P);
    end;

    HoverComponentChanged(Index);
  end;
end;

<event('InitializeWizard')>
procedure onInitializeWizard();
begin
  WizardForm.ComponentsList.Left:=264;
  WizardForm.ComponentsList.Width:=340;
  
  SetTimer(0, 0, 50, CreateCallback(@HoverTimerProc));

  CompImage := TBitmapImage.Create(WizardForm);
  CompImage.Parent := WizardForm.SelectComponentsPage;
  CompImage.Top := WizardForm.ComponentsList.Top + 20;
  CompImage.Width := 200;
  CompImage.Height := 200;
  CompImage.Left := 20;

  CompLabel := TLabel.Create(WizardForm);
  CompLabel.Parent := WizardForm.SelectComponentsPage;
  CompLabel.Left := 20
  CompLabel.Width := 200;
  CompLabel.Height := 200;
  CompLabel.Top := CompImage.Top + CompImage.Height + 5;
  CompLabel.AutoSize := False;
  CompLabel.WordWrap := True;
end;

