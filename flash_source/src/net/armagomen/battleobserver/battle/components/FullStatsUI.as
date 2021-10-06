package net.armagomen.battleobserver.battle.components
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.text.TextField;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Utils;
	import net.wg.gui.battle.components.BattleAtlasSprite;
	
	public class FullStatsUI extends ObserverBattleDisplayable
	{
		private var fullStats:*               = null;
		public var py_getStatisticString:Function;
		public var py_getIconColor:Function;
		public var py_getIconMultiplier:Function;
		public var py_statisticEnabled:Function;
		public var py_iconEnabled:Function;
		private var cached:Object             = new Object;
		private var statisticsEnabled:Boolean = false;
		private var iconEnabled:Boolean       = false;
		
		public function FullStatsUI(fullStats:*)
		{
			this.fullStats = fullStats
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			this.statisticsEnabled = py_statisticEnabled();
			this.iconEnabled = py_iconEnabled();
			this.createCache();
			this.addListeners();
		}
		
		override protected function onDispose():void
		{
			this.removeListeners();
			App.utils.data.cleanupDynamicObject(this.cached);
			super.onDispose();
		}
		
		private function createCache():void
		{
			for each (var ally:* in this.fullStats._tableCtrl._allyRenderers)
			{
				this.cached[ally.data.vehicleID] = ally;
				
			}
			for each (var enemy:* in this.fullStats._tableCtrl._enemyRenderers)
			{
				this.cached[enemy.data.vehicleID] = enemy;
			}
		}
		
		private function addListeners():void
		{
			for each (var holder:* in this.cached)
			{
				var icon:BattleAtlasSprite = holder.statsItem.vehicleIcon;
				icon['battleObserver_color'] = Utils.colorConvert(py_getIconColor(holder.data.vehicleID));
				icon['battleObserver_multiplier'] = py_getIconMultiplier();
				icon['battleObserver_vehicleID'] = holder.data.vehicleID;
				if (!icon.hasEventListener(Event.RENDER))
				{
					icon.addEventListener(Event.RENDER, this.onRenderHendle);
				}
			}
		}
		
		private function removeListeners():void
		{
			for each (var holder:* in this.cached)
			{
				if (holder.statsItem.vehicleIcon.hasEventListener(Event.RENDER))
				{
					holder.statsItem.vehicleIcon.removeEventListener(Event.RENDER, this.onRenderHendle);
				}
			}
		}
		
		private function onRenderHendle(eve:Event):void
		{
			var icon:BattleAtlasSprite = eve.target as BattleAtlasSprite;
			if (this.iconEnabled)
			{
				this.setVehicleIconColor(icon);
			}
			if (this.statisticsEnabled)
			{
				this.setPlayerText(this.cached[icon['battleObserver_vehicleID']]);
			}
		
		}
		
		private function setVehicleIconColor(icon:BattleAtlasSprite):void
		{
			var tColor:ColorTransform = icon.transform.colorTransform;
			tColor.color = icon['battleObserver_color'];
			tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = icon['battleObserver_multiplier'];
			icon.transform.colorTransform = tColor;
		}
		
		private function setPlayerText(holder:*):void
		{
			if (holder.data.accountDBID != 0)
			{
				var playerName:TextField = holder.statsItem._playerNameTF;
				playerName.autoSize = holder.statsItem._isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT;
				playerName.htmlText = py_getStatisticString(holder.data.accountDBID, holder.statsItem._isEnemy);
				if (!holder.data.isAlive()){
					playerName.alpha = 0.5;
				}
			}
		}
	}
}