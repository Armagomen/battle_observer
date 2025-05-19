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
		private const LEAGUE:String     = "league";
		private const NORMAL:String     = "normal";
		
		public function TeamsHealthUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			if (not_initialized)
			{
				super.onPopulate();
				var correlation:* = this.battlePage.getComponent(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR);
				this.updateCorrelationBar(correlation);
				var styles:Object   = {LEAGUE: League, LEAGUE_BIG: LeagueBig, NORMAL: Default};
				var settings:Object = this.getSettings();
				this.x = App.appWidth >> 1;
				this.bar_style = this.addChild(new styles[settings.style](App.colorSchemeMgr.getIsColorBlindS(), this.getColors().global));
				
				if (settings.style != LEAGUE_BIG)
				{
					setTimeout(this.updateCountersPosition, 500, correlation);
				}
				var q_progress:* = this.battlePage.getComponent(BATTLE_VIEW_ALIASES.QUEST_PROGRESS_TOP_VIEW);
				this.battlePage.addChildAt(q_progress, this.battlePage.getChildIndex(correlation) - 1);
			}
			else
			{
				super.onPopulate();
			}
		}
		
		private function updateCorrelationBar(correlation:*):void
		{
			correlation.greenBackground.alpha = 0;
			correlation.redBackground.alpha = 0;
			correlation.purpleBackground.alpha = 0;
			correlation.teamFragsSeparatorField.alpha = 0;
			correlation.allyTeamFragsField.alpha = 0;
			correlation.enemyTeamFragsField.alpha = 0;
			correlation.allyTeamHealthBar.alpha = 0;
			correlation.enemyTeamHealthBar.alpha = 0;
			var background:* = correlation.getChildAt(0);
			background.y = -22;
			background.alpha = 0.9;
			correlation.y = 20;
		}
		
		private function updateCountersPosition(correlation:*):void
		{
			correlation.allyVehicleMarkersList._markerStartPosition = -25;
			correlation.enemyVehicleMarkersList._markerStartPosition = -5;
			correlation.allyVehicleMarkersList.sort();
			correlation.enemyVehicleMarkersList.sort();
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.bar_style.remove();
			this.bar_style = null;
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
			this.x = App.appWidth >> 1;
			if (this.getSettings().style != LEAGUE_BIG)
			{
				this.updateCountersPosition(this.battlePage.getComponent(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR));
			}
		}
	}
}