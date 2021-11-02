package net.armagomen.battleobserver.battle.components.ststistics
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.utils.setTimeout;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Utils;
	import net.wg.data.constants.generated.PLAYERS_PANEL_STATE;
	import net.wg.gui.battle.random.views.stats.components.playersPanel.events.PlayersPanelEvent;
	
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
		public var py_vehicleStatisticColorEnabled:Function;
		private var statisticsEnabled:Boolean = false;
		private var iconEnabled:Boolean       = false;
		private var colorEnabled:Boolean      = false;
		private var stringsCache:Object       = new Object();
		private var stringsCacheCut:Object    = new Object();
		private var count:Number              = 0;
		private var colors:Object             = new Object();
		private var iconColors:Object         = new Object();
		private var iconMultiplier:Number     = -1.25;
		
		public function PlayersPanelsStatisticUI(panels:*)
		{
			this.panels = panels;
			super();
		}
		
		override public function as_onAfterPopulate():void
		{
			super.as_onAfterPopulate();
			this.statisticsEnabled = this.py_statisticEnabled();
			this.iconEnabled = this.py_iconEnabled();
			this.colorEnabled = this.py_vehicleStatisticColorEnabled();
			this.iconMultiplier = this.py_getIconMultiplier();
			this.addListeners();
			this.panels.addEventListener(Event.CHANGE, this.onChange);
			this.panels.addEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.onChange);
		}
		
		private function clear():void
		{
			this.removeListeners();
			App.utils.data.cleanupDynamicObject(this.stringsCache);
			App.utils.data.cleanupDynamicObject(this.stringsCacheCut);
			App.utils.data.cleanupDynamicObject(this.colors);
			App.utils.data.cleanupDynamicObject(this.iconColors);
			this.count = 0;
		}
		
		override public function setCompVisible(param0:Boolean):void
		{
			super.setCompVisible(param0);
			if (this.statisticsEnabled)
			{
				var oldMode:int = int(this.panels.state);
				this.panels.as_setPanelMode(PLAYERS_PANEL_STATE.HIDDEN);
				this.panels.as_setPanelMode(PLAYERS_PANEL_STATE.FULL);
				this.panels.as_setPanelMode(oldMode);
				this.panels.parent.updateDamageLogPosition();
			}
		}
		
		override protected function onBeforeDispose():void
		{
			this.clear();
			this.panels.removeEventListener(Event.CHANGE, this.onChange);
			this.panels.removeEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.onChange);
			super.onBeforeDispose();
		}
		
		private function onChange(eve:*):void
		{
			this.clear();
			this.addListeners();
		}
		
		private function timeout():void
		{
			this.count++;
			if (count < 100)
			{
				setTimeout(this.addListeners, 100);
			}
		}
		
		private function addListeners():void
		{
			if (!this.panels.listLeft || !this.panels.listLeft._items)
			{
				timeout();
				return;
			}
			for each (var ally:* in this.panels.listLeft._items)
			{
				this.addItemListener(ally);
			}
			for each (var enemy:* in this.panels.listRight._items)
			{
				this.addItemListener(enemy);
			}
		}
		
		/// item._listItem, item.vehicleID, item.accountDBID, item.getVehicleData().vehicleType
		/// item._listItem.playerNameCutTF, item._listItem.playerNameFullTF
		/// item._listItem.vehicleIcon, item._listItem.vehicleTF
		
		private function addItemListener(item:*):void
		{
			var vehicleData:* = item.getVehicleData();
			if (!item.vehicleData || !item._listItem)
			{
				setTimeout(this.addItemListener, 200, item);
			}
			else
			{
				var icon:* = item._listItem.vehicleIcon;
				if (!this.iconColors[item.vehicleData.vehicleType])
				{
					this.iconColors[item.vehicleData.vehicleType] = Utils.colorConvert(py_getIconColor(item.vehicleData.vehicleType));
				}
				icon.item = item;
				if (!icon.hasEventListener(Event.RENDER))
				{
					icon.addEventListener(Event.RENDER, this.onRenderHendle);
				}
				if (this.statisticsEnabled)
				{
					var accountDBID:int = item.accountDBID;
					if (accountDBID != 0)
					{
						var isEnemy:Boolean = vehicleData.teamColor == "vm_enemy";
						var strings:Array   = py_getStatisticString(accountDBID, isEnemy, vehicleData.clanAbbrev);
						this.stringsCache[accountDBID] = strings[0];
						this.stringsCacheCut[accountDBID] = strings[1];
						if (this.colorEnabled)
						{
							this.colors[accountDBID] = Utils.colorConvert(strings[2]);
						}
					}
					item._listItem.playerNameCutTF.width = py_getCutWidth();
					item._listItem.playerNameFullTF.width = py_getFullWidth();
				}
			}
		}
		
		private function removeListeners():void
		{
			if (!this.panels.listLeft || !this.panels.listLeft._items)
			{
				return;
			}
			for each (var ally:* in this.panels.listLeft._items)
			{
				this.removeItemListener(ally);
			}
			for each (var enemy:* in this.panels.listRight._items)
			{
				this.removeItemListener(enemy);
			}
		}
		
		private function removeItemListener(item:*):void
		{
			if (!item || !item._listItem || !item._listItem.vehicleIcon)
			{
				return;
			}
			if (item._listItem.vehicleIcon.hasEventListener(Event.RENDER))
			{
				item._listItem.vehicleIcon.removeEventListener(Event.RENDER, this.onRenderHendle);
			}
		}
		
		private function onRenderHendle(eve:Event):void
		{
			var icon:* = eve.target;
			if (this.iconEnabled && (icon.transform.colorTransform.color != this.iconColors[icon.item.vehicleData.vehicleType] || icon.transform.colorTransform.color == 0))
			{
				var tColor:ColorTransform = icon.transform.colorTransform;
				tColor.color = this.iconColors[icon.item.vehicleData.vehicleType];
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
				icon.transform.colorTransform = tColor;
			}
			if (this.statisticsEnabled && icon.item.accountDBID != 0)
			{
				this.setPlayerText(icon.item._listItem, icon.item.accountDBID);
			}
		}
		
		private function setPlayerText(listItem:*, accountDBID:int):void
		{
			if (this.colorEnabled)
			{
				listItem.vehicleTF.textColor = this.colors[accountDBID];
			}
			listItem.playerNameFullTF.htmlText = this.stringsCache[accountDBID];
			listItem.playerNameCutTF.htmlText = this.stringsCacheCut[accountDBID];
			if (!listItem._isAlive)
			{
				listItem.playerNameCutTF.alpha = 0.66;
				listItem.playerNameFullTF.alpha = 0.66;
				listItem.vehicleTF.alpha = 0.66;
			}
		}
	}
}