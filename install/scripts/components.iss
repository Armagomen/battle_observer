#define configs_dir "{app}\mods\configs\mod_battle_observer"
#define mod_source "..\..\output_data"

[Types]
Name: "armagomen"; Description: {cm:types_armagomen};
Name: "user"; Description: {cm:types_user}; Flags: iscustom; 

[Components]
// main.json
Name: main; Description: MAIN CATEGORY; Flags: disablenouninstallwarning;
Name: main/anti_anonymous; Description: {cm:anti_anonymous}; Flags: disablenouninstallwarning
Name: main/auto_crew_training; Description: {cm:auto_crew_training}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main/auto_return_crew; Description: {cm:auto_return_crew}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main/clear_cache_automatically; Description: {cm:clear_cache_automatically}; Flags: disablenouninstallwarning;
Name: main/disable_score_sound; Description: {cm:disable_score_sound}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main/disable_stun_sound; Description: {cm:disable_stun_sound}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main/directives_only_from_storage; Description: {cm:directives_only_from_storage}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main/hide_badges; Description: {cm:hide_badges}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main/hide_button_counters_on_top_panel; Description: {cm:hide_button_counters_on_top_panel}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main/hide_clan_abbrev; Description: {cm:hide_clan_abbrev}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main/hide_dog_tags; Description: {cm:hide_dog_tags}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main/hide_field_mail; Description: {cm:hide_field_mail}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main/hide_hint_panel; Description: {cm:hide_hint_panel}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main/hide_main_chat_in_hangar; Description: {cm:hide_main_chat_in_hangar}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main/ignore_commanders_voice; Description: {cm:ignore_commanders_voice}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main/mute_team_base_sound; Description: {cm:mute_team_base_sound}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main/premium_time; Description: {cm:premium_time}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main/save_shot; Description: {cm:save_shot}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main/show_friends; Description: {cm:show_friends}; Flags: disablenouninstallwarning; Types: "armagomen";

//clock
Name: clock; Description: {cm:clock}; Flags: disablenouninstallwarning; 
Name: clock/hangar; Description: {cm:clock_hangar}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: clock/battle; Description: {cm:clock_battle}; Flags: disablenouninstallwarning; Types: "armagomen";

//hp_bars
Name: hp_bars; Description: {cm:hp_bars}; Flags: disablenouninstallwarning;
Name: hp_bars/alive_count; Description: {cm:alive_count}; Flags: dontinheritcheck disablenouninstallwarning;
Name: hp_bars/normal; Description: {cm:hp_normal}; Flags: exclusive disablenouninstallwarning;
Name: hp_bars/league; Description: {cm:hp_league}; Flags: exclusive disablenouninstallwarning; Types: "armagomen";

//debug_panel
Name: debug_panel; Description: {cm:debug_panel}; Flags: disablenouninstallwarning; 
Name: debug_panel/minimal; Description: minimal; Flags: exclusive disablenouninstallwarning;
Name: debug_panel/modern; Description: modern; Flags: exclusive disablenouninstallwarning; Types: "armagomen";

//dispersion_circle
Name: dispersion_circle; Description: {cm:dispersion_circle}; Flags: disablenouninstallwarning;
Name: dispersion_circle/replace; Description: {cm:dispersion_circle_replace}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: dispersion_circle/server; Description: {cm:dispersion_circle_server}; Flags: disablenouninstallwarning;
Name: dispersion_timer; Description: {cm:dispersion_timer}; Types: "armagomen"; Flags: disablenouninstallwarning;

//sixth_sense
Name: sixth_sense; Description: {cm:sixth_sense}; Flags: disablenouninstallwarning;
Name: sixth_sense/playTickSound; Description: {cm:playTickSound}; Types: "armagomen"; Flags: disablenouninstallwarning;
Name: sixth_sense/bavovnatko; Description: {cm:bavovnatko}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/boris; Description: {cm:boris}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/dog_patron; Description: {cm:dog_patron}; Flags: exclusive disablenouninstallwarning; Types: "armagomen";
Name: sixth_sense/eye_of_sauron; Description: {cm:eye_of_sauron}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/feygin_arestovych; Description: {cm:feygin_arestovych}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/flash; Description: {cm:flash}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/grogu; Description: {cm:grogu}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/himars; Description: {cm:himars}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/kv_dart; Description: {cm:kv_dart}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/lamp_1; Description: {cm:lamp_1}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/lamp_2; Description: {cm:lamp_2}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/lamp_3; Description: {cm:lamp_3}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/luka; Description: {cm:luka}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/medal_ship_censoured; Description: {cm:medal_ship_censoured}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/moscow_ship; Description: {cm:moscow_ship}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/moscow_ship_2; Description: {cm:moscow_ship_2}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/potato; Description: {cm:potato}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/red_bloody_hand; Description: {cm:red_bloody_hand}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/rick_bender; Description: {cm:rick_bender}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/rick_morty; Description: {cm:rick_morty}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/rick_morty_2; Description: {cm:rick_morty_2}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/rick_morty_fu; Description: {cm:rick_morty_fu}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/rick_morty_portal; Description: {cm:rick_morty_portal}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/skull; Description: {cm:skull}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/spark; Description: {cm:spark}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/sun_scream; Description: {cm:sun_scream}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/supernova; Description: {cm:supernova}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/ua_armed_forces; Description: {cm:ua_armed_forces}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/ua_flag; Description: {cm:ua_flag}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/ua_flag_herb; Description: {cm:ua_flag_herb}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/ua_gur; Description: {cm:ua_gur}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/ua_herb; Description: {cm:ua_herb}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/water_fire; Description: {cm:water_fire}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/what_again; Description: {cm:what_again}; Flags: exclusive disablenouninstallwarning;
Name: sixth_sense/zelensky; Description: {cm:zelensky}; Flags: exclusive disablenouninstallwarning;


Name: arcade_camera; Description: {cm:arcade_camera}; Types: "armagomen"; Flags: disablenouninstallwarning;
Name: armor_calculator; Description: {cm:armor_calculator}; Types: "armagomen"; Flags: disablenouninstallwarning;
Name: avg_efficiency_in_hangar; Description: {cm:avg_efficiency_in_hangar}; Types: "armagomen"; Flags: disablenouninstallwarning;
Name: battle_timer; Description: {cm:battle_timer}; Types: "armagomen"; Flags: disablenouninstallwarning;
Name: distance_to_enemy; Description: {cm:distance_to_enemy}; Flags: disablenouninstallwarning;
Name: effects; Description: {cm:effects}; Types: "armagomen user"; Flags: disablenouninstallwarning;
Name: flight_time; Description: {cm:flight_time}; Types: "armagomen"; Flags: disablenouninstallwarning;
Name: log_extended; Description: {cm:log_extended}; Types: "armagomen"; Flags: disablenouninstallwarning;
Name: log_total; Description: {cm:log_total}; Types: "armagomen"; Flags: disablenouninstallwarning;
Name: main_gun; Description: {cm:main_gun}; Types: "armagomen"; Flags: disablenouninstallwarning;
Name: minimap; Description: {cm:minimap}; Types: "armagomen"; Flags: disablenouninstallwarning;
Name: own_health; Description: {cm:own_health}; Flags: disablenouninstallwarning;
Name: players_panels; Description: {cm:players_panels}; Types: "armagomen"; Flags: disablenouninstallwarning;
Name: service_channel_filter; Description: {cm:service_channel_filter}; Types: "armagomen"; Flags: disablenouninstallwarning;
Name: statistics; Description: {cm:statistics}; Types: "armagomen"; Flags: disablenouninstallwarning;
Name: strategic_camera; Description: {cm:strategic_camera}; Types: "armagomen"; Flags: disablenouninstallwarning;
Name: tank_carousel; Description: {cm:tank_carousel}; Flags: disablenouninstallwarning;
Name: team_bases_panel; Description: {cm:team_bases_panel}; Types: "armagomen"; Flags: disablenouninstallwarning;
Name: wg_logs; Description: {cm:wg_logs}; Flags: disablenouninstallwarning;
Name: zoom; Description: {cm:zoom}; Types: "armagomen"; Flags: disablenouninstallwarning;
Name: colors; Description: {cm:colors}; Flags: fixed disablenouninstallwarning; Types: "armagomen user";

[Files]
Source: "{#mod_source}\*"; DestDir: "{app}\{code:PH_Folder_Mods}"; Flags: ignoreversion;
Source: "settings\load.json"; DestDir: "{#configs_dir}"; Flags: ignoreversion;
Source: "settings\main.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion;
Source: "settings\hp_bars.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion;
Source: "settings\clock.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion;
Source: "settings\debug_panel.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion;
Source: "settings\dispersion_circle.json"; DestDir: "{#configs_dir}\armagomen";  Flags: ignoreversion;
Source: "settings\dispersion_timer.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion;
Source: "settings\sixth_sense.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion;

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
Type: filesandordirs; Name: "{app}\mods\configs\mod_battle_observer\armagomen\*"

[Code]

procedure ChangeMainJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\main.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle main.json');
    JSON_SetBool(Handle,'/anti_anonymous', WizardIsComponentSelected('main/anti_anonymous'));
    JSON_SetBool(Handle,'/auto_crew_training', WizardIsComponentSelected('main/auto_crew_training'));
    JSON_SetBool(Handle,'/auto_return_crew', WizardIsComponentSelected('main/auto_return_crew'));
    JSON_SetBool(Handle,'/clear_cache_automatically', WizardIsComponentSelected('main/clear_cache_automatically'));
    JSON_SetBool(Handle,'/directives_only_from_storage', WizardIsComponentSelected('main/directives_only_from_storage'));
    JSON_SetBool(Handle,'/disable_score_sound', WizardIsComponentSelected('main/disable_score_sound'));
    JSON_SetBool(Handle,'/disable_stun_sound', WizardIsComponentSelected('main/disable_stun_sound'));
    JSON_SetBool(Handle,'/hide_badges', WizardIsComponentSelected('main/hide_badges'));
    JSON_SetBool(Handle,'/hide_button_counters_on_top_panel', WizardIsComponentSelected('main/hide_button_counters_on_top_panel'));
    JSON_SetBool(Handle,'/hide_clan_abbrev', WizardIsComponentSelected('main/hide_clan_abbrev'));
    JSON_SetBool(Handle,'/hide_dog_tags', WizardIsComponentSelected('main/hide_dog_tags'));
    JSON_SetBool(Handle,'/hide_field_mail', WizardIsComponentSelected('main/hide_field_mail'));
    JSON_SetBool(Handle,'/hide_hint_panel', WizardIsComponentSelected('main/hide_hint_panel'));
    JSON_SetBool(Handle,'/hide_main_chat_in_hangar', WizardIsComponentSelected('main/hide_main_chat_in_hangar'));
    JSON_SetBool(Handle,'/ignore_commanders_voice', WizardIsComponentSelected('main/ignore_commanders_voice'));
    JSON_SetBool(Handle,'/mute_team_base_sound', WizardIsComponentSelected('main/mute_team_base_sound'));
    JSON_SetBool(Handle,'/premium_time', WizardIsComponentSelected('main/premium_time'));
    JSON_SetBool(Handle,'/save_shot', WizardIsComponentSelected('main/save_shot'));
    JSON_SetBool(Handle,'/show_friends', WizardIsComponentSelected('main/show_friends'));
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

procedure ChangeSixthSenseJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\sixth_sense.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle sixth_sense.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('sixth_sense'));
    JSON_SetBool(Handle,'/playTickSound', WizardIsComponentSelected('sixth_sense/playTickSound'));
    if WizardIsComponentSelected('sixth_sense/bavovnatko') then JSON_SetString(Handle,'/default_icon_name', 'bavovnatko.png');
    if WizardIsComponentSelected('sixth_sense/boris') then JSON_SetString(Handle,'/default_icon_name', 'boris.png');
    if WizardIsComponentSelected('sixth_sense/dog_patron') then JSON_SetString(Handle,'/default_icon_name', 'dog_patron.png');
    if WizardIsComponentSelected('sixth_sense/eye_of_sauron') then JSON_SetString(Handle,'/default_icon_name', 'eye_of_sauron.png');
    if WizardIsComponentSelected('sixth_sense/feygin_arestovych') then JSON_SetString(Handle,'/default_icon_name', 'feygin_arestovych.png');
    if WizardIsComponentSelected('sixth_sense/flash') then JSON_SetString(Handle,'/default_icon_name', 'flash.png');
    if WizardIsComponentSelected('sixth_sense/grogu') then JSON_SetString(Handle,'/default_icon_name', 'grogu.png');
    if WizardIsComponentSelected('sixth_sense/himars') then JSON_SetString(Handle,'/default_icon_name', 'himars.png');
    if WizardIsComponentSelected('sixth_sense/kv_dart') then JSON_SetString(Handle,'/default_icon_name', 'kv_dart.png');
    if WizardIsComponentSelected('sixth_sense/lamp_1') then JSON_SetString(Handle,'/default_icon_name', 'lamp_1.png');
    if WizardIsComponentSelected('sixth_sense/lamp_2') then JSON_SetString(Handle,'/default_icon_name', 'lamp_2.png');
    if WizardIsComponentSelected('sixth_sense/lamp_3') then JSON_SetString(Handle,'/default_icon_name', 'lamp_3.png');
    if WizardIsComponentSelected('sixth_sense/luka') then JSON_SetString(Handle,'/default_icon_name', 'luka.png');
    if WizardIsComponentSelected('sixth_sense/medal_ship_censoured') then JSON_SetString(Handle,'/default_icon_name', 'medal_ship_censoured.png');
    if WizardIsComponentSelected('sixth_sense/moscow_ship') then JSON_SetString(Handle,'/default_icon_name', 'moscow_ship.png');
    if WizardIsComponentSelected('sixth_sense/moscow_ship_2') then JSON_SetString(Handle,'/default_icon_name', 'moscow_ship_2.png');
    if WizardIsComponentSelected('sixth_sense/potato') then JSON_SetString(Handle,'/default_icon_name', 'potato.png');
    if WizardIsComponentSelected('sixth_sense/red_bloody_hand') then JSON_SetString(Handle,'/default_icon_name', 'red_bloody_hand.png');
    if WizardIsComponentSelected('sixth_sense/rick_bender') then JSON_SetString(Handle,'/default_icon_name', 'rick_bender.png');
    if WizardIsComponentSelected('sixth_sense/rick_morty') then JSON_SetString(Handle,'/default_icon_name', 'rick_morty.png');
    if WizardIsComponentSelected('sixth_sense/rick_morty_2') then JSON_SetString(Handle,'/default_icon_name', 'rick_morty_2.png');
    if WizardIsComponentSelected('sixth_sense/rick_morty_fu') then JSON_SetString(Handle,'/default_icon_name', 'rick_morty_fu.png');
    if WizardIsComponentSelected('sixth_sense/rick_morty_portal') then JSON_SetString(Handle,'/default_icon_name', 'rick_morty_portal.png');
    if WizardIsComponentSelected('sixth_sense/skull') then JSON_SetString(Handle,'/default_icon_name', 'skull.png');
    if WizardIsComponentSelected('sixth_sense/spark') then JSON_SetString(Handle,'/default_icon_name', 'spark.png');
    if WizardIsComponentSelected('sixth_sense/sun_scream') then JSON_SetString(Handle,'/default_icon_name', 'sun_scream.png');
    if WizardIsComponentSelected('sixth_sense/supernova') then JSON_SetString(Handle,'/default_icon_name', 'supernova.png');
    if WizardIsComponentSelected('sixth_sense/ua_armed_forces') then JSON_SetString(Handle,'/default_icon_name', 'ua_armed_forces.png');
    if WizardIsComponentSelected('sixth_sense/ua_flag') then JSON_SetString(Handle,'/default_icon_name', 'ua_flag.png');
    if WizardIsComponentSelected('sixth_sense/ua_flag_herb') then JSON_SetString(Handle,'/default_icon_name', 'ua_flag_herb.png');
    if WizardIsComponentSelected('sixth_sense/ua_gur') then JSON_SetString(Handle,'/default_icon_name', 'ua_gur.png');
    if WizardIsComponentSelected('sixth_sense/ua_herb') then JSON_SetString(Handle,'/default_icon_name', 'ua_herb.png');
    if WizardIsComponentSelected('sixth_sense/water_fire') then JSON_SetString(Handle,'/default_icon_name', 'water_fire.png');
    if WizardIsComponentSelected('sixth_sense/what_again') then JSON_SetString(Handle,'/default_icon_name', 'what_again.png');
    if WizardIsComponentSelected('sixth_sense/zelensky') then JSON_SetString(Handle,'/default_icon_name', 'zelensky.png');
    JSON_Close(Handle);
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
      ChangeSixthSenseJsonValues();
    end;
end;


