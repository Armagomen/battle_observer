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
	import net.wg.gui.battle.components.BattleDisplayable;
	import net.wg.gui.battle.views.BaseBattlePage;
	
	public class BattleObserverLibraryMain extends MovieClip
	{
		public function BattleObserverLibraryMain()
		{
			super();
			Font.registerFont(BattleObserver.fontClass);
			BaseBattlePage.prototype.as_observerCreateComponents = function(aliases:Array, statsEnabled:Boolean = false, iconEnabled:Boolean = false):void
			{
				for each (var alias:String in aliases)
				{
					switch (alias)
					{
					case "Observer_BattleLoading_UI": 
						var statBattleLoading:BattleLoadingUI = new BattleLoadingUI(this.getComponent(BATTLE_VIEW_ALIASES.BATTLE_LOADING), statsEnabled, iconEnabled);
						this.registerComponent(statBattleLoading, alias);
						break;
					case "Observer_FullStats_UI": 
						var statFullStats:FullStatsUI = new FullStatsUI(this.getComponent(BATTLE_VIEW_ALIASES.FULL_STATS), statsEnabled, iconEnabled);
						this.registerComponent(statFullStats, alias);
						break;
					case "Observer_PlayersPanelsStatistic_UI": 
						var statPanels:PlayersPanelsStatisticUI = new PlayersPanelsStatisticUI(this.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL), statsEnabled, iconEnabled);
						this.registerComponent(statPanels, alias);
						break;
					case "Observer_UserBackGround_UI": 
						var background:UserBackGroundUI = new UserBackGroundUI();
						this.registerComponent(background, alias);
						this.addChildAt(background, 0);
						break;
					case "Observer_TeamsHP_UI": 
						var teamHealth:TeamsHealthUI = new TeamsHealthUI();
						this.registerComponent(teamHealth, alias);
						this.addChild(teamHealth)
						break;
					case "Observer_DamageLog_UI": 
						var damageLog:DamageLogsUI = new DamageLogsUI(this.getComponent(BATTLE_VIEW_ALIASES.BATTLE_DAMAGE_LOG_PANEL));
						this.registerComponent(damageLog, alias);
						this.addChild(damageLog);
						break;
					case "Observer_MainGun_UI": 
						var mainGun:MainGunUI = new MainGunUI();
						this.registerComponent(mainGun, alias);
						this.addChild(mainGun);
						break;
					case "Observer_DebugPanel_UI": 
						var debugPanel:ObserverDebugPanelUI = new ObserverDebugPanelUI();
						this.registerComponent(debugPanel, alias);
						this.addChild(debugPanel);
						break;
					case "Observer_DateTimes_UI": 
						var dateTime:ObserverDateTimesUI = new ObserverDateTimesUI();
						this.registerComponent(dateTime, alias);
						this.addChild(dateTime);
						break;
					case "Observer_BattleTimer_UI": 
						var battleTimer:ObserverBattleTimerUI = new ObserverBattleTimerUI();
						this.registerComponent(battleTimer, alias);
						this.addChild(battleTimer);
						break;
					case "Observer_SixthSense_UI": 
						var sixthSense:SixthSenseUI = new SixthSenseUI();
						this.registerComponent(sixthSense, alias);
						this.addChild(sixthSense);
						break;
					case "Observer_TeamBases_UI": 
						var teamBases:TeamBasesUI = new TeamBasesUI();
						this.registerComponent(teamBases, alias);
						this.addChild(teamBases)
						break;
					case "Observer_ArmorCalculator_UI": 
						var armorCalculator:ArmorCalculatorUI = new ArmorCalculatorUI();
						this.registerComponent(armorCalculator, alias);
						this.addChild(armorCalculator);
						break;
					case "Observer_FlightTime_UI": 
						var flightTime:FlightTimeUI = new FlightTimeUI();
						this.registerComponent(flightTime, alias);
						this.addChild(flightTime);
						break;
					case "Observer_DispersionTimer_UI": 
						var dispersionTimer:DispersionTimerUI = new DispersionTimerUI();
						this.registerComponent(dispersionTimer, alias);
						this.addChild(dispersionTimer);
						break;
					case "Observer_Distance_UI": 
						var distance:DistanceUI = new DistanceUI();
						this.registerComponent(distance, alias);
						this.addChild(distance);
						break;
					case "Observer_OwnHealth_UI": 
						var ownHealth:OwnHealthUI = new OwnHealthUI();
						this.registerComponent(ownHealth, alias);
						this.addChild(ownHealth);
						break;
					case "Observer_PlayersPanels_UI": 
						var playersPanel:PlayersPanelsUI = new PlayersPanelsUI(this.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL));
						setTimeout(this.registerComponent, 2000, playersPanel, alias);
						break;
					case "Observer_Minimap_UI": 
						var minimap:MinimapUI = new MinimapUI(this.getComponent(BATTLE_VIEW_ALIASES.MINIMAP));
						setTimeout(this.registerComponent, 2000, minimap, alias);
						break;
					default: 
						DebugUtils.LOG_WARNING("[BATTLE_OBSERVER]: No view component named - " + alias);
						break;
					}
				}
			}
			
			BaseBattlePage.prototype.as_observerUpdatePrebattleTimer = function(shadow:Boolean):void
			{
				var prebattleTimer:* = this.getComponent(BATTLE_VIEW_ALIASES.PREBATTLE_TIMER);
				if (prebattleTimer)
				{
					this.addChild(prebattleTimer);
					prebattleTimer.background.shadow.visible = !shadow;
					prebattleTimer.background.shadow.alpha = int(!shadow);
				}
			}
			
			BaseBattlePage.prototype.as_observerHideWgComponents = function(components:Array):void
			{
				for each (var alias:String in components)
				{
					var component:BattleDisplayable = this.getComponent(alias);
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