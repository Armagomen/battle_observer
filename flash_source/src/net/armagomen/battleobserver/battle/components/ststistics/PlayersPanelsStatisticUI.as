package net.armagomen.battleobserver.battle.components.ststistics
{
	import flash.events.Event;
	import flash.utils.setTimeout;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.battle.components.ststistics.liasItem.PanelsListItem;
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
		private var count:Number              = 0;
		private var iconMultiplier:Number     = -1.25;
		private var listItems:Vector.<PanelsListItem>;
		
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
			this.listItems = new Vector.<PanelsListItem>();
			this.addListeners();
			this.panels.addEventListener(Event.CHANGE, this.onChange);
			this.panels.addEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.onChange);
		}
		
		private function clear():void
		{
			this.removeListeners();
			this.listItems.splice(0, this.listItems.length);
			this.count = 0;
		}
		
		override protected function onBeforeDispose():void
		{
			this.clear();
			this.listItems = null;
			this.panels.removeEventListener(Event.CHANGE, this.onChange);
			this.panels.removeEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.onChange);
			super.onBeforeDispose();
		}
		
		private function onChange(eve:*):void
		{
			this.clear();
			this.listItems = new Vector.<PanelsListItem>();
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
		
		private function addItemListener(item:*):void
		{
			if (!item.vehicleData || !item._listItem)
			{
				setTimeout(this.addItemListener, 200, item);
			}
			else
			{
				var statistic:Boolean = this.statisticsEnabled && item.accountDBID != 0;
				var listItem:PanelsListItem = new PanelsListItem(item, statistic, this.iconEnabled, this.colorEnabled && item.accountDBID != 0, 
				                                     Utils.colorConvert(py_getIconColor(item.vehicleData.vehicleType)),  
													 this.iconMultiplier);
				
				listItems.push(listItem)
				if (statistic)
				{
					var strings:Array   = py_getStatisticString(item.accountDBID, item.vehicleData.teamColor == "vm_enemy", item.vehicleData.clanAbbrev);
					listItem.setStatisticStrings(strings[0], strings[1], Utils.colorConvert(strings[2]));
				}
				
				if (this.statisticsEnabled){
					item._listItem.playerNameCutTF.width = py_getCutWidth();
					item._listItem.playerNameFullTF.width = py_getFullWidth();
				}
				
				listItem.addListener();
				
			}
		}
		
		private function removeListeners():void
		{
			for each (var listItem:PanelsListItem in this.listItems)
			{
				listItem.removeListener();
			}
		}
	}
}