package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.events.Event;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.battle.interfaces.ITeamHealth;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class TeamsHealthUI extends ObserverBattleDisplayable
	{
		private var hpBars:ITeamHealth;
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
			
			if (settings.style == "league")
			{
				this.hpBars = this.addChild(new League(this.isColorBlind(), this.getColors().global)) as ITeamHealth;
			}
			else
			{
				this.hpBars = this.addChild(new Default(this.isColorBlind(), this.getColors().global)) as ITeamHealth;
			}
			this.as_updateCorrelationBar();
		}
		
		public function as_updateCorrelationBar():void
		{
			var page:*        = parent;
			var correlation:* = page.getComponent(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR);
			if (!this.removed)
			{
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
			correlation._allyVehicleMarkersList._markerStartPosition = -31;
			correlation._enemyVehicleMarkersList._markerStartPosition = 1;
			correlation._allyVehicleMarkersList._isHPBarEnabled = true;
			correlation._enemyVehicleMarkersList._isHPBarEnabled = true;
			correlation._allyVehicleMarkersList.sort(correlation._allyVehicleMarkersList._vehicleIDs);
			correlation._enemyVehicleMarkersList.sort(correlation._enemyVehicleMarkersList._vehicleIDs);
			correlation.y = 10;
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.hpBars.remove();
			this.hpBars = null;
			this.removed = false;
		}
		
		public function as_colorBlind(enabled:Boolean):void
		{
			this.hpBars.setColorBlind(enabled);
		}
		
		public function as_updateHealth(alliesHP:int, enemiesHP:int, totalAlliesHP:int, totalEnemiesHP:int):void
		{
			this.hpBars.update(alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP);
		}
		
		public function as_updateScore(ally:int, enemy:int):void
		{
			this.hpBars.updateScore(ally, enemy);
		}
		
		override public function onResizeHandle(event:Event):void
		{
			this.x = App.appWidth >> 1;
		}
	}
}