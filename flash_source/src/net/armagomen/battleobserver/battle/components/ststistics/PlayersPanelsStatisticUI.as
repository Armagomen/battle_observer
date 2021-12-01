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
		public var py_getStatisticString:Function;
		public var py_getIconColor:Function;
		public var py_getIconMultiplier:Function;
		public var py_getCutWidth:Function;
		public var py_getFullWidth:Function;
		public var py_vehicleStatisticColorEnabled:Function;
		private var panels:*                  = null;
		private var statisticsEnabled:Boolean = false;
		private var iconEnabled:Boolean       = false;
		private var colorEnabled:Boolean      = false;
		private var dataCache:Object       = new Object();;
		private var colors:Object             = new Object();
		private var iconsColors:Object        = new Object();
		private var iconMultiplier:Number     = -1.25;
		
		public function PlayersPanelsStatisticUI(panels:*, statsEnabled:Boolean, icon:Boolean)
		{
			this.panels = panels;
			this.statisticsEnabled = statsEnabled;
			this.iconEnabled = icon;
			super();
		}
		
		override public function as_onAfterPopulate():void
		{
			super.as_onAfterPopulate();
			this.colorEnabled = this.py_vehicleStatisticColorEnabled();
			this.iconMultiplier = this.py_getIconMultiplier();
			setTimeout(this.addListeners, 3000);
			this.panels.addEventListener(Event.CHANGE, this.onChange);
			this.panels.addEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.onChange);
		}
		
		private function clear():void
		{
			this.removeListeners();
			if (App.instance && App.utils)
			{
				App.utils.data.cleanupDynamicObject(this.dataCache);
				App.utils.data.cleanupDynamicObject(this.colors);
				App.utils.data.cleanupDynamicObject(this.iconsColors);
			}
		}
		
		override public function setCompVisible(param0:Boolean):void
		{
			super.setCompVisible(param0);
			if (this.statisticsEnabled && param0)
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
			this.dataCache = null;
			this.colors = null;
			this.iconsColors = null;
			this.panels = null;
			super.onBeforeDispose();
		}
		
		private function onChange(eve:*):void
		{
			this.clear();
			this.addListeners();
		}
		
		private function addListeners():void
		{
			if (!this.panels.listLeft || !this.panels.listLeft._items)
			{
				setTimeout(this.addListeners, 1000);
			}
			else
			{
				for each (var ally:* in this.panels.listLeft._items)
				{
					this.addItemListener(ally);
				}
				for each (var enemy:* in this.panels.listRight._items)
				{
					this.addItemListener(enemy);
				}
			}
		}
		
		/// item._listItem, item.vehicleID, item.accountDBID, item.vehicleData.vehicleType
		/// item._listItem.playerNameCutTF, item._listItem.playerNameFullTF
		/// item._listItem.vehicleIcon, item._listItem.vehicleTF
		
		private function addItemListener(item:*):void
		{
			if (!item.vehicleData || !item._listItem || !item.vehicleData.vehicleType)
			{
				setTimeout(this.addItemListener, 1000, item);
			}
			else
			{
				if (this.iconEnabled)
				{
					var typeColor:String = py_getIconColor(item.vehicleData.vehicleType);
					if (!this.iconsColors[item.vehicleData.vehicleType] && typeColor)
					{
						this.iconsColors[item.vehicleData.vehicleType] = Utils.colorConvert(typeColor);
					}
				}
				var icon:* = item._listItem.vehicleIcon;
				icon.item = item;
				if (!icon.hasEventListener(Event.RENDER))
				{
					icon.addEventListener(Event.RENDER, this.onRenderHendle, false, 0, true);
				}
				if (this.statisticsEnabled)
				{
					var accountDBID:int = item.accountDBID;
					if (accountDBID != 0)
					{
						var isEnemy:Boolean = item.vehicleData.teamColor == "vm_enemy";
						this.dataCache[accountDBID] = py_getStatisticString(accountDBID, isEnemy, item.vehicleData.clanAbbrev);
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
			if (this.iconEnabled)
			{
				var iconColor:uint    = icon.transform.colorTransform.color;
				var newIconColor:uint = this.iconsColors[icon.item.vehicleData.vehicleType];
				if (iconColor != newIconColor || iconColor == 0)
				{
					var tColor:ColorTransform = icon.transform.colorTransform;
					tColor.color = newIconColor;
					tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
					icon.transform.colorTransform = tColor;
				}
			}
			var accountDBID:int = icon.item.accountDBID;
			if (this.statisticsEnabled && this.dataCache[accountDBID])
			{
				this.setPlayerText(icon.item._listItem, this.dataCache[accountDBID]);
			}
		}
		
		private function setPlayerText(listItem:*, data:Array):void
		{
			if (this.colorEnabled && data[2])
			{
				listItem.vehicleTF.textColor = data[2];
			}
			if (data[0]){
				listItem.playerNameFullTF.htmlText = data[0];
			}
			if (data[1]){
				listItem.playerNameCutTF.htmlText = data[1];
			}
			if (!listItem._isAlive)
			{
				listItem.playerNameCutTF.alpha = 0.66;
				listItem.playerNameFullTF.alpha = 0.66;
				listItem.vehicleTF.alpha = 0.66;
			}
		}
	}
}