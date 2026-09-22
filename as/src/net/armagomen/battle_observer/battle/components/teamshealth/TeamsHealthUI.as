package net.armagomen.battle_observer.battle.components.teamshealth
{
	import flash.events.Event;
	import flash.utils.setTimeout;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class TeamsHealthUI extends ObserverBattleDisplayable
	{
		private var bar_style:*;
		private const LEAGUE_BIG:String = "league_big";
		private const OFFSET:Number = 20;
		
		public function TeamsHealthUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			if (this.notInitialized())
			{
				var correlation:* = this.battlePage.getComponent(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR);
				this.updateCorrelationBar(correlation);
				var styles:Object = {"league": League, "league_big": LeagueBig, "normal": Default};
				var settings:Object = this.getSettings();
				this.bar_style = new styles[settings.style](App.colorSchemeMgr.getIsColorBlindS(), this.getColors().global);
				this.bar_style.y = -OFFSET;
				correlation.addChild(this.bar_style);
				if (settings.style != LEAGUE_BIG)
				{
					setTimeout(this.updateCountersPosition, 500, correlation);
				}
				var q_progress:* = this.battlePage.getComponent(BATTLE_VIEW_ALIASES.QUEST_PROGRESS_TOP_VIEW);
				if (q_progress){
					q_progress.getChildAt(0).alpha = 0.8;
					this.battlePage.addChildAt(q_progress, this.battlePage.getChildIndex(correlation) - 1);
				}
			}
		}
		
		private function updateCorrelationBar(correlation:*):void
		{
			var background:* = correlation.getChildAt(0);
			background.alpha = 0.8;
			background.y = -OFFSET;
			
			correlation.greenBackground.alpha = 0;
			correlation.redBackground.alpha = 0;
			correlation.purpleBackground.alpha = 0;
			correlation.teamFragsSeparatorField.alpha = 0;
			correlation.allyTeamFragsField.alpha = 0;
			correlation.enemyTeamFragsField.alpha = 0;
			correlation.allyTeamHealthBar.alpha = 0;
			correlation.enemyTeamHealthBar.alpha = 0;
			
			correlation.removeChild(correlation.greenBackground);
			correlation.removeChild(correlation.redBackground);
			correlation.removeChild(correlation.purpleBackground);
			correlation.removeChild(correlation.teamFragsSeparatorField);
			correlation.removeChild(correlation.allyTeamFragsField);
			correlation.removeChild(correlation.enemyTeamFragsField);
			correlation.removeChild(correlation.allyTeamHealthBar);
			correlation.removeChild(correlation.enemyTeamHealthBar);
			
			correlation.y = OFFSET;
			
		}
		
		private function updateCountersPosition(correlation:*):void
		{
			correlation.allyVehicleMarkersList._markerStartPosition = -30;
			correlation.enemyVehicleMarkersList._markerStartPosition = 0;
			correlation.allyVehicleMarkersList.sort(correlation.allyVehicleMarkersList._vehicleIDs);
			correlation.enemyVehicleMarkersList.sort(correlation.enemyVehicleMarkersList._vehicleIDs);
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			if (this.bar_style)
			{
				this.bar_style.remove();
				this.bar_style = null;
			}
		}
		
		public function as_colorBlind(enabled:Boolean):void
		{
			if (this.bar_style)
			{
				this.bar_style.setColorBlind(enabled);
			}
		}
		
		public function as_updateHealth(alliesHP:int, enemiesHP:int, totalAlliesHP:int, totalEnemiesHP:int):void
		{
			if (this.bar_style)
			{
				this.bar_style.update(alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP);
			}
		}
		
		public function as_updateScore(ally:int, enemy:int):void
		{
			if (this.bar_style)
			{
				this.bar_style.updateScore(ally, enemy);
			}
		}
		
		override public function onResizeHandle(event:Event):void
		{
			if (this.getSettings().style != LEAGUE_BIG)
			{
				this.updateCountersPosition(this.battlePage.getComponent(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR));
			}
		}
	}
}