package net.armagomen.battleobserver.battle.components
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.text.TextField;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.utils.Utils;
	import net.wg.gui.battle.components.BattleAtlasSprite;
	
	/**
	 * ...
	 * @author ...
	 */
	public class FullStatsUI extends ObserverBattleDispalaysble
	{
		private var fullStats:* = null;
		public var py_getStatisticString:Function;
		public var py_getIconColor:Function;
		public var py_getIconMultiplier:Function;
		public var onNameChanged:Function;
		private var cached:Object = new Object;
		
		public function FullStatsUI(fullStats:*)
		{
			this.fullStats = fullStats
			super();
		
		}
		
		public function as_showStats(statistics:Boolean, setIcon:Boolean):void
		{

			for each (var ally:* in this.fullStats._tableCtrl._allyRenderers)
			{
				this.cached[ally.data.vehicleID] = ally;
				//if (setIcon)
				//{
				//	this.setVehicleIconColor(ally);
				//}
				if (statistics)
				{
					this.setPlayerText(ally);
				}
				
			}
			for each (var enemy:* in this.fullStats._tableCtrl._enemyRenderers)
			{
				this.cached[enemy.data.vehicleID] = enemy;
				//if (setIcon)
				//{
				//	this.setVehicleIconColor(enemy);
				//}
				if (statistics)
				{
					this.setPlayerText(enemy);
				}
			}
		}
		
		public function as_updateVehicleStatus(data:Object):void
		{
			if (this.cached.hasOwnProperty(data.vehicleID)){
				this.setPlayerText(this.cached[data.vehicleID])
			}
		}
		
		private function onRenderHendle(eve:Event):void
		{
			var icon:BattleAtlasSprite = eve.target as BattleAtlasSprite;
			var tColor:ColorTransform  = icon.transform.colorTransform;
			tColor.color = icon['battleObserver']['color'];
			tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = icon['battleObserver']['multiplier'];
			icon.transform.colorTransform = tColor;
		}
		
		private function setVehicleIconColor(holder:*):void
		{
			var icon:BattleAtlasSprite = holder.statsItem._vehicleIcon;
			icon['battleObserver'] = {"color": Utils.colorConvert(py_getIconColor(holder.data.vehicleID)), "multiplier": py_getIconMultiplier()};
			if (!icon.hasEventListener(Event.RENDER))
			{
				icon.addEventListener(Event.RENDER, this.onRenderHendle);
			}
		}
		
		
		private function setPlayerText(holder:*):void
		{
			if (holder.data.accountDBID != 0){
				holder.statsItem._playerNameTF.autoSize = holder.statsItem._isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT;
				holder.statsItem._playerNameTF.htmlText = py_getStatisticString(holder.data.accountDBID, holder.statsItem._isEnemy);
			}
		}
	}
}