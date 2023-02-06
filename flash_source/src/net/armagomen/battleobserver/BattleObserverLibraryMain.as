package net.armagomen.battleobserver
{
	/**
	 * ...
	 * @author Armagomen
	 */
	
	import flash.display.*;
	import flash.text.Font;
	import net.armagomen.battleobserver.battle.StatisticsAndIcons;
	import net.armagomen.battleobserver.battle.components.ArmorCalculatorUI;
	import net.armagomen.battleobserver.battle.components.DamageLogsUI;
	import net.armagomen.battleobserver.battle.components.DispersionTimerUI;
	import net.armagomen.battleobserver.battle.components.DistanceUI;
	import net.armagomen.battleobserver.battle.components.FlightTimeUI;
	import net.armagomen.battleobserver.battle.components.ObserverDateTimesUI;
	import net.armagomen.battleobserver.battle.components.OwnHealthUI;
	import net.armagomen.battleobserver.battle.components.battletimer.ObserverBattleTimerUI;
	import net.armagomen.battleobserver.battle.components.debugpanel.ObserverDebugPanelUI;
	import net.armagomen.battleobserver.battle.components.maingun.MainGunUI;
	import net.armagomen.battleobserver.battle.components.playerspanels.PlayersPanelsUI;
	import net.armagomen.battleobserver.battle.components.sixthsense.SixthSenseUI;
	import net.armagomen.battleobserver.battle.components.teambases.TeamBasesUI;
	import net.armagomen.battleobserver.battle.components.teamshealth.TeamsHealthUI;
	import net.armagomen.battleobserver.battle.wgcomponents.minimapZoom;
	import net.armagomen.battleobserver.font.BattleObserver;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.views.BaseBattlePage;
	import net.wg.infrastructure.base.AbstractView;
	
	public class BattleObserverLibraryMain extends AbstractView
	{
		private var mapZoom:minimapZoom             = null;
		private var statisticsBO:StatisticsAndIcons = null;
		
		public function BattleObserverLibraryMain()
		{
			super();
			Font.registerFont(BattleObserver.fontClass);
			BaseBattlePage.prototype.as_observerCreateComponents = function(aliases:Array):void
			{
				for each (var alias:String in aliases)
				{
					switch (alias)
					{
					case "Observer_TeamsHP_UI": 
						var teamHealthUI:TeamsHealthUI = new TeamsHealthUI();
						this.registerComponent(teamHealthUI, alias);
						this.addChild(teamHealthUI);
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
						this.addChildAt(sixthSense, this.getChildIndex(this.getComponent(BATTLE_VIEW_ALIASES.SIXTH_SENSE)));
						break;
					case "Observer_TeamBases_UI": 
						var teamBases:TeamBasesUI = new TeamBasesUI();
						this.registerComponent(teamBases, alias);
						this.addChildAt(teamBases, this.getChildIndex(this.getComponent(BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL)));
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
						var playersPanel:PlayersPanelsUI = new PlayersPanelsUI(this);
						this.registerComponent(playersPanel, alias);
						break;
					default: 
						DebugUtils.LOG_WARNING("[BATTLE_OBSERVER]: No view component named - " + alias);
						break;
					}
					this.showComponent(alias, false);
				}
			}
			
			BaseBattlePage.prototype.as_createStatisticComponent = function(iconsEnabled:Boolean, statsData:Object, cutWidth:Number, fullWidth:Number, typeColors:Object, iconMultiplier:Number):void
			{
				this.statisticsBO = new StatisticsAndIcons(this, iconsEnabled, statsData, cutWidth, fullWidth, typeColors, iconMultiplier);
			}
			
			BaseBattlePage.prototype.as_updateStatisticData = function(statsData:Object):void
			{
				if (this.statisticsBO)
				{
					this.statisticsBO.update_wtrdata(statsData);
				}
			}
			
			BaseBattlePage.prototype.as_createMimimapCentered = function():void
			{
				this.mapZoom = new minimapZoom(this);
			}
			
			BaseBattlePage.prototype.as_zoomMimimapCentered = function(enable:Boolean):void
			{
				if (this.mapZoom)
				{
					this.mapZoom.minimapCentered(enable);
				}
			}
			
			BaseBattlePage.prototype.as_observerHideWgComponents = function(components:Array):void
			{
				for each (var alias:String in components)
				{
					var component:* = this.getComponent(alias);
					if (component)
					{
						component.visible = false;
						component.alpha = 0;
						this.removeChild(component);
					}
				}
				var prebattleTimer:* = this.getComponent(BATTLE_VIEW_ALIASES.PREBATTLE_TIMER);
				if (prebattleTimer)
				{
					this.addChild(prebattleTimer);
				}
				var damageIndicator:* = this.getComponent(BATTLE_VIEW_ALIASES.DAMAGE_INDICATOR);
				if (damageIndicator)
				{
					this.addChild(damageIndicator);
				}
			}
			
			BaseBattlePage.prototype.as_observerUpdateDamageLogPosition = function(isEpicRandomBattle:Boolean):void
			{
				var damageLogPanel:* = this.getComponent(BATTLE_VIEW_ALIASES.BATTLE_DAMAGE_LOG_PANEL);
				if (damageLogPanel)
				{
					damageLogPanel.updateContainersPosition()
					if (isEpicRandomBattle)
					{
						this.updateDamageLogPosition(this.epicRandomPlayersPanel.state);
					}
					else
					{
						this.updateDamageLogPosition();
					}
				}
			}
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.mapZoom = null;
			this.statisticsBO = null;
		}
	}
}