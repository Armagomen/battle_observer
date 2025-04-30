package net.armagomen.battle_observer.battle.components.teamshealth
{
	import flash.events.Event;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class TeamsHealthUI extends ObserverBattleDisplayable
	{
		private var hpBars:*;
		private var correlation:* = null;
		
		public function TeamsHealthUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();			
			var settings:Object = this.getSettings();
			this.x = App.appWidth >> 1;
			
			var _class:* = settings.style == "league" ? League : Default;
			this.hpBars = new _class(this.isColorBlind(), this.getColors().global, this);
			
			var page:* = parent;
			this.correlation = page.getComponent(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR);
			
			this.updateCorrelationBar();
			this.updateCountersPosition();
			
			var q_progress:* = page.getComponent(BATTLE_VIEW_ALIASES.QUEST_PROGRESS_TOP_VIEW);
			page.addChildAt(q_progress, page.getChildIndex(this.correlation) - 1);
		}
		
		private function updateCorrelationBar():void
		{
			this.correlation.greenBackground.alpha = 0;
			this.correlation.redBackground.alpha = 0;
			this.correlation.purpleBackground.alpha = 0;
			this.correlation.teamFragsSeparatorField.alpha = 0;
			this.correlation.allyTeamFragsField.alpha = 0;
			this.correlation.enemyTeamFragsField.alpha = 0;
			this.correlation.allyTeamHealthBar.alpha = 0;
			this.correlation.enemyTeamHealthBar.alpha = 0;
			var background:* = this.correlation.getChildAt(0);
			background.y = -22;
			background.alpha = 0.9;
			this.correlation.y = 20;
		}
		
		private function updateCountersPosition():void
		{
			this.correlation.allyVehicleMarkersList._markerStartPosition = -25;
			this.correlation.enemyVehicleMarkersList._markerStartPosition = -5;
			this.correlation.allyVehicleMarkersList.sort();
			this.correlation.enemyVehicleMarkersList.sort();
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.hpBars.remove();
			this.hpBars = null;
			this.correlation = null;
		}
		
		public function as_colorBlind(enabled:Boolean):void
		{
			if (this.hpBars)
			{
				this.hpBars.setColorBlind(enabled);
			}
		}
		
		public function as_updateHealth(alliesHP:int, enemiesHP:int, totalAlliesHP:int, totalEnemiesHP:int):void
		{
			if (this.hpBars)
			{
				this.hpBars.update(alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP);
			}
		}
		
		public function as_updateScore(ally:int, enemy:int):void
		{
			if (this.hpBars)
			{
				this.hpBars.updateScore(ally, enemy);
			}
		}
		
		override public function onResizeHandle(event:Event):void
		{
			this.x = App.appWidth >> 1;
			this.updateCountersPosition();
		}
	}
}