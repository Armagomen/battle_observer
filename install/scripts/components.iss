#define configs_dir "{app}\mods\configs\mod_battle_observer"
#define mod_source "..\..\output_data"

[Types]
Name: "empty"; Description: {cm:types_empty};
Name: "armagomen"; Description: {cm:types_armagomen};
Name: "saxon_ua"; Description: "SaXon UA";
Name: "user"; Description: {cm:types_user}; Flags: iscustom; 

[Components]
Name: main; Description: MAIN CATEGORY; Flags: disablenouninstallwarning;
Name: main/anti_anonymous; Description: {cm:anti_anonymous}; 
Name: main/auto_crew_training; Description: {cm:auto_crew_training}; Types: armagomen saxon_ua;
Name: main/auto_return_crew; Description: {cm:auto_return_crew}; Types: armagomen saxon_ua;
Name: main/clear_cache_automatically; Description: {cm:clear_cache_automatically}; 
Name: main/disable_score_sound; Description: {cm:disable_score_sound}; Types: armagomen saxon_ua;
Name: main/disable_stun_sound; Description: {cm:disable_stun_sound}; Types: armagomen;
Name: main/directives_only_from_storage; Description: {cm:directives_only_from_storage}; Types: armagomen saxon_ua;
Name: main/excluded_map_slots_notification; Description: {cm:excluded_map_slots_notification};
Name: main/hide_badges; Description: {cm:hide_badges}; Types: armagomen saxon_ua;
Name: main/hide_button_counters_on_top_panel; Description: {cm:hide_button_counters_on_top_panel}; Types: armagomen saxon_ua;
Name: main/hide_clan_abbrev; Description: {cm:hide_clan_abbrev}; Types: armagomen saxon_ua;
Name: main/hide_dog_tags; Description: {cm:hide_dog_tags}; Types: armagomen saxon_ua;
Name: main/hide_field_mail; Description: {cm:hide_field_mail}; Types: armagomen saxon_ua;
Name: main/hide_prestige_hangar_widget; Description: {cm:hide_prestige_hangar_widget};
Name: main/hide_hint_panel; Description: {cm:hide_hint_panel}; Types: armagomen saxon_ua;
Name: main/hide_main_chat_in_hangar; Description: {cm:hide_main_chat_in_hangar}; Types: armagomen saxon_ua;
Name: main/hide_prestige_hangar_widget; Description: {cm:hide_prestige_hangar_widget};
Name: main/hide_prestige_profile_widget; Description: {cm:hide_prestige_profile_widget};
Name: main/hide_prestige_battle_widget; Description: {cm:hide_prestige_battle_widget};
Name: main/ignore_commanders_voice; Description: {cm:ignore_commanders_voice}; Types: armagomen saxon_ua;
Name: main/mute_team_base_sound; Description: {cm:mute_team_base_sound}; Types: armagomen saxon_ua;
Name: main/premium_time; Description: {cm:premium_time}; Types: armagomen saxon_ua;
Name: main/save_shot; Description: {cm:save_shot}; Types: armagomen saxon_ua;
Name: main/show_friends; Description: {cm:show_friends}; Types: armagomen saxon_ua;
Name: main/auto_claim_clan_reward; Description: {cm:auto_claim_clan_reward};
Name: clock; Description: {cm:clock}; Flags: disablenouninstallwarning;
Name: clock/hangar; Description: {cm:clock_hangar}; Types: armagomen;
Name: clock/battle; Description: {cm:clock_battle}; Types: armagomen;
Name: hp_bars; Description: {cm:hp_bars}; Flags: disablenouninstallwarning;
Name: hp_bars/alive_count; Description: {cm:alive_count}; Flags: dontinheritcheck;
Name: hp_bars/normal; Description: {cm:hp_normal}; Flags: exclusive;
Name: hp_bars/league; Description: {cm:hp_league}; Flags: exclusive; Types: armagomen saxon_ua;
Name: debug_panel; Description: {cm:debug_panel}; Flags: disablenouninstallwarning;  
Name: debug_panel/minimal; Description: minimal; Flags: exclusive;
Name: debug_panel/modern; Description: modern; Flags: exclusive; Types: armagomen;
Name: dispersion_circle; Description: {cm:dispersion_circle}; Flags: disablenouninstallwarning;
Name: dispersion_circle/replace; Description: {cm:dispersion_circle_replace}; Types: saxon_ua;
Name: dispersion_circle/server; Description: {cm:dispersion_circle_server}; Types: armagomen;
Name: dispersion_timer; Description: {cm:dispersion_timer}; Flags: disablenouninstallwarning;
Name: sixth_sense; Description: {cm:sixth_sense}; Flags: disablenouninstallwarning;
Name: sixth_sense/playTickSound; Description: {cm:playTickSound}; Types: armagomen saxon_ua;
Name: arcade_camera; Description: {cm:arcade_camera}; Flags: disablenouninstallwarning; Types: armagomen saxon_ua;
Name: strategic_camera; Description: {cm:strategic_camera}; Flags: disablenouninstallwarning; Types: armagomen saxon_ua;
Name: zoom; Description: {cm:zoom}; Flags: disablenouninstallwarning;
Name: zoom/disable_cam_after_shot; Description: {cm:zoom_disable_cam};
Name: zoom/dynamic_zoom; Description: {cm:zoom_dynamic_zoom}; Flags: checkablealone; Types: armagomen; 
Name: zoom/dynamic_zoom/steps_only; Description: {cm:zoom_steps_only}; Flags: dontinheritcheck; Types: armagomen;
Name: zoom/zoomSteps; Description: {cm:zoom_zoomSteps}; Types: armagomen;
Name: armor_calculator; Description: {cm:armor_calculator}; Flags: checkablealone disablenouninstallwarning; Types: armagomen saxon_ua;
Name: armor_calculator/display_on_allies; Description: {cm:armor_calculator_display_on_allies}; Flags: dontinheritcheck;
Name: avg_efficiency_in_hangar; Description: {cm:avg_efficiency_in_hangar}; Flags: disablenouninstallwarning;
Name: avg_efficiency_in_hangar/avg_damage; Description: {cm:avg_efficiency_in_hangar_damage}; Types: armagomen saxon_ua;
Name: avg_efficiency_in_hangar/avg_blocked; Description: {cm:avg_efficiency_in_hangar_blocked}; Types: armagomen saxon_ua;
Name: avg_efficiency_in_hangar/avg_assist; Description: {cm:avg_efficiency_in_hangar_assist}; Types: armagomen saxon_ua;
Name: avg_efficiency_in_hangar/avg_stun; Description: {cm:avg_efficiency_in_hangar_stun}; Types: armagomen saxon_ua;
Name: avg_efficiency_in_hangar/win_rate; Description: {cm:avg_efficiency_in_hangar_win_rate}; Types: armagomen saxon_ua;
Name: avg_efficiency_in_hangar/gun_marks; Description: {cm:avg_efficiency_in_hangar_gun_marks}; Types: armagomen saxon_ua; 
Name: battle_timer; Description: {cm:battle_timer}; Flags: disablenouninstallwarning; Types: armagomen;
Name: distance_to_enemy; Description: {cm:distance_to_enemy}; Flags: disablenouninstallwarning;
Name: effects; Description: {cm:effects}; Flags: disablenouninstallwarning;
Name: effects/noBinoculars; Description: {cm:effects_noBinoculars};
Name: effects/noFlashBang; Description: {cm:effects_noFlashBang}; Types: armagomen saxon_ua;
Name: effects/noShockWave; Description: {cm:effects_noShockWave}; Types: armagomen saxon_ua;
Name: effects/noSniperDynamic; Description: {cm:effects_noSniperDynamic};
Name: flight_time; Description: {cm:flight_time}; Flags: checkablealone disablenouninstallwarning;
Name: flight_time/spgOnly; Description: {cm:flight_time_spg}; Flags: dontinheritcheck;
Name: log_total; Description: {cm:log_total}; Flags: disablenouninstallwarning; Types: armagomen saxon_ua;
Name: log_extended; Description: {cm:log_extended}; Flags: disablenouninstallwarning;
Name: log_extended/top_enabled; Description: {cm:log_extended_top}; Types: armagomen;
Name: log_extended/bottom_enabled; Description: {cm:log_extended_bottom}; Types: armagomen;
Name: log_extended/reverse; Description: {cm:log_extended_reverse};
Name: main_gun; Description: {cm:main_gun}; Flags: checkablealone disablenouninstallwarning; Types: armagomen saxon_ua;
Name: main_gun/progress_bar; Description: {cm:main_gun_progress}; Flags: dontinheritcheck;
Name: minimap; Description: {cm:minimap}; Flags: disablenouninstallwarning;
Name: minimap/permanentMinimapDeath; Description: {cm:minimap_permanent}; 
Name: minimap/real_view_radius; Description: {cm:minimap_radius};  Types: armagomen saxon_ua;
Name: minimap/showDeathNames; Description: {cm:minimap_names}; 
Name: minimap/yaw_limits; Description: {cm:minimap_limits}; Types: armagomen saxon_ua;
Name: minimap/zoom; Description: {cm:minimap_zoom}; Types: armagomen saxon_ua;
Name: own_health; Description: {cm:own_health}; Flags: disablenouninstallwarning;
Name: players_panels; Description: {cm:players_panels}; Flags: disablenouninstallwarning;
Name: players_panels/panels_spotted_fix; Description: {cm:players_panels_spotted}; Types: armagomen saxon_ua;
Name: players_panels/players_bars; Description: {cm:players_panels_bars}; Flags: checkablealone; Types: armagomen saxon_ua; 
Name: players_panels/players_bars/classColor; Description: {cm:players_panels_bars_class}; Flags: dontinheritcheck;
Name: players_panels/players_bars/on_key_pressed; Description: {cm:players_panels_on_key}; Flags: dontinheritcheck;
Name: players_panels/players_damages_enabled; Description: {cm:players_panels_damages}; Types: armagomen saxon_ua; 
Name: service_channel_filter; Description: {cm:service_channel_filter}; Flags: disablenouninstallwarning; 
Name: service_channel_filter/CustomizationForCredits; Description: {cm:service_channel_CustomizationForCredits}; Types: armagomen saxon_ua;
Name: service_channel_filter/CustomizationForGold; Description: {cm:service_channel_CustomizationForGold}; 
Name: service_channel_filter/DismantlingForCredits; Description: {cm:service_channel_DismantlingForCredits}; Types: armagomen saxon_ua;
Name: service_channel_filter/DismantlingForCrystal; Description: {cm:service_channel_DismantlingForCrystal}; 
Name: service_channel_filter/DismantlingForGold; Description: {cm:service_channel_DismantlingForGold}; 
Name: service_channel_filter/GameGreeting; Description: {cm:service_channel_GameGreeting}; Types: armagomen saxon_ua;
Name: service_channel_filter/Information; Description: {cm:service_channel_Information}; Types: armagomen saxon_ua;
Name: service_channel_filter/MultipleSelling; Description: {cm:service_channel_MultipleSelling}; Types: armagomen saxon_ua;
Name: service_channel_filter/PowerLevel; Description: {cm:service_channel_PowerLevel}; Types: armagomen saxon_ua;
Name: service_channel_filter/PurchaseForCredits; Description: {cm:service_channel_PurchaseForCredits}; Types: armagomen saxon_ua;
Name: service_channel_filter/PurchaseForCrystal; Description: {cm:service_channel_PurchaseForCrystal}; 
Name: service_channel_filter/PurchaseForGold; Description: {cm:service_channel_PurchaseForGold}; 
Name: service_channel_filter/Remove; Description: {cm:service_channel_Remove}; 
Name: service_channel_filter/Repair; Description: {cm:service_channel_Repair}; Types: armagomen saxon_ua;
Name: service_channel_filter/Restore; Description: {cm:service_channel_Restore}; 
Name: service_channel_filter/Selling; Description: {cm:service_channel_Selling}; Types: armagomen saxon_ua;
Name: service_channel_filter/autoMaintenance; Description: {cm:service_channel_autoMaintenance}; Types: armagomen saxon_ua;
Name: service_channel_filter/customizationChanged; Description: {cm:service_channel_customizationChanged}; Types: armagomen saxon_ua;
Name: statistics; Description: {cm:statistics}; Flags: disablenouninstallwarning;
Name: statistics/icon_enabled; Description: {cm:statistics_icons}; Types: armagomen saxon_ua;
Name: statistics/statistics_change_vehicle_name_color; Description: {cm:statistics_names_color};  Types: armagomen saxon_ua;
Name: statistics/statistics_enabled; Description: {cm:statistics_enabled}; Types: armagomen saxon_ua;
Name: team_bases_panel; Description: {cm:team_bases_panel}; Flags: disablenouninstallwarning; Types: armagomen saxon_ua;
Name: wg_logs; Description: {cm:wg_logs}; Flags: disablenouninstallwarning;
Name: wg_logs/wg_log_hide_assist; Description: {cm:wg_logs_assist};
Name: wg_logs/wg_log_hide_block; Description: {cm:wg_logs_block};
Name: wg_logs/wg_log_hide_critics; Description: {cm:wg_logs_critics};
Name: wg_logs/wg_log_pos_fix; Description: {cm:wg_logs_pos_fix};

[Files]
Source: "{#mod_source}\armagomen.battleObserver*.wotmod"; DestDir: "{app}\{code:PH_Folder_Mods}"; Flags: ignoreversion;
Source: "{#mod_source}\me.poliroid.modslistapi*.wotmod"; DestDir: "{app}\{code:PH_Folder_Mods}"; Flags: ignoreversion uninsneveruninstall onlyifdoesntexist;
Source: "{#mod_source}\polarfox.vxSettingsApi*.wotmod"; DestDir: "{app}\{code:PH_Folder_Mods}"; Flags: ignoreversion;
Source: "settings\load.json"; DestDir: "{#configs_dir}\"; Flags: ignoreversion;
Source: "settings\default\*"; DestDir: "{#configs_dir}\armagomen_install"; Flags: ignoreversion;

[InstallDelete]
Type: files; Name: "{app}\{code:PH_Folder_Mods}\armagomen.battleObserver*.wotmod"
Type: files; Name: "{app}\{code:PH_Folder_Mods}\me.poliroid.modslistapi*.wotmod"
Type: files; Name: "{app}\{code:PH_Folder_Mods}\polarfox.vxSettingsApi*.wotmod"

[UninstallDelete]
Type: files; Name: "{app}\{code:PH_Folder_Mods}\armagomen.battleObserver*.wotmod"
Type: filesandordirs; Name: "{#configs_dir}\armagomen_install\*"

[Code]
procedure ChangeMainJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\main.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/anti_anonymous', WizardIsComponentSelected('main/anti_anonymous'));
    JSON_SetBool(Handle,'/auto_crew_training', WizardIsComponentSelected('main/auto_crew_training'));
    JSON_SetBool(Handle,'/auto_return_crew', WizardIsComponentSelected('main/auto_return_crew'));
    JSON_SetBool(Handle,'/clear_cache_automatically', WizardIsComponentSelected('main/clear_cache_automatically'));
    JSON_SetBool(Handle,'/directives_only_from_storage', WizardIsComponentSelected('main/directives_only_from_storage'));
    JSON_SetBool(Handle,'/excluded_map_slots_notification', WizardIsComponentSelected('main/excluded_map_slots_notification'));
    JSON_SetBool(Handle,'/disable_score_sound', WizardIsComponentSelected('main/disable_score_sound'));
    JSON_SetBool(Handle,'/disable_stun_sound', WizardIsComponentSelected('main/disable_stun_sound'));
    JSON_SetBool(Handle,'/hide_badges', WizardIsComponentSelected('main/hide_badges'));
    JSON_SetBool(Handle,'/hide_button_counters_on_top_panel', WizardIsComponentSelected('main/hide_button_counters_on_top_panel'));
    JSON_SetBool(Handle,'/hide_clan_abbrev', WizardIsComponentSelected('main/hide_clan_abbrev'));
    JSON_SetBool(Handle,'/hide_dog_tags', WizardIsComponentSelected('main/hide_dog_tags'));
    JSON_SetBool(Handle,'/hide_field_mail', WizardIsComponentSelected('main/hide_field_mail'));
    JSON_SetBool(Handle,'/hide_hint_panel', WizardIsComponentSelected('main/hide_hint_panel'));
    JSON_SetBool(Handle,'/hide_main_chat_in_hangar', WizardIsComponentSelected('main/hide_main_chat_in_hangar'));
    JSON_SetBool(Handle,'/hide_prestige_hangar_widget', WizardIsComponentSelected('main/hide_prestige_hangar_widget'));
    JSON_SetBool(Handle,'/hide_prestige_profile_widget', WizardIsComponentSelected('main/hide_prestige_profile_widget'));
    JSON_SetBool(Handle,'/hide_prestige_battle_widget', WizardIsComponentSelected('main/hide_prestige_battle_widget'));
    JSON_SetBool(Handle,'/ignore_commanders_voice', WizardIsComponentSelected('main/ignore_commanders_voice'));
    JSON_SetBool(Handle,'/mute_team_base_sound', WizardIsComponentSelected('main/mute_team_base_sound'));
    JSON_SetBool(Handle,'/premium_time', WizardIsComponentSelected('main/premium_time'));
    JSON_SetBool(Handle,'/save_shot', WizardIsComponentSelected('main/save_shot'));
    JSON_SetBool(Handle,'/show_friends', WizardIsComponentSelected('main/show_friends'));
    JSON_SetBool(Handle,'/auto_claim_clan_reward', WizardIsComponentSelected('main/auto_claim_clan_reward'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeClockJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\clock.json'), False);
  if Handle <> 0 then
  begin
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
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\hp_bars.json'), False);
  if Handle <> 0 then
  begin
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
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\debug_panel.json'), False);
  if Handle <> 0 then
  begin
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
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\dispersion_circle.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('dispersion_circle'));
    JSON_SetBool(Handle,'/server_aim', WizardIsComponentSelected('dispersion_circle/server'));
    JSON_SetBool(Handle,'/replace', WizardIsComponentSelected('dispersion_circle/replace'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeSixthSenseJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\sixth_sense.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('sixth_sense'));
    JSON_SetBool(Handle,'/playTickSound', WizardIsComponentSelected('sixth_sense/playTickSound'));
    JSON_SetString(Handle,'/default_icon_name', 'logo.png');
    JSON_Close(Handle);
  end;
end;

procedure ChangeArcadeCameraJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\arcade_camera.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('arcade_camera'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeStrategicCameraJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\strategic_camera.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('strategic_camera'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeArmorCalculatorJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\armor_calculator.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('armor_calculator'));
    JSON_SetBool(Handle,'/display_on_allies', WizardIsComponentSelected('armor_calculator/display_on_allies'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeZoomJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\zoom.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('zoom'));
    JSON_SetBool(Handle,'/disable_cam_after_shot', WizardIsComponentSelected('zoom/disable_cam_after_shot'));
    JSON_SetBool(Handle,'/dynamic_zoom/enabled', WizardIsComponentSelected('zoom/dynamic_zoom'));
    JSON_SetBool(Handle,'/dynamic_zoom/steps_only', WizardIsComponentSelected('zoom/dynamic_zoom/steps_only'));
    JSON_SetBool(Handle,'/zoomSteps/enabled', WizardIsComponentSelected('zoom/zoomSteps'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeEffiencyJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\avg_efficiency_in_hangar.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('avg_efficiency_in_hangar'));
    JSON_SetBool(Handle,'/avg_damage', WizardIsComponentSelected('avg_efficiency_in_hangar/avg_damage'));
    JSON_SetBool(Handle,'/avg_blocked', WizardIsComponentSelected('avg_efficiency_in_hangar/avg_blocked'));
    JSON_SetBool(Handle,'/avg_assist', WizardIsComponentSelected('avg_efficiency_in_hangar/avg_assist'));
    JSON_SetBool(Handle,'/avg_stun', WizardIsComponentSelected('avg_efficiency_in_hangar/avg_stun'));
    JSON_SetBool(Handle,'/gun_marks', WizardIsComponentSelected('avg_efficiency_in_hangar/gun_marks'));
    JSON_SetBool(Handle,'/win_rate', WizardIsComponentSelected('avg_efficiency_in_hangar/win_rate'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeEffectsJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\effects.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/noBinoculars', WizardIsComponentSelected('effects/noBinoculars'));
    JSON_SetBool(Handle,'/noFlashBang', WizardIsComponentSelected('effects/noFlashBang'));
    JSON_SetBool(Handle,'/noShockWave', WizardIsComponentSelected('effects/noShockWave'));
    JSON_SetBool(Handle,'/noSniperDynamic', WizardIsComponentSelected('effects/noSniperDynamic'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeExtendedLogsJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\log_extended.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('log_extended'));
    JSON_SetBool(Handle,'/top_enabled', WizardIsComponentSelected('log_extended/top_enabled'));
    JSON_SetBool(Handle,'/bottom_enabled', WizardIsComponentSelected('log_extended/bottom_enabled'));
    JSON_SetBool(Handle,'/reverse', WizardIsComponentSelected('log_extended/reverse'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeMinimapLogsJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\minimap.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('minimap'));
    JSON_SetBool(Handle,'/permanentMinimapDeath', WizardIsComponentSelected('minimap/permanentMinimapDeath'));
    JSON_SetBool(Handle,'/real_view_radius', WizardIsComponentSelected('minimap/real_view_radius'));
    JSON_SetBool(Handle,'/showDeathNames', WizardIsComponentSelected('minimap/showDeathNames'));
    JSON_SetBool(Handle,'/yaw_limits', WizardIsComponentSelected('minimap/yaw_limits'));
    JSON_SetBool(Handle,'/zoom', WizardIsComponentSelected('minimap/zoom'));
    JSON_Close(Handle);
  end;
end;

procedure ChangePlayersPanelsJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\players_panels.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('players_panels'));
    JSON_SetBool(Handle,'/panels_spotted_fix', WizardIsComponentSelected('players_panels/panels_spotted_fix'));
    JSON_SetBool(Handle,'/players_bars_enabled', WizardIsComponentSelected('players_panels/players_bars'));
    JSON_SetBool(Handle,'/players_bars_classColor', WizardIsComponentSelected('players_panels/players_bars/classColor'));
    JSON_SetBool(Handle,'/players_bars_on_key_pressed', WizardIsComponentSelected('players_panels/players_bars/on_key_pressed'));
    JSON_SetBool(Handle,'/players_damages_enabled', WizardIsComponentSelected('players_panels/players_damages_enabled'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeServiceChannelJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\service_channel_filter.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('service_channel_filter'));
    JSON_SetBool(Handle,'/sys_keys/CustomizationForCredits', WizardIsComponentSelected('service_channel_filter/CustomizationForCredits'));
    JSON_SetBool(Handle,'/sys_keys/CustomizationForGold', WizardIsComponentSelected('service_channel_filter/CustomizationForGold'));
    JSON_SetBool(Handle,'/sys_keys/DismantlingForCredits', WizardIsComponentSelected('service_channel_filter/DismantlingForCredits'));
    JSON_SetBool(Handle,'/sys_keys/DismantlingForCrystal', WizardIsComponentSelected('service_channel_filter/DismantlingForCrystal'));
    JSON_SetBool(Handle,'/sys_keys/DismantlingForGold', WizardIsComponentSelected('service_channel_filter/DismantlingForGold'));
    JSON_SetBool(Handle,'/sys_keys/GameGreeting', WizardIsComponentSelected('service_channel_filter/GameGreeting'));
    JSON_SetBool(Handle,'/sys_keys/Information', WizardIsComponentSelected('service_channel_filter/Information'));
    JSON_SetBool(Handle,'/sys_keys/MultipleSelling', WizardIsComponentSelected('service_channel_filter/MultipleSelling'));
    JSON_SetBool(Handle,'/sys_keys/PowerLevel', WizardIsComponentSelected('service_channel_filter/PowerLevel'));
    JSON_SetBool(Handle,'/sys_keys/PurchaseForCredits', WizardIsComponentSelected('service_channel_filter/PurchaseForCredits'));
    JSON_SetBool(Handle,'/sys_keys/PurchaseForCrystal', WizardIsComponentSelected('service_channel_filter/PurchaseForCrystal'));
    JSON_SetBool(Handle,'/sys_keys/PurchaseForGold', WizardIsComponentSelected('service_channel_filter/PurchaseForGold'));
    JSON_SetBool(Handle,'/sys_keys/Remove', WizardIsComponentSelected('service_channel_filter/Remove'));
    JSON_SetBool(Handle,'/sys_keys/Repair', WizardIsComponentSelected('service_channel_filter/Repair'));
    JSON_SetBool(Handle,'/sys_keys/Restore', WizardIsComponentSelected('service_channel_filter/Restore'));
    JSON_SetBool(Handle,'/sys_keys/Selling', WizardIsComponentSelected('service_channel_filter/Selling'));
    JSON_SetBool(Handle,'/sys_keys/autoMaintenance', WizardIsComponentSelected('service_channel_filter/autoMaintenance'));
    JSON_SetBool(Handle,'/sys_keys/customizationChanged', WizardIsComponentSelected('service_channel_filter/customizationChanged'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeStatisticsJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\statistics.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('statistics'));
    JSON_SetBool(Handle,'/icon_enabled', WizardIsComponentSelected('statistics/icon_enabled'));
    JSON_SetBool(Handle,'/statistics_change_vehicle_name_color', WizardIsComponentSelected('statistics/statistics_change_vehicle_name_color'));
    JSON_SetBool(Handle,'/statistics_enabled', WizardIsComponentSelected('statistics/statistics_enabled'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeWGLogsJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\wg_logs.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('wg_logs'));
    JSON_SetBool(Handle,'/wg_log_hide_assist', WizardIsComponentSelected('wg_logs/wg_log_hide_assist'));
    JSON_SetBool(Handle,'/wg_log_hide_block', WizardIsComponentSelected('wg_logs/wg_log_hide_block'));
    JSON_SetBool(Handle,'/wg_log_hide_critics', WizardIsComponentSelected('wg_logs/wg_log_hide_critics'));
    JSON_SetBool(Handle,'/wg_log_pos_fix', WizardIsComponentSelected('wg_logs/wg_log_pos_fix'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeFlightTimeJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\flight_time.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('flight_time'));
    JSON_SetBool(Handle,'/spgOnly', WizardIsComponentSelected('flight_time/spgOnly'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeDistanceToEnemyJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\distance_to_enemy.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('distance_to_enemy'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeBattleTimerJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\battle_timer.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('battle_timer'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeLogTotalJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\log_total.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('log_total'));
    if not WizardIsComponentSelected('hp_bars') then JSON_SetInteger(Handle,'/settings/x', -360);
    JSON_Close(Handle);
  end;
end;

procedure ChangeMainGunJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\main_gun.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('main_gun'));
    JSON_SetBool(Handle,'/progress_bar', WizardIsComponentSelected('main_gun/progress_bar'));
    if not WizardIsComponentSelected('hp_bars') then JSON_SetInteger(Handle,'/x', 360);
    JSON_Close(Handle);
  end;
end;

procedure ChangeOwnHealthJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\own_health.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('own_health'));
    JSON_Close(Handle);
  end;
end;



procedure ChangeTeamBasesJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\team_bases_panel.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('team_bases_panel'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeDispersionTimerJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen_install\dispersion_timer.json'), False);
  if Handle <> 0 then
  begin
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('dispersion_timer'));
    JSON_Close(Handle);
  end;
end;


//JSON_SetDouble(Handle,'/gaw', 1.3);
//JSON_SetInteger(Handle,'/krya/krya/krya', 42);
//JSON_SetString(Handle,'/chyk/chyryk', 'aaa');
<event('CurStepChanged')>
procedure StepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
    begin
      ChangeArcadeCameraJsonValues();
      ChangeArmorCalculatorJsonValues();
      ChangeBattleTimerJsonValues();
      ChangeClockJsonValues();
      ChangeDebugPanelJsonValues();
      ChangeDispersioCircleJsonValues();
      ChangeDispersionTimerJsonValues();
      ChangeDistanceToEnemyJsonValues();
      ChangeEffectsJsonValues();
      ChangeEffiencyJsonValues();
      ChangeExtendedLogsJsonValues();
      ChangeFlightTimeJsonValues();
      ChangeHpBarsJsonValues();
      ChangeLogTotalJsonValues();
      ChangeMainGunJsonValues();
      ChangeMainJsonValues();
      ChangeMinimapLogsJsonValues();
      ChangeOwnHealthJsonValues();
      ChangePlayersPanelsJsonValues();
      ChangeServiceChannelJsonValues();
      ChangeSixthSenseJsonValues();
      ChangeStatisticsJsonValues();
      ChangeStrategicCameraJsonValues();
      ChangeTeamBasesJsonValues();
      ChangeWGLogsJsonValues();
      ChangeZoomJsonValues();
    end;
end;


