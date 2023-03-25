package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.events.Event;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.battle.interfaces.ITeamHealth;
	import net.wg.gui.battle.random.views.fragCorrelationBar.FragCorrelationBar;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class TeamsHealthUI extends ObserverBattleDisplayable
	{
		private var hpBars:ITeamHealth;
		private var score:Score;
		private var removed:Boolean = false;
		
		public function TeamsHealthUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			this.removed = false;
			var settings:Object = this.getSettings();
			this.x = App.appWidth >> 1;
			this.hpBars = this.createHpBars(settings.style);
			this.score = new Score(this.isColorBlind(), this.getColors().global, settings.style);
			this.addChild(this.hpBars);
			this.addChild(this.score);
			this.as_updateCorrelationBar();
		}
		
		public function as_updateCorrelationBar():void
		{
			var correlation:* = parent.getComponent(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR);
			if (!this.removed){
				correlation.removeChild(correlation.getChildAt(0));
				correlation.removeChild(correlation.greenBackground);
				correlation.removeChild(correlation.redBackground);
				correlation.removeChild(correlation.purpleBackground);
				correlation.removeChild(correlation.teamFragsSeparatorField);
				correlation.removeChild(correlation.allyTeamFragsField);
				correlation.removeChild(correlation.enemyTeamFragsField);
				correlation.removeChild(correlation.allyTeamHealthBar);
				correlation.removeChild(correlation.enemyTeamHealthBar);
				this.removed = true;
			}
			correlation._allyVehicleMarkersList._markerStartPosition = -30;
			correlation._enemyVehicleMarkersList._markerStartPosition = 0;
			correlation._allyVehicleMarkersList._isHPBarEnabled = true;
			correlation._enemyVehicleMarkersList._isHPBarEnabled = true;
			correlation._allyVehicleMarkersList.sort(correlation._allyVehicleMarkersList._vehicleIDs);
			correlation._enemyVehicleMarkersList.sort(correlation._enemyVehicleMarkersList._vehicleIDs);
			
			correlation.y = 10;
			this.parent.teamBasesPanelUI.y = 60;
			this.parent.updatePositionForQuestProgress();
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.hpBars.remove();
			this.hpBars = null;
			this.score.removeChildren();
			this.score = null;
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
		
		override public function onResizeHandle(event:Event):void
		{
			this.x = App.appWidth >> 1;
		}
	}
}