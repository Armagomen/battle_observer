package net.armagomen.battleobserver.battle.components.ststistics
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Utils;
	import net.wg.gui.battle.components.BattleAtlasSprite;
	
	public class PlayersPanelsStatisticUI extends ObserverBattleDisplayable
	{
		
		private var panels:*                  = null;
		public var py_getStatisticString:Function;
		public var py_getIconColor:Function;
		public var py_getIconMultiplier:Function;
		public var py_statisticEnabled:Function;
		public var py_iconEnabled:Function;
		public var py_getCutWidth:Function;
		public var py_getFullWidth:Function;
		private var cached:Object             = new Object;
		private var statisticsEnabled:Boolean = false;
		private var iconEnabled:Boolean       = false;
		
		public function PlayersPanelsStatisticUI(panels:*)
		{
			this.panels = panels;
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
			for each (var ally:* in panels.listRight._items)
			{
				this.cached[ally.vehicleID] = ally;
			}
			for each (var enemy:* in panels.listLeft._items)
			{
				this.cached[enemy.vehicleID] = enemy;
			}
		}
		
		/// item._listItem, item.getVehicleData().accountDBID
		/// item._listItem.vehicleTF, item._listItem.playerNameCutTF, item._listItem.playerNameFullTF
		/// item._listItem.vehicleIcon
		/// item._listItem.vehicleTF
		
		private function addListeners():void
		{
			for each (var item:* in this.cached)
			{
				var icon:BattleAtlasSprite = item._listItem.vehicleIcon;
				icon['battleObserver_color'] = Utils.colorConvert(py_getIconColor(item.vehicleID));
				icon['battleObserver_multiplier'] = py_getIconMultiplier();
				icon['battleObserver_vehicleID'] = item.vehicleID;
				if (!icon.hasEventListener(Event.RENDER))
				{
					icon.addEventListener(Event.RENDER, this.onRenderHendle);
				}
				
				if (this.statisticsEnabled)
				{
					item._listItem.playerNameCutTF.width = py_getCutWidth();
					item._listItem.playerNameFullTF.width = py_getFullWidth();
				}
			}
		}
		
		private function removeListeners():void
		{
			for each (var item:* in this.cached)
			{
				if (item._listItem.vehicleIcon.hasEventListener(Event.RENDER))
				{
					item._listItem.vehicleIcon.removeEventListener(Event.RENDER, this.onRenderHendle);
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
		
		private function setPlayerText(item:*):void
		{
			var accountDBID:int = item.getVehicleData().accountDBID;
			if (accountDBID != 0)
			{
				var playerNameHtml:String = py_getStatisticString(accountDBID, item.vehicleID, false);
				if (playerNameHtml){
					item._listItem.playerNameFullTF.htmlText = playerNameHtml;
					item._listItem.playerNameCutTF.htmlText = py_getStatisticString(accountDBID, item.vehicleID, true);
					if (!item._listItem._isAlive)
					{
						item._listItem.playerNameFullTF.alpha = 0.6;
						item._listItem.playerNameCutTF.alpha = 0.6;
					}
				}
			}
		}
	}
}