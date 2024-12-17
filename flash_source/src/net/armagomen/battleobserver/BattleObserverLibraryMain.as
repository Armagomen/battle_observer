package net.armagomen.battleobserver
{
	/**
	 * ...
	 * @author Armagomen
	 */
	
	import flash.display.*;
	import net.armagomen.battleobserver.battle.components.ArmorCalculatorUI;
	import net.armagomen.battleobserver.battle.components.DamageLogsUI;
	import net.armagomen.battleobserver.battle.components.DispersionTimerUI;
	import net.armagomen.battleobserver.battle.components.DistanceUI;
	import net.armagomen.battleobserver.battle.components.FlightTimeUI;
	import net.armagomen.battleobserver.battle.components.MinimapUI;
	import net.armagomen.battleobserver.battle.components.ObserverDateTimesUI;
	import net.armagomen.battleobserver.battle.components.OwnHealthUI;
	import net.armagomen.battleobserver.battle.components.StatisticsAndIcons;
	import net.armagomen.battleobserver.battle.components.battletimer.ObserverBattleTimerUI;
	import net.armagomen.battleobserver.battle.components.debugpanel.ObserverDebugPanelUI;
	import net.armagomen.battleobserver.battle.components.maingun.MainGunUI;
	import net.armagomen.battleobserver.battle.components.playerspanels.PlayersPanelsUI;
	import net.armagomen.battleobserver.battle.components.sixthsense.SixthSenseUI;
	import net.armagomen.battleobserver.battle.components.teambases.TeamBasesUI;
	import net.armagomen.battleobserver.battle.components.teamshealth.TeamsHealthUI;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.views.BaseBattlePage;
	import net.wg.infrastructure.base.AbstractView;
	
	public class BattleObserverLibraryMain extends AbstractView
	{
	
		public function BattleObserverLibraryMain()
		{
			super();
			BaseBattlePage.prototype.as_BattleObserverCreate = function(aliases:Array, hidden:Array):void
			{
				var alias_to_ui:Object = {"Observer_MainGun_UI": MainGunUI, "Observer_TeamsHP_UI": TeamsHealthUI, "Observer_DamageLog_UI": DamageLogsUI, "Observer_DebugPanel_UI": ObserverDebugPanelUI, "Observer_BattleTimer_UI": ObserverBattleTimerUI, "Observer_SixthSense_UI": SixthSenseUI, "Observer_TeamBases_UI": TeamBasesUI, "Observer_ArmorCalculator_UI": ArmorCalculatorUI, "Observer_FlightTime_UI": FlightTimeUI, "Observer_DispersionTimer_UI": DispersionTimerUI, "Observer_DateTimes_UI": ObserverDateTimesUI, "Observer_Distance_UI": DistanceUI, "Observer_OwnHealth_UI": OwnHealthUI, "Observer_PlayersPanels_UI": PlayersPanelsUI, "Observer_WGRAndIcons_UI": StatisticsAndIcons, "Observer_MiniMap_UI": MinimapUI};
				
				for each (var alias:String in aliases)
				{
					try
					{
						if (this.isFlashComponentRegisteredS(alias))
						{
							continue;
						}
						this.registerComponent(this.addChild(new alias_to_ui[alias]()), alias);
						this.showComponent(alias, false);
					}
					catch (err:Error)
					{
						DebugUtils.LOG_ERROR("[BATTLE_OBSERVER] registerComponent " + alias + " : " + err.message);
					}
				}
				
				for each (var alias:String in hidden)
				{
					var component:* = this.getComponent(alias);
					if (component)
					{
						component.visible = false;
						component.alpha = 0;
						component.removeChildren();
						this.removeChild(component);
					}
				}
				var prebattleTimer:* = this.getComponent(BATTLE_VIEW_ALIASES.PREBATTLE_TIMER);
				if (prebattleTimer)
				{
					this.addChild(prebattleTimer);
				}
			}
		}
	}
}