package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.events.Event;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.battle.interfaces.ITeamHealth;
	
	public class TeamsHealthUI extends ObserverBattleDisplayable
	{
		private var hpBars:ITeamHealth;
		private var score:Score;
		private var markers:Markers;
		
		public function TeamsHealthUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			var settings:Object = this.getSettings();
			this.x = App.appWidth >> 1;
			this.hpBars = this.createHpBars(settings.style);
			this.score = new Score(this.isColorBlind(), this.getColors().global, settings.style);
			this.addChild(this.hpBars);
			this.addChild(this.score);
			if (settings.markers.enabled)
			{
				this.markers = new Markers(settings.markers, this.getAlpha());
				this.addChild(this.markers);
			}
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.hpBars.remove();
			this.hpBars = null;
			this.score.removeChildren();
			this.score = null;
			if (this.markers)
			{
				this.markers.removeChildren();
				this.markers = null;
			}
		}
		
		private function createHpBars(style:String):ITeamHealth
		{
			switch (style)
			{
			case "league": 
				return new League(this.isColorBlind(), this.getColors().global);
			default: 
				return new Default(this.isColorBlind(), this.getColors().global);
			}
		}
		
		public function as_colorBlind(enabled:Boolean):void
		{
			this.hpBars.setColorBlind(enabled);
			this.score.setColorBlind(enabled);
		}
		
		public function as_updateHealth(alliesHP:int, enemiesHP:int, totalAlliesHP:int, totalEnemiesHP:int):void
		{
			this.hpBars.update(alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP);
		}
		
		public function as_updateScore(ally:int, enemy:int):void
		{
			this.score.updateScore(ally, enemy);
		}
		
		public function as_markers(correlationItemsLeft:String, correlationItemsRight:String):void
		{
			if (this.markers)
			{
				this.markers.update_markers(correlationItemsLeft, correlationItemsRight);
			}
		}
		
		override public function onResizeHandle(event:Event):void
		{
			this.x = App.appWidth >> 1;
		}
	}
}