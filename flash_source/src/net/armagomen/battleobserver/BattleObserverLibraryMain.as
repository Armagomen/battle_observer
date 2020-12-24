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
import net.armagomen.battleobserver.battle.components.FlightTimeUI;
import net.armagomen.battleobserver.battle.components.ObserverDateTimesUI;
import net.armagomen.battleobserver.battle.components.ScorePanelUI;
import net.armagomen.battleobserver.battle.components.UserBackGroundUI;
import net.armagomen.battleobserver.battle.components.DispersionTimerUI;
import net.armagomen.battleobserver.battle.components.batlletimer.ObserverBattleTimerUI;
import net.armagomen.battleobserver.battle.components.debugpanel.ObserverDebugPanelUI;
import net.armagomen.battleobserver.battle.components.maingun.MainGunUI;
import net.armagomen.battleobserver.battle.components.playerspanels.PlayersPanelsUI;
import net.armagomen.battleobserver.battle.components.sixthsense.SixthSenseUI;
import net.armagomen.battleobserver.battle.components.teambases.TeamBasesUI;
import net.armagomen.battleobserver.battle.components.teamshealth.TeamsHealthUI;
import net.armagomen.battleobserver.battle.components.wgcomponents.MinimapUI;
import net.armagomen.battleobserver.battle.components.wgcomponents.WGComponentsSetting;
import net.armagomen.battleobserver.battle.utils.*;
	import net.armagomen.battleobserver.font.BattleObserver;
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
				var child:* = this.getComponent(BATTLE_VIEW_ALIASES.PREBATTLE_TIMER);
				var index:int = this.getChildIndex(child) - 1;
				switch (ui_name)
				{
				case "Observer_WGCompSettings_UI":
					if (!this.isFlashComponentRegisteredS(ui_name))
					{
						this.registerComponent(this.addChild(new WGComponentsSetting(ui_name)), ui_name);
					}
					break;
				case "Observer_UserBackGround_UI":
					if (!this.isFlashComponentRegisteredS(ui_name))
					{
						this.registerComponent(this.addChildAt(new UserBackGroundUI(ui_name), 0), ui_name);
					}
					break;
				case "Observer_TeamsHP_UI":
					if (!this.isFlashComponentRegisteredS(ui_name))
					{
						this.registerComponent(this.addChildAt(new TeamsHealthUI(ui_name), index), ui_name);
					}
					break;
				case "Observer_ScorePanel_UI":
					if (!this.isFlashComponentRegisteredS(ui_name))
					{
						this.registerComponent(this.addChildAt(new ScorePanelUI(ui_name), index), ui_name);
					}
					break;
				case "Observer_DamageLog_UI":
					if (!this.isFlashComponentRegisteredS(ui_name))
					{
						this.registerComponent(this.addChildAt(new DamageLogsUI(ui_name), index), ui_name);
					}
					break;
				case "Observer_MainGun_UI":
					if (!this.isFlashComponentRegisteredS(ui_name))
					{
						this.registerComponent(this.addChildAt(new MainGunUI(ui_name), index), ui_name);
					}
					break;
				case "Observer_DebugPanel_UI":
					if (!this.isFlashComponentRegisteredS(ui_name))
					{
						this.registerComponent(this.addChildAt(new ObserverDebugPanelUI(ui_name), index), ui_name);
					}
					break;
				case "Observer_DateTimes_UI":
					if (!this.isFlashComponentRegisteredS(ui_name))
					{
						this.registerComponent(this.addChildAt(new ObserverDateTimesUI(ui_name), index), ui_name);
					}
					break;
				case "Observer_BattleTimer_UI":
					if (!this.isFlashComponentRegisteredS(ui_name))
					{
						this.registerComponent(this.addChildAt(new ObserverBattleTimerUI(ui_name), index), ui_name);
					}
					break;
				case "Observer_SixthSense_UI":
					if (!this.isFlashComponentRegisteredS(ui_name))
					{
						this.registerComponent(this.addChildAt(new SixthSenseUI(ui_name), index), ui_name);
					}
					break;
				case "Observer_TeamBases_UI":
					if (!this.isFlashComponentRegisteredS(ui_name))
					{
						this.registerComponent(this.addChildAt(new TeamBasesUI(ui_name), index), ui_name);
					}
					break;
				case "Observer_ArmorCalculator_UI":
					if (!this.isFlashComponentRegisteredS(ui_name)) {
						this.registerComponent(this.addChildAt(new ArmorCalculatorUI(ui_name), index), ui_name);
					}
					break;
					case "Observer_FlightTime_UI":
						if (!this.isFlashComponentRegisteredS(ui_name)) {
							this.registerComponent(this.addChildAt(new FlightTimeUI(ui_name), index), ui_name);
						}
						break;
					case "Observer_DispersionTimer_UI":
						if (!this.isFlashComponentRegisteredS(ui_name)) {
							this.registerComponent(this.addChildAt(new DispersionTimerUI(ui_name), index), ui_name);
						}
						break;
					case "Observer_PlayersPanels_UI":
						if (!this.isFlashComponentRegisteredS(ui_name)) {
							this.registerComponent(this.addChildAt(new PlayersPanelsUI(ui_name), index), ui_name);
						}
						break;
					case "Observer_Minimap_UI":
						if (!this.isFlashComponentRegisteredS(ui_name)) {
						this.registerComponent(this.addChild(new MinimapUI(ui_name)), ui_name);
					}
					break;
				default:
					DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO]: No view component named - " + ui_name);
					break;
				}
			}
		}
	}
}