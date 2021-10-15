package net.armagomen.battleobserver.battle.components.ststistics
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.utils.setTimeout;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Utils;
	import net.wg.gui.battle.components.BattleAtlasSprite;
	import net.wg.data.constants.generated.PLAYERS_PANEL_STATE;
	
	public class PlayersPanelsStatisticUI extends ObserverBattleDisplayable
	{
		
		private var panels:*                  = null;
		public var py_getStatisticString:Function;
		public var py_getIconColor:Function;
		public var py_getStatColor:Function;
		public var py_getIconMultiplier:Function;
		public var py_statisticEnabled:Function;
		public var py_iconEnabled:Function;
		public var py_getCutWidth:Function;
		public var py_getFullWidth:Function;
		private var cached:Object             = new Object();
		private var statisticsEnabled:Boolean = false;
		private var iconEnabled:Boolean       = false;
		private var stringsCache:Object       = new Object();
		private var stringsCacheCut:Object    = new Object();
		private var count:Number              = 0;
		private var colors:Object             = new Object();
		
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
			this.panels.addEventListener(Event.CHANGE, this.onChange);
		}
		
		private function clear():void
		{
			this.removeListeners();
			App.utils.data.cleanupDynamicObject(this.cached);
		}
		
		override protected function onBeforeDispose():void
		{
			this.clear();
			this.panels.removeEventListener(Event.CHANGE, this.onChange);
			super.onBeforeDispose();
		}
		
		private function onChange(eve:Event):void
		{
			this.clear();
			this.createCache();
		}
		
		private function timeout():void
		{
			this.count++;
			if (count < 100)
			{
				setTimeout(this.createCache, 100);
			}
		}
		
		private function createCache():void
		{
			if (!this.panels.listLeft || !this.panels.listLeft._items)
			{
				timeout();
				return;
			}
			for each (var ally:* in this.panels.listRight._items)
			{
				this.cached[ally.vehicleID] = ally;
			}
			for each (var enemy:* in this.panels.listLeft._items)
			{
				this.cached[enemy.vehicleID] = enemy;
			}
			this.addListeners();
		}
		
		/// item._listItem, item.vehicleID, item.accountDBID, item.getVehicleData().vehicleType
		/// item._listItem.playerNameCutTF, item._listItem.playerNameFullTF
		/// item._listItem.vehicleIcon, item._listItem.vehicleTF
		
		private function addListeners():void
		{
			for each (var item:* in this.cached)
			{
				var icon:BattleAtlasSprite = item._listItem.vehicleIcon;
				var tColor:ColorTransform  = icon.transform.colorTransform;
				tColor.color = Utils.colorConvert(py_getIconColor(item.getVehicleData().vehicleType));
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = py_getIconMultiplier();
				icon['cTansform'] = tColor;
				icon['vehicleID'] = item.vehicleID;
				if (!icon.hasEventListener(Event.RENDER))
				{
					icon.addEventListener(Event.RENDER, this.onRenderHendle);
				}
				if (this.statisticsEnabled)
				{
					var accountDBID:int = item.accountDBID;
					if (accountDBID != 0)
					{
						var isEnemy:Boolean = item.getVehicleData().teamColor == "vm_enemy"
						this.stringsCache[accountDBID] = py_getStatisticString(accountDBID, isEnemy, item.getVehicleData().clanAbbrev, false);
						this.stringsCacheCut[accountDBID] = py_getStatisticString(accountDBID, isEnemy, item.getVehicleData().clanAbbrev, true);
						var color:String = py_getStatColor(accountDBID);
						if (color){
							this.colors[accountDBID] = Utils.colorConvert(color);
						}
					}
					item._listItem.playerNameCutTF.width = py_getCutWidth();
					item._listItem.playerNameFullTF.width = py_getFullWidth();
				}
			}
			if (this.statisticsEnabled)
			{
				var oldMode:int = int(this.panels.state);
				this.panels.as_setPanelMode(PLAYERS_PANEL_STATE.HIDDEN);
				this.panels.as_setPanelMode(PLAYERS_PANEL_STATE.FULL);
				this.panels.as_setPanelMode(oldMode);
			}
		}
		
		private function removeListeners():void
		{
			for each (var item:* in this.cached)
			{
				if (!item || !item._listItem || !item._listItem.vehicleIcon)
				{
					continue;
				}
				if (item._listItem.vehicleIcon.hasEventListener(Event.RENDER))
				{
					item._listItem.vehicleIcon.removeEventListener(Event.RENDER, this.onRenderHendle);
				}
			}
		}
		
		private function onRenderHendle(eve:Event):void
		{
			var icon:BattleAtlasSprite = eve.target as BattleAtlasSprite;
			if (this.iconEnabled && icon.transform.colorTransform !== icon['cTansform'])
			{
				icon.transform.colorTransform = icon['cTansform'];
			}
			if (this.statisticsEnabled)
			{
				this.setPlayerText(this.cached[icon['vehicleID']]);
			}
			if (!this.cached[icon['vehicleID']]._listItem._isAlive && (this.statisticsEnabled || this.iconEnabled))
			{
				icon.parent.alpha = 0.6;
			}
		}
		
		private function setPlayerText(item:*):void
		{
			if (item.accountDBID != 0)
			{
				if (this.colors[item.accountDBID])
				{
					item._listItem.vehicleTF.textColor = this.colors[item.accountDBID];
				}
				if (this.stringsCache[item.accountDBID])
				{
					item._listItem.playerNameFullTF.htmlText = this.stringsCache[item.accountDBID];
				}
				if (this.stringsCacheCut[item.accountDBID])
				{
					item._listItem.playerNameCutTF.htmlText = this.stringsCacheCut[item.accountDBID];
				}
			}
		}
	}
}