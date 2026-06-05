[CustomMessages]
uk.uninstall_caption=Видалення Battle Observer
uk.uninstall_desc=Виберіть параметри видалення
uk.uninstall_ready_caption=Готово до видалення
uk.uninstall_ready_desc=Натисніть "Видалити", щоб продовжити
uk.uninstall_remove_all=Видалити всі дані (включно з configs)
uk.uninstall_press_uninstall=Натисніть "Видалити", щоб продовжити деінсталяцію.
uk.uninstall_button=Видалити


en.uninstall_caption=Battle Observer Uninstallation
en.uninstall_desc=Choose removal options
en.uninstall_ready_caption=Ready to uninstall
en.uninstall_ready_desc=Press "Uninstall" to proceed
en.uninstall_remove_all=Remove all data (including configs)
en.uninstall_press_uninstall=Press "Uninstall" to proceed with uninstallation.
en.uninstall_button=Uninstall


[Code]

var
  UninstallFirstPage: TNewNotebookPage;
  UninstallSecondPage: TNewNotebookPage;
  UninstallBackButton: TNewButton;
  UninstallNextButton: TNewButton;
  RemoveConfigsCheck: TNewCheckBox;
  RemoveConfigsSelected: Boolean; // глобальна змінна

procedure UpdateUninstallWizard;
begin
  if UninstallProgressForm.InnerNotebook.ActivePage = UninstallFirstPage then
  begin
    UninstallProgressForm.PageNameLabel.Caption := ExpandConstant('{cm:uninstall_caption}');
    UninstallProgressForm.PageDescriptionLabel.Caption := ExpandConstant('{cm:uninstall_desc}');
  end
  else
  if UninstallProgressForm.InnerNotebook.ActivePage = UninstallSecondPage then
  begin
    UninstallProgressForm.PageNameLabel.Caption := ExpandConstant('{cm:uninstall_ready_caption}');
    UninstallProgressForm.PageDescriptionLabel.Caption := ExpandConstant('{cm:uninstall_ready_desc}');
  end;

  UninstallBackButton.Visible :=
    (UninstallProgressForm.InnerNotebook.ActivePage <> UninstallFirstPage);

  if UninstallProgressForm.InnerNotebook.ActivePage <> UninstallSecondPage then
  begin
    UninstallNextButton.Caption := SetupMessage(msgButtonNext);
    UninstallNextButton.ModalResult := mrNone;
  end
  else
  begin
    UninstallNextButton.Caption := ExpandConstant('{cm:uninstall_button}');
    UninstallNextButton.ModalResult := mrOK;
  end;
end;

procedure UninstallNextButtonClick(Sender: TObject);
begin
  if UninstallProgressForm.InnerNotebook.ActivePage = UninstallSecondPage then
  begin
    // зберігаємо стан чекбокса перед завершенням
    RemoveConfigsSelected := RemoveConfigsCheck.Checked;

    UninstallNextButton.Visible := False;
    UninstallBackButton.Visible := False;
  end
  else
  begin
    if UninstallProgressForm.InnerNotebook.ActivePage = UninstallFirstPage then
      UninstallProgressForm.InnerNotebook.ActivePage := UninstallSecondPage;
    UpdateUninstallWizard;
  end;
end;

procedure UninstallBackButtonClick(Sender: TObject);
begin
  if UninstallProgressForm.InnerNotebook.ActivePage = UninstallSecondPage then
    UninstallProgressForm.InnerNotebook.ActivePage := UninstallFirstPage;
  UpdateUninstallWizard;
end;

procedure InitializeUninstallProgressForm();
var
  PageText: TNewStaticText;
  PageNameLabel: string;
  PageDescriptionLabel: string;
  CancelButtonEnabled: Boolean;
  CancelButtonModalResult: Integer;
begin
  if not UninstallSilent then
  begin
    // Перша сторінка
    UninstallFirstPage := TNewNotebookPage.Create(UninstallProgressForm);
    UninstallFirstPage.Notebook := UninstallProgressForm.InnerNotebook;
    UninstallFirstPage.Parent := UninstallProgressForm.InnerNotebook;
    UninstallFirstPage.Align := alClient;

    RemoveConfigsCheck := TNewCheckBox.Create(UninstallFirstPage);
    RemoveConfigsCheck.Parent := UninstallFirstPage;
    RemoveConfigsCheck.Caption := ExpandConstant('{cm:uninstall_remove_all}');
    RemoveConfigsCheck.Left := ScaleX(20);
    RemoveConfigsCheck.Top := ScaleY(40);
    RemoveConfigsCheck.Width := UninstallProgressForm.ClientWidth - ScaleX(40);
    RemoveConfigsCheck.Height := ScaleY(30);
    RemoveConfigsCheck.Font.Size := UninstallProgressForm.StatusLabel.Font.Size;

    UninstallProgressForm.InnerNotebook.ActivePage := UninstallFirstPage;

    PageNameLabel := UninstallProgressForm.PageNameLabel.Caption;
    PageDescriptionLabel := UninstallProgressForm.PageDescriptionLabel.Caption;

    // Друга сторінка
    UninstallSecondPage := TNewNotebookPage.Create(UninstallProgressForm);
    UninstallSecondPage.Notebook := UninstallProgressForm.InnerNotebook;
    UninstallSecondPage.Parent := UninstallProgressForm.InnerNotebook;
    UninstallSecondPage.Align := alClient;

    PageText := TNewStaticText.Create(UninstallProgressForm);
    PageText.Parent := UninstallSecondPage;
    PageText.Caption := ExpandConstant('{cm:uninstall_press_uninstall}');
    PageText.Left := ScaleX(20);
    PageText.Top := ScaleY(40);
    PageText.Width := UninstallProgressForm.ClientWidth - ScaleX(40);
    PageText.Font.Size := UninstallProgressForm.StatusLabel.Font.Size;

    // Кнопки
    UninstallNextButton := TNewButton.Create(UninstallProgressForm);
    UninstallNextButton.Parent := UninstallProgressForm;
    UninstallNextButton.Left :=
      UninstallProgressForm.CancelButton.Left -
      UninstallProgressForm.CancelButton.Width -
      ScaleX(10);
    UninstallNextButton.Top := UninstallProgressForm.CancelButton.Top;
    UninstallNextButton.Width := UninstallProgressForm.CancelButton.Width;
    UninstallNextButton.Height := UninstallProgressForm.CancelButton.Height;
    UninstallNextButton.OnClick := @UninstallNextButtonClick;

    UninstallBackButton := TNewButton.Create(UninstallProgressForm);
    UninstallBackButton.Parent := UninstallProgressForm;
    UninstallBackButton.Left :=
      UninstallNextButton.Left - UninstallNextButton.Width -
      ScaleX(10);
    UninstallBackButton.Top := UninstallProgressForm.CancelButton.Top;
    UninstallBackButton.Width := UninstallProgressForm.CancelButton.Width;
    UninstallBackButton.Height := UninstallProgressForm.CancelButton.Height;
    UninstallBackButton.Caption := SetupMessage(msgButtonBack);
    UninstallBackButton.OnClick := @UninstallBackButtonClick;

    UpdateUninstallWizard;

    CancelButtonEnabled := UninstallProgressForm.CancelButton.Enabled;
    UninstallProgressForm.CancelButton.Enabled := True;
    CancelButtonModalResult := UninstallProgressForm.CancelButton.ModalResult;
    UninstallProgressForm.CancelButton.ModalResult := mrCancel;

    if UninstallProgressForm.ShowModal = mrCancel then Abort;

    // Restore
    UninstallProgressForm.CancelButton.Enabled := CancelButtonEnabled;
    UninstallProgressForm.CancelButton.ModalResult := CancelButtonModalResult;
    UninstallProgressForm.PageNameLabel.Caption := PageNameLabel;
    UninstallProgressForm.PageDescriptionLabel.Caption := PageDescriptionLabel;
    UninstallProgressForm.InnerNotebook.ActivePage :=
      UninstallProgressForm.InstallingPage;
  end;
end;

// Виконується після завершення стандартного процесу
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if (CurUninstallStep = usPostUninstall) and RemoveConfigsSelected then
  begin
    DelTree(ExpandConstant('{app}\mods\configs\mod_battle_observer'), True, True, True);
  end;
end;
