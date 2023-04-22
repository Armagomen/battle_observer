#define configs_dir "{app}\mods\configs\mod_battle_observer"
#define mod_source "..\..\output_data"

[Types]
Name: "armagomen"; Description: {cm:types_armagomen};
Name: "user"; Description: {cm:types_user}; Flags: iscustom; 

[Components]
Name: main; Description: MAIN CATEGORY;
Name: main/anti_anonymous; Description: {cm:anti_anonymous}; Flags: disablenouninstallwarning;
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
Name: clock; Description: {cm:clock}; Flags: disablenouninstallwarning;
Name: clock/hangar; Description: {cm:clock_hangar}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: clock/battle; Description: {cm:clock_battle}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: hp_bars; Description: {cm:hp_bars}; Flags: disablenouninstallwarning;
Name: hp_bars/alive_count; Description: {cm:alive_count}; Flags: disablenouninstallwarning dontinheritcheck;
Name: hp_bars/normal; Description: {cm:hp_normal}; Flags: disablenouninstallwarning exclusive;
Name: hp_bars/league; Description: {cm:hp_league}; Flags: disablenouninstallwarning exclusive; Types: "armagomen";
Name: debug_panel; Description: {cm:debug_panel}; Flags: disablenouninstallwarning;  
Name: debug_panel/minimal; Description: minimal; Flags: exclusive;
Name: debug_panel/modern; Description: modern; Flags: exclusive; Types: "armagomen";
Name: dispersion_circle; Description: {cm:dispersion_circle}; Flags: disablenouninstallwarning;
Name: dispersion_circle/replace; Description: {cm:dispersion_circle_replace}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: dispersion_circle/server; Description: {cm:dispersion_circle_server}; Flags: disablenouninstallwarning;
Name: dispersion_timer; Description: {cm:dispersion_timer}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: sixth_sense; Description: {cm:sixth_sense}; Flags: disablenouninstallwarning;
Name: sixth_sense/playTickSound; Description: {cm:playTickSound}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: sixth_sense/bavovnatko; Description: {cm:bavovnatko}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/boris; Description: {cm:boris}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/dog_patron; Description: {cm:dog_patron}; Flags: disablenouninstallwarning exclusive; Types: "armagomen";
Name: sixth_sense/eye_of_sauron; Description: {cm:eye_of_sauron}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/feygin_arestovych; Description: {cm:feygin_arestovych}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/flash; Description: {cm:flash}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/grogu; Description: {cm:grogu}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/himars; Description: {cm:himars}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/kv_dart; Description: {cm:kv_dart}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/lamp_1; Description: {cm:lamp_1}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/lamp_2; Description: {cm:lamp_2}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/lamp_3; Description: {cm:lamp_3}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/luka; Description: {cm:luka}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/medal_ship_censoured; Description: {cm:medal_ship_censoured}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/moscow_ship; Description: {cm:moscow_ship}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/moscow_ship_2; Description: {cm:moscow_ship_2}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/potato; Description: {cm:potato}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/red_bloody_hand; Description: {cm:red_bloody_hand}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/rick_bender; Description: {cm:rick_bender}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/rick_morty; Description: {cm:rick_morty}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/rick_morty_2; Description: {cm:rick_morty_2}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/rick_morty_fu; Description: {cm:rick_morty_fu}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/rick_morty_portal; Description: {cm:rick_morty_portal}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/skull; Description: {cm:skull}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/spark; Description: {cm:spark}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/sun_scream; Description: {cm:sun_scream}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/supernova; Description: {cm:supernova}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/ua_armed_forces; Description: {cm:ua_armed_forces}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/ua_flag; Description: {cm:ua_flag}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/ua_flag_herb; Description: {cm:ua_flag_herb}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/ua_gur; Description: {cm:ua_gur}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/ua_herb; Description: {cm:ua_herb}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/water_fire; Description: {cm:water_fire}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/what_again; Description: {cm:what_again}; Flags: disablenouninstallwarning exclusive;
Name: sixth_sense/zelensky; Description: {cm:zelensky}; Flags: disablenouninstallwarning exclusive;
Name: arcade_camera; Description: {cm:arcade_camera}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: strategic_camera; Description: {cm:strategic_camera}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: zoom; Description: {cm:zoom}; Flags: disablenouninstallwarning;
Name: zoom/disable_cam_after_shot; Description: {cm:zoom_disable_cam}; Flags: disablenouninstallwarning;
Name: zoom/dynamic_zoom; Description: {cm:zoom_dynamic_zoom}; Flags: checkablealone disablenouninstallwarning; Types: "armagomen"; 
Name: zoom/dynamic_zoom/steps_only; Description: {cm:zoom_steps_only}; Flags: disablenouninstallwarning dontinheritcheck;
Name: zoom/zoomSteps; Description: {cm:zoom_zoomSteps}; Flags: disablenouninstallwarning;
Name: armor_calculator; Description: {cm:armor_calculator}; Flags: checkablealone disablenouninstallwarning; Types: "armagomen";
Name: armor_calculator/display_on_allies; Description: {cm:armor_calculator_display_on_allies}; Flags: disablenouninstallwarning dontinheritcheck;
Name: avg_efficiency_in_hangar; Description: {cm:avg_efficiency_in_hangar}; Flags: disablenouninstallwarning;
Name: avg_efficiency_in_hangar/avg_damage; Description: {cm:avg_efficiency_in_hangar_damage}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: avg_efficiency_in_hangar/avg_blocked; Description: {cm:avg_efficiency_in_hangar_blocked}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: avg_efficiency_in_hangar/avg_assist; Description: {cm:avg_efficiency_in_hangar_assist}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: avg_efficiency_in_hangar/avg_stun; Description: {cm:avg_efficiency_in_hangar_stun}; Flags: disablenouninstallwarning; Types: "armagomen"; 
Name: avg_efficiency_in_hangar/gun_marks; Description: {cm:avg_efficiency_in_hangar_gun_marks}; Flags: disablenouninstallwarning; Types: "armagomen"; 
Name: battle_timer; Description: {cm:battle_timer}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: distance_to_enemy; Description: {cm:distance_to_enemy}; Flags: disablenouninstallwarning;
Name: effects; Description: {cm:effects}; Flags: disablenouninstallwarning;
Name: effects/noBinoculars; Description: {cm:effects_noBinoculars}; Flags: disablenouninstallwarning;
Name: effects/noFlashBang; Description: {cm:effects_noFlashBang}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: effects/noShockWave; Description: {cm:effects_noShockWave}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: effects/noSniperDynamic; Description: {cm:effects_noSniperDynamic}; Flags: disablenouninstallwarning;
Name: flight_time; Description: {cm:flight_time}; Flags: checkablealone disablenouninstallwarning; Types: "armagomen";
Name: flight_time/spgOnly; Description: {cm:flight_time_spg}; Flags: disablenouninstallwarning dontinheritcheck;
Name: log_total; Description: {cm:log_total}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: log_extended; Description: {cm:log_extended}; Flags: disablenouninstallwarning;
Name: log_extended/top_enabled; Description: {cm:log_extended_top}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: log_extended/bottom_enabled; Description: {cm:log_extended_bottom}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: log_extended/reverse; Description: {cm:log_extended_reverse}; Flags: disablenouninstallwarning;
Name: main_gun; Description: {cm:main_gun}; Flags: checkablealone disablenouninstallwarning; Types: "armagomen";
Name: main_gun/progress_bar; Description: {cm:main_gun_progress}; Flags: disablenouninstallwarning dontinheritcheck;
Name: minimap; Description: {cm:minimap}; Flags: disablenouninstallwarning;
Name: minimap/permanentMinimapDeath; Description: {cm:minimap_permanent}; Flags: disablenouninstallwarning;
Name: minimap/real_view_radius; Description: {cm:minimap_radius}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: minimap/showDeathNames; Description: {cm:minimap_names}; Flags: disablenouninstallwarning;
Name: minimap/yaw_limits; Description: {cm:minimap_limits}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: minimap/zoom; Description: {cm:minimap_zoom}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: own_health; Description: {cm:own_health}; Flags: disablenouninstallwarning;
Name: players_panels; Description: {cm:players_panels}; Flags: disablenouninstallwarning;
Name: players_panels/panels_spotted_fix; Description: {cm:players_panels_spotted}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: players_panels/players_bars; Description: {cm:players_panels_bars}; Flags: disablenouninstallwarning checkablealone; Types: "armagomen"; 
Name: players_panels/players_bars/classColor; Description: {cm:players_panels_bars_class}; Flags: disablenouninstallwarning dontinheritcheck;
Name: players_panels/players_bars/on_key_pressed; Description: {cm:players_panels_on_key}; Flags: disablenouninstallwarning dontinheritcheck;
Name: players_panels/players_damages_enabled; Description: {cm:players_panels_damages}; Flags: disablenouninstallwarning; Types: "armagomen"; 
Name: service_channel_filter; Description: {cm:service_channel_filter}; Flags: disablenouninstallwarning;
Name: service_channel_filter/CustomizationForCredits; Description: {cm:service_channel_CustomizationForCredits}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: service_channel_filter/CustomizationForGold; Description: {cm:service_channel_CustomizationForGold}; Flags: disablenouninstallwarning;
Name: service_channel_filter/DismantlingForCredits; Description: {cm:service_channel_DismantlingForCredits}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: service_channel_filter/DismantlingForCrystal; Description: {cm:service_channel_DismantlingForCrystal}; Flags: disablenouninstallwarning;
Name: service_channel_filter/DismantlingForGold; Description: {cm:service_channel_DismantlingForGold}; Flags: disablenouninstallwarning;
Name: service_channel_filter/GameGreeting; Description: {cm:service_channel_GameGreeting}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: service_channel_filter/Information; Description: {cm:service_channel_Information}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: service_channel_filter/MultipleSelling; Description: {cm:service_channel_MultipleSelling}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: service_channel_filter/PowerLevel; Description: {cm:service_channel_PowerLevel}; Flags: disablenouninstallwarning;Types: "armagomen";
Name: service_channel_filter/PurchaseForCredits; Description: {cm:service_channel_PurchaseForCredits}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: service_channel_filter/PurchaseForCrystal; Description: {cm:service_channel_PurchaseForCrystal}; Flags: disablenouninstallwarning;
Name: service_channel_filter/PurchaseForGold; Description: {cm:service_channel_PurchaseForGold}; Flags: disablenouninstallwarning;
Name: service_channel_filter/Remove; Description: {cm:service_channel_Remove}; Flags: disablenouninstallwarning;
Name: service_channel_filter/Repair; Description: {cm:service_channel_Repair}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: service_channel_filter/Restore; Description: {cm:service_channel_Restore}; Flags: disablenouninstallwarning;
Name: service_channel_filter/Selling; Description: {cm:service_channel_Selling}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: service_channel_filter/autoMaintenance; Description: {cm:service_channel_autoMaintenance}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: service_channel_filter/customizationChanged; Description: {cm:service_channel_customizationChanged}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: statistics; Description: {cm:statistics}; Flags: disablenouninstallwarning;
Name: statistics/icon_enabled; Description: {cm:statistics_icons}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: statistics/statistics_change_vehicle_name_color; Description: {cm:statistics_names_color}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: statistics/statistics_enabled; Description: {cm:statistics_enabled}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: tank_carousel; Description: {cm:tank_carousel}; Flags: disablenouninstallwarning;
Name: tank_carousel/smallDoubleCarousel; Description: {cm:tank_carousel_small}; Flags: disablenouninstallwarning dontinheritcheck;
Name: tank_carousel/3; Description: {cm:tank_carousel_3}; Flags: disablenouninstallwarning exclusive;
Name: tank_carousel/4; Description: {cm:tank_carousel_4}; Flags: disablenouninstallwarning exclusive;
Name: team_bases_panel; Description: {cm:team_bases_panel}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: wg_logs; Description: {cm:wg_logs}; Flags: disablenouninstallwarning;
Name: wg_logs/wg_log_hide_assist; Description: {cm:wg_logs_assist}; Flags: disablenouninstallwarning;
Name: wg_logs/wg_log_hide_block; Description: {cm:wg_logs_block}; Flags: disablenouninstallwarning;
Name: wg_logs/wg_log_hide_critics; Description: {cm:wg_logs_critics}; Flags: disablenouninstallwarning;
Name: wg_logs/wg_log_pos_fix; Description: {cm:wg_logs_pos_fix}; Flags: disablenouninstallwarning;


[Files]
Source: "{#mod_source}\*"; DestDir: "{app}\{code:PH_Folder_Mods}"; Flags: ignoreversion;
Source: "settings\load.json"; DestDir: "{#configs_dir}\"; Flags: ignoreversion;
Source: "settings\default\*"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion;

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
    JSON_Close(Handle);
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

procedure ChangeArcadeCameraJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\arcade_camera.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle arcade_camera.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('arcade_camera'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeStrategicCameraJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\strategic_camera.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle strategic_camera.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('strategic_camera'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeArmorCalculatorJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\armor_calculator.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle armor_calculator.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('armor_calculator'));
    JSON_SetBool(Handle,'/display_on_allies', WizardIsComponentSelected('armor_calculator/display_on_allies'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeZoomJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\zoom.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle zoom.json');
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
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\avg_efficiency_in_hangar.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle avg_efficiency_in_hangar.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('avg_efficiency_in_hangar'));
    JSON_SetBool(Handle,'/avg_damage', WizardIsComponentSelected('avg_efficiency_in_hangar/avg_damage'));
    JSON_SetBool(Handle,'/avg_blocked', WizardIsComponentSelected('avg_efficiency_in_hangar/avg_blocked'));
    JSON_SetBool(Handle,'/avg_assist', WizardIsComponentSelected('avg_efficiency_in_hangar/avg_assist'));
    JSON_SetBool(Handle,'/avg_stun', WizardIsComponentSelected('avg_efficiency_in_hangar/avg_stun'));
    JSON_SetBool(Handle,'/gun_marks', WizardIsComponentSelected('avg_efficiency_in_hangar/gun_marks'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeEffectsJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\effects.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle effects.json');
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
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\log_extended.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle log_extended.json');
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
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\minimap.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle minimap.json');
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
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\players_panels.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle players_panels.json');
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
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\service_channel_filter.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle service_channel_filter.json');
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
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\statistics.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle statistics.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('statistics'));
    JSON_SetBool(Handle,'/icon_enabled', WizardIsComponentSelected('players_panels/icon_enabled'));
    JSON_SetBool(Handle,'/statistics_change_vehicle_name_color', WizardIsComponentSelected('statistics/statistics_change_vehicle_name_color'));
    JSON_SetBool(Handle,'/statistics_enabled', WizardIsComponentSelected('statistics/statistics_enabled'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeWGLogsJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\wg_logs.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle wg_logs.json');
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
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\flight_time.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle flight_time.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('flight_time'));
    JSON_SetBool(Handle,'/spgOnly', WizardIsComponentSelected('flight_time/spgOnly'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeDistanceToEnemyJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\distance_to_enemy.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle distance_to_enemy.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('distance_to_enemy'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeBattleTimerJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\battle_timer.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle battle_timer.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('battle_timer'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeLogTotalJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\log_total.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle log_total.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('log_total'));
    if not WizardIsComponentSelected('hp_bars') then JSON_SetInteger(Handle,'/settings/x', -350);
    JSON_Close(Handle);
  end;
end;

procedure ChangeMainGunJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\main_gun.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle main_gun.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('main_gun'));
    JSON_SetBool(Handle,'/progress_bar', WizardIsComponentSelected('main_gun/progress_bar'));
    if not WizardIsComponentSelected('hp_bars') then JSON_SetInteger(Handle,'/x', 350);
    JSON_Close(Handle);
  end;
end;

procedure ChangeOwnHealthJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\own_health.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle own_health.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('own_health'));
    JSON_Close(Handle);
  end;
end;

procedure ChangeTankCarouselJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\tank_carousel.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle tank_carousel.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('tank_carousel'));
    JSON_SetBool(Handle,'/smallDoubleCarousel', WizardIsComponentSelected('tank_carousel/smallDoubleCarousel'));
    if WizardIsComponentSelected('tank_carousel/3') then JSON_SetInteger(Handle,'/carouselRows', 3);
    if WizardIsComponentSelected('tank_carousel/4') then JSON_SetInteger(Handle,'/carouselRows', 4);
    JSON_Close(Handle);
  end;
end;

procedure ChangeTeamBasesJsonValues();
var
  Handle: Integer;
begin
  Handle := JSON_OpenFile(ExpandConstant('{#configs_dir}\armagomen\team_bases_panel.json'), False);
  if Handle <> 0 then
  begin
    Log('Handle team_bases_panel.json');
    JSON_SetBool(Handle,'/enabled', WizardIsComponentSelected('team_bases_panel'));
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
      ChangeMainJsonValues();
      ChangeClockJsonValues();
      ChangeHpBarsJsonValues();
      ChangeDebugPanelJsonValues();
      ChangeDispersioCircleJsonValues();
      ChangeSixthSenseJsonValues();
      ChangeArcadeCameraJsonValues();
      ChangeStrategicCameraJsonValues();
      ChangeArmorCalculatorJsonValues();
      ChangeZoomJsonValues();
      ChangeEffiencyJsonValues();
      ChangeEffectsJsonValues();
      ChangeExtendedLogsJsonValues();
      ChangeMinimapLogsJsonValues();
      ChangePlayersPanelsJsonValues();
      ChangeServiceChannelJsonValues();
      ChangeWGLogsJsonValues();
      ChangeFlightTimeJsonValues();
      ChangeDistanceToEnemyJsonValues();
      ChangeBattleTimerJsonValues();
      ChangeLogTotalJsonValues();
      ChangeMainGunJsonValues();
      ChangeOwnHealthJsonValues();
      ChangeTankCarouselJsonValues();
      ChangeTeamBasesJsonValues();
    end;
end;


