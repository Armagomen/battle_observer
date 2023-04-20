#define configs_dir "{app}\mods\configs\mod_battle_observer"
#define mod_source "..\..\output_data"

[Types]
Name: "armagomen"; Description: {cm:types_armagomen};
Name: "user"; Description: {cm:types_user}; Flags: iscustom; 

[Components]
// main.json
Name: anti_anonymous; Description: {cm:anti_anonymous}; Flags: disablenouninstallwarning;
Name: auto_crew_training; Description: {cm:auto_crew_training}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: auto_return_crew; Description: {cm:auto_return_crew}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: clear_cache_automatically; Description: {cm:clear_cache_automatically}; Flags: disablenouninstallwarning;
Name: disable_score_sound; Description: {cm:disable_score_sound}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: disable_stun_sound; Description: {cm:disable_stun_sound}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: directives_only_from_storage; Description: {cm:directives_only_from_storage}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: hide_badges; Description: {cm:hide_badges}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: hide_button_counters_on_top_panel; Description: {cm:hide_button_counters_on_top_panel}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: hide_clan_abbrev; Description: {cm:hide_clan_abbrev}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: hide_dog_tags; Description: {cm:hide_dog_tags}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: hide_field_mail; Description: {cm:hide_field_mail}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: hide_hint_panel; Description: {cm:hide_hint_panel}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: hide_main_chat_in_hangar; Description: {cm:hide_main_chat_in_hangar}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: ignore_commanders_voice; Description: {cm:ignore_commanders_voice}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: mute_team_base_sound; Description: {cm:mute_team_base_sound}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: premium_time; Description: {cm:premium_time}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: save_shot; Description: {cm:save_shot}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: show_friends; Description: {cm:show_friends}; Flags: disablenouninstallwarning; Types: "armagomen";

//clock
Name: clock; Description: {cm:clock}; Flags: dontinheritcheck checkablealone disablenouninstallwarning; 
Name: clock/hangar; Description: {cm:clock_hangar}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: clock/battle; Description: {cm:clock_battle}; Flags: disablenouninstallwarning; Types: "armagomen";

//hp_bars
Name: hp_bars; Description: {cm:hp_bars}; Flags: checkablealone disablenouninstallwarning;
Name: hp_bars/alive_count; Description: {cm:alive_count}; Flags: dontinheritcheck disablenouninstallwarning;
Name: hp_bars/normal; Description: {cm:hp_normal}; Flags: exclusive disablenouninstallwarning;
Name: hp_bars/league; Description: {cm:hp_league}; Flags: exclusive disablenouninstallwarning; Types: "armagomen";

//debug_panel
Name: debug_panel; Description: {cm:debug_panel}; Flags: checkablealone disablenouninstallwarning; 
Name: debug_panel/minimal; Description: minimal; Flags: exclusive disablenouninstallwarning;
Name: debug_panel/modern; Description: modern; Flags: exclusive disablenouninstallwarning; Types: "armagomen";

//dispersion_circle
Name: dispersion_circle; Description: {cm:dispersion_circle}; Flags: checkablealone disablenouninstallwarning;
Name: dispersion_circle/replace; Description: {cm:dispersion_circle_replace}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: dispersion_circle/server; Description: {cm:dispersion_circle_server}; Flags: disablenouninstallwarning;
Name: dispersion_timer; Description: {cm:dispersion_timer}; Flags: disablenouninstallwarning; Types: "armagomen";

Name: sixth_sense; Description: {cm:sixth_sense}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: arcade_camera; Description: {cm:arcade_camera}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: armor_calculator; Description: {cm:armor_calculator}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: avg_efficiency_in_hangar; Description: {cm:avg_efficiency_in_hangar}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: battle_timer; Description: {cm:battle_timer}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: distance_to_enemy; Description: {cm:distance_to_enemy}; Flags: disablenouninstallwarning;
Name: effects; Description: {cm:effects}; Flags: disablenouninstallwarning; Types: "armagomen user";
Name: flight_time; Description: {cm:flight_time}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: log_extended; Description: {cm:log_extended}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: log_total; Description: {cm:log_total}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main_gun; Description: {cm:main_gun}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: minimap; Description: {cm:minimap}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: own_health; Description: {cm:own_health}; Flags: disablenouninstallwarning;
Name: players_panels; Description: {cm:players_panels}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: service_channel_filter; Description: {cm:service_channel_filter}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: statistics; Description: {cm:statistics}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: strategic_camera; Description: {cm:strategic_camera}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: tank_carousel; Description: {cm:tank_carousel}; Flags: disablenouninstallwarning;
Name: team_bases_panel; Description: {cm:team_bases_panel}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: wg_logs; Description: {cm:wg_logs}; Flags: disablenouninstallwarning;
Name: zoom; Description: {cm:zoom}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: colors; Description: {cm:colors}; Flags: fixed disablenouninstallwarning; Types: "armagomen user";

[Files]
Source: "{#mod_source}\*"; DestDir: "{app}\{code:PH_Folder_Mods}"; Flags: ignoreversion;
Source: "settings\load.json"; DestDir: "{#configs_dir}"; Flags: ignoreversion;
Source: "settings\main.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion;
Source: "settings\hp_bars.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: hp_bars;
Source: "settings\clock.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: clock;
Source: "settings\debug_panel.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: debug_panel;
Source: "settings\dispersion_circle.json"; DestDir: "{#configs_dir}\armagomen";  Flags: ignoreversion; Components: dispersion_circle;
Source: "settings\dispersion_timer.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: dispersion_timer;

 
Source: "settings\sixth_sense.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: sixth_sense;
Source: "settings\arcade_camera.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: arcade_camera;
Source: "settings\armor_calculator.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: armor_calculator;
Source: "settings\avg_efficiency_in_hangar.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: avg_efficiency_in_hangar;
Source: "settings\battle_timer.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: battle_timer;
Source: "settings\distance_to_enemy.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: distance_to_enemy;
Source: "settings\effects.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: effects;
Source: "settings\flight_time.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: flight_time;
Source: "settings\log_extended.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: log_extended;
Source: "settings\log_total.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: log_total;
Source: "settings\main_gun.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: main_gun;
Source: "settings\minimap.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: minimap;
Source: "settings\own_health.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: own_health;
Source: "settings\players_panels.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: players_panels;
Source: "settings\service_channel_filter.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: service_channel_filter;
Source: "settings\statistics.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: statistics;
Source: "settings\strategic_camera.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: strategic_camera;
Source: "settings\tank_carousel.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: tank_carousel;
Source: "settings\team_bases_panel.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: team_bases_panel;
Source: "settings\wg_logs.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: wg_logs;
Source: "settings\zoom.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: zoom;
Source: "settings\colors.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: colors;

[InstallDelete]
Type: files; Name: "{app}\{code:PH_Folder_Mods}\armagomen.battleObserver*.wotmod"
Type: files; Name: "{app}\{code:PH_Folder_Mods}\me.poliroid.modslistapi*.wotmod"
Type: files; Name: "{app}\{code:PH_Folder_Mods}\polarfox.vxSettingsApi*.wotmod"
Type: filesandordirs; Name: "{app}\mods\configs\mod_battle_observer\armagomen\*"

[UninstallDelete]
Type: files; Name: "{app}\{code:PH_Folder_Mods}\armagomen.battleObserver*.wotmod"

[Code]

procedure ChangeMainJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\main.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle main.json');
    JSON_SetBool(Handle,'/anti_anonymous', WizardIsComponentSelected('anti_anonymous'));
    JSON_SetBool(Handle,'/auto_crew_training', WizardIsComponentSelected('auto_crew_training'));
    JSON_SetBool(Handle,'/auto_return_crew', WizardIsComponentSelected('auto_return_crew'));
    JSON_SetBool(Handle,'/clear_cache_automatically', WizardIsComponentSelected('clear_cache_automatically'));
    JSON_SetBool(Handle,'/directives_only_from_storage', WizardIsComponentSelected('directives_only_from_storage'));
    JSON_SetBool(Handle,'/disable_score_sound', WizardIsComponentSelected('disable_score_sound'));
    JSON_SetBool(Handle,'/disable_stun_sound', WizardIsComponentSelected('disable_stun_sound'));
    JSON_SetBool(Handle,'/hide_badges', WizardIsComponentSelected('hide_badges'));
    JSON_SetBool(Handle,'/hide_button_counters_on_top_panel', WizardIsComponentSelected('hide_button_counters_on_top_panel'));
    JSON_SetBool(Handle,'/hide_clan_abbrev', WizardIsComponentSelected('hide_clan_abbrev'));
    JSON_SetBool(Handle,'/hide_dog_tags', WizardIsComponentSelected('hide_dog_tags'));
    JSON_SetBool(Handle,'/hide_field_mail', WizardIsComponentSelected('hide_field_mail'));
    JSON_SetBool(Handle,'/hide_hint_panel', WizardIsComponentSelected('hide_hint_panel'));
    JSON_SetBool(Handle,'/hide_main_chat_in_hangar', WizardIsComponentSelected('hide_main_chat_in_hangar'));
    JSON_SetBool(Handle,'/ignore_commanders_voice', WizardIsComponentSelected('ignore_commanders_voice'));
    JSON_SetBool(Handle,'/mute_team_base_sound', WizardIsComponentSelected('mute_team_base_sound'));
    JSON_SetBool(Handle,'/premium_time', WizardIsComponentSelected('premium_time'));
    JSON_SetBool(Handle,'/save_shot', WizardIsComponentSelected('save_shot'));
    JSON_SetBool(Handle,'/show_friends', WizardIsComponentSelected('show_friends'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeClockJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\clock.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle clock.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('clock'));
    JSON_SetBool(Handle,'/hangar/enabled', WizardIsComponentSelected('clock/hangar'));
    JSON_SetBool(Handle,'/battle/enabled', WizardIsComponentSelected('clock/battle'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeHpBarsJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\hp_bars.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle hp_bars.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('hp_bars'));
    JSON_SetBool(Handle,'/showAliveCount', WizardIsComponentSelected('hp_bars/alive_count'));
    if WizardIsComponentSelected('hp_bars/normal') then JSON_SetString(Handle,'/style', 'normal');
    if WizardIsComponentSelected('hp_bars/league') then JSON_SetString(Handle,'/style', 'league');
    JSON_Close(Handle);
  end;
end;

procedure ChangeDebugPanelJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\debug_panel.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle debug_panel.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('debug_panel'));
    if WizardIsComponentSelected('debug_panel/minimal') then JSON_SetString(Handle,'/style', 'minimal');
    if WizardIsComponentSelected('debug_panel/modern') then JSON_SetString(Handle,'/style', 'modern');
    JSON_Close(Handle);
  end;
end;

procedure ChangeDispersioCircleJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\dispersion_circle.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle dispersion_circle.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('dispersion_circle'));
    JSON_SetBool(Handle,'/extraServerLap', WizardIsComponentSelected('dispersion_circle/server'));
    JSON_SetBool(Handle,'/replaceOriginalCircle', WizardIsComponentSelected('dispersion_circle/replace'));
    //JSON_SetDouble(Handle,'/gaw', 1.3);
    //JSON_SetInteger(Handle,'/krya/krya/krya', 42);
    //JSON_SetString(Handle,'/chyk/chyryk', 'aaa');
    JSON_Close(Handle);
    // after JSON_FileClose() the file handle is not valid anymore
  end;
end;

<event('CurStepChanged')>
procedure StepChanged(CurStep: TSetupStep);

begin
  if CurStep = ssPostInstall then
    begin
      ChangeMainJsonValues();
      ChangeClockJsonValues();
      ChangeHpBarsJsonValues();
      ChangeDebugPanelJsonValues();
      ChangeDispersioCircleJsonValues();
    end;
end;


