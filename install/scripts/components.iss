#define configs_dir "{app}\mods\configs\mod_battle_observer"
#define mod_source "..\..\output_data"
#define configs "default_settings"

[Types]
Name: "armagomen"; Description: {cm:types_armagomen};
Name: "user"; Description: {cm:types_user}; Flags: iscustom; 

[Components]
Name: debug_panel; Description: {cm:debug_panel}; Flags: checkablealone disablenouninstallwarning; 
Name: debug_panel/minimal; Description: minimal; Flags: exclusive disablenouninstallwarning;
Name: debug_panel/modern; Description: modern; Flags: exclusive disablenouninstallwarning; Types: "armagomen";
Name: sixth_sense; Description: {cm:sixth_sense}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: arcade_camera; Description: {cm:arcade_camera}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: armor_calculator; Description: {cm:armor_calculator}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: avg_efficiency_in_hangar; Description: {cm:avg_efficiency_in_hangar}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: battle_timer; Description: {cm:battle_timer}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: clock; Description: {cm:clock}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: dispersion_circle; Description: {cm:dispersion_circle}; Flags: checkablealone disablenouninstallwarning;
Name: dispersion_circle/replace; Description: {cm:dispersion_circle_replace}; Flags: exclusive disablenouninstallwarning; Types: "armagomen";
Name: dispersion_circle/server; Description: {cm:dispersion_circle_server}; Flags: exclusive disablenouninstallwarning;
Name: dispersion_timer; Description: {cm:dispersion_timer}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: distance_to_enemy; Description: {cm:distance_to_enemy}; Flags: disablenouninstallwarning;
Name: effects; Description: {cm:effects}; Flags: disablenouninstallwarning; Types: "armagomen user";
Name: flight_time; Description: {cm:flight_time}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: hp_bars; Description: {cm:hp_bars}; Flags: checkablealone disablenouninstallwarning;
Name: hp_bars/normal; Description: normal; Flags: exclusive disablenouninstallwarning;
Name: hp_bars/league; Description: league; Flags: exclusive disablenouninstallwarning; Types: "armagomen";
Name: log_extended; Description: {cm:log_extended}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: log_total; Description: {cm:log_total}; Flags: disablenouninstallwarning; Types: "armagomen";
Name: main; Description: {cm:main}; Flags: disablenouninstallwarning; Types: "armagomen";
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
Name: colors; Description: {cm:colors}; Flags: disablenouninstallwarning; Types: "armagomen user";

[Files]
Source: "{#mod_source}\*"; DestDir: "{app}\{code:PH_Folder_Mods}"; Flags: ignoreversion;
Source: "{#configs}\load.json"; DestDir: "{#configs_dir}"; Flags: ignoreversion;
Source: "{#configs}\debug_panel_minimal.json"; DestDir: "{#configs_dir}\armagomen"; DestName:"debug_panel.json"; Flags: ignoreversion; Components: debug_panel/minimal;
Source: "{#configs}\debug_panel_modern.json"; DestDir: "{#configs_dir}\armagomen"; DestName:"debug_panel.json"; Flags: ignoreversion; Components: debug_panel/modern;
Source: "{#configs}\sixth_sense.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: sixth_sense;
Source: "{#configs}\arcade_camera.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: arcade_camera;
Source: "{#configs}\armor_calculator.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: armor_calculator;
Source: "{#configs}\avg_efficiency_in_hangar.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: avg_efficiency_in_hangar;
Source: "{#configs}\battle_timer.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: battle_timer;
Source: "{#configs}\clock.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: clock;
Source: "{#configs}\dispersion_circle_replace.json"; DestDir: "{#configs_dir}\armagomen"; DestName:"dispersion_circle.json"; Flags: ignoreversion; Components: dispersion_circle/replace;
Source: "{#configs}\dispersion_circle_server.json"; DestDir: "{#configs_dir}\armagomen"; DestName:"dispersion_circle.json"; Flags: ignoreversion; Components: dispersion_circle/server;
Source: "{#configs}\dispersion_timer.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: dispersion_timer;
Source: "{#configs}\distance_to_enemy.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: distance_to_enemy;
Source: "{#configs}\effects.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: effects;
Source: "{#configs}\flight_time.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: flight_time;
Source: "{#configs}\hp_bars_normal.json"; DestDir: "{#configs_dir}\armagomen"; DestName:"hp_bars.json"; Flags: ignoreversion; Components: hp_bars/normal;
Source: "{#configs}\hp_bars_league.json"; DestDir: "{#configs_dir}\armagomen"; DestName:"hp_bars.json"; Flags: ignoreversion; Components: hp_bars/league;
Source: "{#configs}\log_extended.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: log_extended;
Source: "{#configs}\log_total.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: log_total;
Source: "{#configs}\main.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: main;
Source: "{#configs}\main_gun.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: main_gun;
Source: "{#configs}\minimap.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: minimap;
Source: "{#configs}\own_health.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: own_health;
Source: "{#configs}\players_panels.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: players_panels;
Source: "{#configs}\service_channel_filter.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: service_channel_filter;
Source: "{#configs}\statistics.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: statistics;
Source: "{#configs}\strategic_camera.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: strategic_camera;
Source: "{#configs}\tank_carousel.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: tank_carousel;
Source: "{#configs}\team_bases_panel.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: team_bases_panel;
Source: "{#configs}\wg_logs.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: wg_logs;
Source: "{#configs}\zoom.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: zoom;
Source: "{#configs}\colors.json"; DestDir: "{#configs_dir}\armagomen"; Flags: ignoreversion; Components: colors;

[InstallDelete]
Type: files; Name: "{app}\{code:PH_Folder_Mods}\armagomen.battleObserver*.wotmod"
Type: files; Name: "{app}\{code:PH_Folder_Mods}\me.poliroid.modslistapi*.wotmod"
Type: files; Name: "{app}\{code:PH_Folder_Mods}\polarfox.vxSettingsApi*.wotmod"
Type: filesandordirs; Name: "{app}\mods\configs\mod_battle_observer\armagomen\*.*"

[UninstallDelete]
Type: files; Name: "{app}\{code:PH_Folder_Mods}\armagomen.battleObserver*.wotmod"
