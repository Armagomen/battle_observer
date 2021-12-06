package net.armagomen.battleobserver
{
	/**
	 * ...
	 * @author Armagomen
	 */
	
	import flash.display.*;
	import flash.text.Font;
	import flash.utils.setTimeout;
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
	import net.armagomen.battleobserver.battle.components.ststistics.BattleLoadingUI;
	import net.armagomen.battleobserver.battle.components.ststistics.FullStatsUI;
	import net.armagomen.battleobserver.battle.components.ststistics.PlayersPanelsStatisticUI;
	import net.armagomen.battleobserver.battle.components.teambases.TeamBasesUI;
	import net.armagomen.battleobserver.battle.components.teamshealth.TeamsHealthUI;
	import net.armagomen.battleobserver.battle.components.wgcomponents.MinimapUI;
	import net.armagomen.battleobserver.font.BattleObserver;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.views.BaseBattlePage;
	
	public class BattleObserverLibraryMain extends MovieClip
	{
		public function BattleObserverLibraryMain()
		{
			super();
			Font.registerFont(BattleObserver.fontClass);
			BaseBattlePage.prototype['as_createBattleObserverComp'] = function(alias:String, statsEnabled:Boolean = false, iconEnabled:Boolean = false):void
			{
				switch (alias)
				{
				
				case "Observer_BattleLoading_UI": 
					this.registerComponent(new BattleLoadingUI(this.getComponent(BATTLE_VIEW_ALIASES.BATTLE_LOADING), statsEnabled, iconEnabled), alias);
					break;
				case "Observer_FullStats_UI": 
					this.registerComponent(new FullStatsUI(this.getComponent(BATTLE_VIEW_ALIASES.FULL_STATS), statsEnabled, iconEnabled), alias);
					break;
				case "Observer_PlayersPanelsStatistic_UI": 
					this.registerComponent(new PlayersPanelsStatisticUI(this.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL), statsEnabled, iconEnabled), alias);
					break;
				case "Observer_UserBackGround_UI": 
					this.registerComponent(this.addChildAt(new UserBackGroundUI(), 0), alias);
					break;
				case "Observer_TeamsHP_UI": 
					this.registerComponent(this.addChild(new TeamsHealthUI()), alias);
					break;
				case "Observer_DamageLog_UI": 
					this.registerComponent(this.addChild(new DamageLogsUI()), alias);
					break;
				case "Observer_MainGun_UI": 
					this.registerComponent(this.addChild(new MainGunUI()), alias);
					break;
				case "Observer_DebugPanel_UI": 
					this.registerComponent(this.addChild(new ObserverDebugPanelUI()), alias);
					break;
				case "Observer_DateTimes_UI": 
					this.registerComponent(this.addChild(new ObserverDateTimesUI()), alias);
					break;
				case "Observer_BattleTimer_UI": 
					this.registerComponent(this.addChild(new ObserverBattleTimerUI()), alias);
					break;
				case "Observer_SixthSense_UI": 
					this.registerComponent(this.addChild(new SixthSenseUI()), alias);
					break;
				case "Observer_TeamBases_UI": 
					this.registerComponent(this.addChild(new TeamBasesUI()), alias);
					break;
				case "Observer_ArmorCalculator_UI": 
					this.registerComponent(this.addChild(new ArmorCalculatorUI()), alias);
					break;
				case "Observer_FlightTime_UI": 
					this.registerComponent(this.addChild(new FlightTimeUI()), alias);
					break;
				case "Observer_DispersionTimer_UI": 
					this.registerComponent(this.addChild(new DispersionTimerUI()), alias);
					break;
				case "Observer_Distance_UI": 
					this.registerComponent(this.addChild(new DistanceUI()), alias);
					break;
				case "Observer_OwnHealth_UI": 
					this.registerComponent(this.addChild(new OwnHealthUI()), alias);
					break;
				case "Observer_PlayersPanels_UI": 
					setTimeout(this.registerComponent, 3000, new PlayersPanelsUI(this.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL)), alias);
					break;
				case "Observer_Minimap_UI": 
					setTimeout(this.registerComponent, 5000, new MinimapUI(this.getComponent(BATTLE_VIEW_ALIASES.MINIMAP)), alias);
					break;
				default: 
					DebugUtils.LOG_WARNING("[BATTLE_OBSERVER]: No view component named - " + alias);
					break;
				}
			}
			
			BaseBattlePage.prototype['as_observerUpdatePrebattleTimer'] = function(shadow:Boolean):void
			{
				var prebattleTimer:* = this.getComponent(BATTLE_VIEW_ALIASES.PREBATTLE_TIMER);
				if (prebattleTimer)
				{
					this.addChild(prebattleTimer);
					prebattleTimer.background.shadow.visible = !shadow;
					prebattleTimer.background.shadow.alpha = int(!shadow);
				}
			}
			
			BaseBattlePage.prototype['as_observerHideWgComponents'] = function(components:Array):void
			{
				for each (var alias:String in components)
				{
					var component:* = this.getComponent(alias);
					if (component)
					{
						component.visible = false;
						component.alpha = 0;
					}
				}
			}
		}
	}
}