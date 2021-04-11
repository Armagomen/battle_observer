package net.armagomen.battleobserver
{
	/**
	 * ...
	 * @author Armagomen
	 */
	
	import flash.display.*;
	import flash.events.*;
	import flash.text.Font;
	import flash.utils.*;
	import net.armagomen.battleobserver.battle.components.ArmorCalculatorUI;
	import net.armagomen.battleobserver.battle.components.DamageLogsUI;
	import net.armagomen.battleobserver.battle.components.DispersionTimerUI;
	import net.armagomen.battleobserver.battle.components.FlightTimeUI;
	import net.armagomen.battleobserver.battle.components.ObserverDateTimesUI;
	import net.armagomen.battleobserver.battle.components.UserBackGroundUI;
	import net.armagomen.battleobserver.battle.components.batlletimer.ObserverBattleTimerUI;
	import net.armagomen.battleobserver.battle.components.debugpanel.ObserverDebugPanelUI;
	import net.armagomen.battleobserver.battle.components.maingun.MainGunUI;
	import net.armagomen.battleobserver.battle.components.playerspanels.PlayersPanelsUI;
	import net.armagomen.battleobserver.battle.components.sixthsense.SixthSenseUI;
	import net.armagomen.battleobserver.battle.components.teambases.TeamBasesUI;
	import net.armagomen.battleobserver.battle.components.teamshealth.TeamsHealthUI;
	import net.armagomen.battleobserver.battle.components.wgcomponents.MinimapUI;
	import net.armagomen.battleobserver.battle.components.wgcomponents.WGComponentsSetting;
	import net.armagomen.battleobserver.font.BattleObserver;
	import net.armagomen.battleobserver.utils.*;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.*;
	import net.wg.gui.battle.random.views.*;
	import net.wg.gui.battle.views.BaseBattlePage;
	import net.wg.infrastructure.base.*;
	
	public class BattleObserverLibraryMain extends MovieClip
	{
		private var _idx:int = 0;
		
		public function BattleObserverLibraryMain()
		{
			super();
			Font.registerFont(BattleObserver.fontClass);
			BaseBattlePage.prototype['as_createBattleObserverComp'] = function(ui_name:String):void
			{
				
				switch (ui_name)
				{
				case "Observer_UserBackGround_UI": 
					this.registerComponent(this.addChildAt(new UserBackGroundUI, _idx), ui_name);
					break;
				case "Observer_TeamsHP_UI": 
					this.registerComponent(this.addChildAt(new TeamsHealthUI, _idx), ui_name);
					break;
				case "Observer_DamageLog_UI": 
					this.registerComponent(this.addChildAt(new DamageLogsUI, _idx), ui_name);
					break;
				case "Observer_MainGun_UI":
					this.registerComponent(this.addChildAt(new MainGunUI, _idx), ui_name);
					break;
				case "Observer_DebugPanel_UI":
					this.registerComponent(this.addChildAt(new ObserverDebugPanelUI, _idx), ui_name);
					break;
				case "Observer_DateTimes_UI":
					this.registerComponent(this.addChildAt(new ObserverDateTimesUI, _idx), ui_name);
					break;
				case "Observer_BattleTimer_UI":
					this.registerComponent(this.addChildAt(new ObserverBattleTimerUI, _idx), ui_name);
					break;
				case "Observer_SixthSense_UI":
					this.registerComponent(this.addChildAt(new SixthSenseUI, _idx), ui_name);
					break;
				case "Observer_TeamBases_UI":
					this.registerComponent(this.addChildAt(new TeamBasesUI, _idx), ui_name);
					break;
				case "Observer_ArmorCalculator_UI":
					this.registerComponent(this.addChildAt(new ArmorCalculatorUI, _idx), ui_name);
					break;
				case "Observer_FlightTime_UI":
					this.registerComponent(this.addChildAt(new FlightTimeUI, _idx), ui_name);
					break;
				case "Observer_DispersionTimer_UI":
					this.registerComponent(this.addChildAt(new DispersionTimerUI, _idx), ui_name);
					break;
				case "Observer_PlayersPanels_UI":
					this.registerComponent(this.addChildAt(new PlayersPanelsUI, _idx), ui_name);
					break;
				case "Observer_Minimap_UI":
					this.registerComponent(this.addChildAt(new MinimapUI, _idx), ui_name);
					break;
				case "Observer_WGCompSettings_UI":
					this.registerComponent(this.addChildAt(new WGComponentsSetting, _idx), ui_name);
					break;
				default: 
					DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO]: No view component named - " + ui_name);
					break;
				}
			}
		}
	}
}