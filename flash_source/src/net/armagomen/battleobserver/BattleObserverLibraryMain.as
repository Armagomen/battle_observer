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
	import net.armagomen.battleobserver.battle.components.DistanceUI;
	import net.armagomen.battleobserver.battle.components.FlightTimeUI;
	import net.armagomen.battleobserver.battle.components.ObserverDateTimesUI;
	import net.armagomen.battleobserver.battle.components.OwnHealthUI;
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
		
		public function BattleObserverLibraryMain()
		{
			super();
			Font.registerFont(BattleObserver.fontClass);
			BaseBattlePage.prototype['as_createBattleObserverComp'] = function(ui_name:String):void
			{
				switch (ui_name)
				{
				case "Observer_UserBackGround_UI": 
					this.registerComponent(this.addChildAt(new UserBackGroundUI, 0), ui_name);
					break;
				case "Observer_TeamsHP_UI": 
					this.registerComponent(this.addChild(new TeamsHealthUI), ui_name);
					break;
				case "Observer_DamageLog_UI": 
					this.registerComponent(this.addChild(new DamageLogsUI), ui_name);
					break;
				case "Observer_MainGun_UI": 
					this.registerComponent(this.addChild(new MainGunUI), ui_name);
					break;
				case "Observer_DebugPanel_UI": 
					this.registerComponent(this.addChild(new ObserverDebugPanelUI), ui_name);
					break;
				case "Observer_DateTimes_UI": 
					this.registerComponent(this.addChild(new ObserverDateTimesUI), ui_name);
					break;
				case "Observer_BattleTimer_UI": 
					this.registerComponent(this.addChild(new ObserverBattleTimerUI), ui_name);
					break;
				case "Observer_SixthSense_UI": 
					this.registerComponent(this.addChild(new SixthSenseUI), ui_name);
					break;
				case "Observer_TeamBases_UI": 
					this.registerComponent(this.addChild(new TeamBasesUI), ui_name);
					break;
				case "Observer_ArmorCalculator_UI": 
					this.registerComponent(this.addChild(new ArmorCalculatorUI), ui_name);
					break;
				case "Observer_FlightTime_UI": 
					this.registerComponent(this.addChild(new FlightTimeUI), ui_name);
					break;
				case "Observer_DispersionTimer_UI": 
					this.registerComponent(this.addChild(new DispersionTimerUI), ui_name);
					break;
				case "Observer_Distance_UI": 
					this.registerComponent(this.addChild(new DistanceUI), ui_name);
					break;
				case "Observer_OwnHealth_UI": 
					this.registerComponent(this.addChild(new OwnHealthUI), ui_name);
					break;
				case "Observer_PlayersPanels_UI": 
					this.registerComponent(this.addChild(new PlayersPanelsUI), ui_name);
					break;
				case "Observer_Minimap_UI": 
					this.registerComponent(this.addChild(new MinimapUI), ui_name);
					break;
				case "Observer_WGCompSettings_UI": 
					this.registerComponent(this.addChild(new WGComponentsSetting), ui_name);
					break;
				default: 
					DebugUtils.LOG_WARNING("[BATTLE_OBSERVER]: No view component named - " + ui_name);
					break;
				}
			}
			BaseBattlePage.prototype['as_updateBattleObserverChildIndexes'] = function():void
			{
				var prebattleTimer:DisplayObject = this.getComponent(BATTLE_VIEW_ALIASES.PREBATTLE_TIMER);
				if (prebattleTimer)
				{
					this.removeChild(prebattleTimer);
					this.addChild(prebattleTimer);
				}
			}
		}
	}
}