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
		public var py_getStatColor:Function;
		public var py_getIconMultiplier:Function;
		public var py_statisticEnabled:Function;
		public var py_iconEnabled:Function;
		public var py_getCutWidth:Function;
		public var py_getFullWidth:Function;
		private var statisticsEnabled:Boolean = false;
		private var iconEnabled:Boolean       = false;
		private var stringsCache:Object       = new Object();
		private var stringsCacheCut:Object    = new Object();
		private var count:Number              = 0;
		private var colors:Object             = new Object();
		private var iconColors:Object         = new Object();
		
		public function PlayersPanelsStatisticUI(panels:*)
		{
			this.panels = panels;
			super();
		}
		
		override public function as_onAfterPopulate():void
		{
			super.as_onAfterPopulate();
			this.statisticsEnabled = py_statisticEnabled();
			this.iconEnabled = py_iconEnabled();
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
			for each (var ally:* in this.panels.listRight._items)
			{
				this.addListener(ally);
			}
			for each (var enemy:* in this.panels.listLeft._items)
			{
				this.addListener(enemy);
			}
			if (this.statisticsEnabled)
			{
				var oldMode:int = int(this.panels.state);
				this.panels.as_setPanelMode(PLAYERS_PANEL_STATE.HIDDEN);
				this.panels.as_setPanelMode(PLAYERS_PANEL_STATE.FULL);
				this.panels.as_setPanelMode(oldMode);
				this.panels.parent.updateDamageLogPosition();
			}
		}
		
		/// item._listItem, item.vehicleID, item.accountDBID, item.getVehicleData().vehicleType
		/// item._listItem.playerNameCutTF, item._listItem.playerNameFullTF
		/// item._listItem.vehicleIcon, item._listItem.vehicleTF
		
		private function addListener(item:*):void
		{
			var icon:* = item._listItem.vehicleIcon;
			icon.bo_color = Utils.colorConvert(py_getIconColor(item.getVehicleData().vehicleType));
			icon.bo_mulpipier = py_getIconMultiplier();
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
					var isEnemy:Boolean = item.getVehicleData().teamColor == "vm_enemy"
					this.stringsCache[accountDBID] = py_getStatisticString(accountDBID, isEnemy, item.getVehicleData().clanAbbrev, false);
					this.stringsCacheCut[accountDBID] = py_getStatisticString(accountDBID, isEnemy, item.getVehicleData().clanAbbrev, true);
					var color:String = py_getStatColor(accountDBID);
					if (color)
					{
						this.colors[accountDBID] = Utils.colorConvert(color);
					}
				}
				item._listItem.playerNameCutTF.width = py_getCutWidth();
				item._listItem.playerNameFullTF.width = py_getFullWidth();
			}
		}
		
		private function removeListeners():void
		{
			if (!this.panels.listLeft || !this.panels.listLeft._items)
			{
				return;
			}
			for each (var ally:* in this.panels.listRight._items)
			{
				this.removeListener(ally);
			}
			for each (var enemy:* in this.panels.listLeft._items)
			{
				this.removeListener(enemy);
			}
		}
		
		private function removeListener(item:*):void
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
			if (icon.transform.colorTransform.color == icon.bo_color)
			{
				return;
			}
			if (this.iconEnabled)
			{
				var tColor:ColorTransform = icon.transform.colorTransform;
				tColor.color = icon.bo_color;
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = icon.bo_mulpipier;
				icon.transform.colorTransform = tColor;
			}
			if (this.statisticsEnabled)
			{
				this.setPlayerText(icon.item);
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
				if (!item._listItem._isAlive)
				{
					item._listItem.playerNameCutTF.alpha = 0.6;
					item._listItem.playerNameFullTF.alpha = 0.6;
					item._listItem.vehicleTF.alpha = 0.6;
				}
			}
		}
	}
}