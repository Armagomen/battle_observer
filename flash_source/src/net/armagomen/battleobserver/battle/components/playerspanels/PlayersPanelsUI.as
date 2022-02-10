package net.armagomen.battleobserver.battle.components.playerspanels
{
	import flash.events.Event;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.battle.components.playerspanels.ListItem;
	import net.wg.data.constants.generated.PLAYERS_PANEL_STATE;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.stats.playersPanel.SpottedIndicator;
	
	public class PlayersPanelsUI extends ObserverBattleDisplayable
	{
		private var playersPanel:* = null;
		private var storage:Object = new Object();
		public var onAddedToStorage:Function;
		public var clear:Function;
		private var isReplay:Boolean = false;
		
		public function PlayersPanelsUI(battlePage:*)
		{
			super();
			this.playersPanel = battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
			this.isReplay = battlePage.getComponent(BATTLE_VIEW_ALIASES.CONSUMABLES_PANEL)._isReplay;
		}
		
		public function as_clearStorage():void
		{
			this.clear();
			for each (var item:ListItem in this.storage)
			{
				if (item && item.parent)
				{
					item.removeChildren();
					item.parent.removeChild(item);
				}
			}
			App.utils.data.cleanupDynamicObject(this.storage);
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			if (this.playersPanel)
			{
				this.playersPanel.addEventListener(Event.CHANGE, this.onChange);
			}
		}
		
		override public function setCompVisible(visible:Boolean):void
		{
			super.setCompVisible(visible);
			if (visible && this.playersPanel)
			{
				var oldMode:int = int(this.playersPanel.state);
				this.playersPanel.as_setPanelMode(PLAYERS_PANEL_STATE.HIDDEN);
				this.playersPanel.as_setPanelMode(PLAYERS_PANEL_STATE.FULL);
				this.playersPanel.as_setPanelMode(oldMode);
				this.playersPanel.parent.updateDamageLogPosition();
			}
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			if (this.playersPanel)
			{
				this.as_clearStorage();
				this.playersPanel.removeEventListener(Event.CHANGE, this.onChange);
				this.playersPanel = null;
			}
		}
		
		private function onChange(eve:Event):void
		{
			if (this.isReplay){
				this.as_clearStorage();
				for each (var itemL:* in this.playersPanel.listLeft._items)
				{
					this.as_AddVehIdToList(itemL.vehicleData.vehicleID, false);
				}
			}
			for each (var itemR:* in this.playersPanel.listRight._items)
			{
				this.as_AddVehIdToList(itemR.vehicleData.vehicleID, true);
			}
		}
		
		public function as_AddVehIdToList(vehicleID:int, enemy:Boolean):void
		{
			if (!this.storage[vehicleID])
			{
				var listitem:* = this.getWGListitem(vehicleID, enemy);
				if (listitem)
				{
					this.storage[vehicleID] = new ListItem(enemy, getShadowSettings());
					this.onAddedToStorage(vehicleID, enemy);
					listitem.addChild(this.storage[vehicleID]);
				}
			}
		}
		
		public function as_updateHealthBar(vehicleID:int, scale:Number, text:String):void
		{
			if (this.storage[vehicleID])
			{
				this.storage[vehicleID].updateHealth(scale, text);
			}
		}
		
		public function as_setHealthBarsVisible(vis:Boolean):void
		{
			for each (var item:ListItem in storage)
			{
				item.setHealthVisible(vis);
			}
		}
		
		public function as_addHealthBar(vehicleID:int, color:String, colorParams:Object, settings:Object, startVisible:Boolean):void
		{
			if (this.storage[vehicleID])
			{
				this.storage[vehicleID].addHealth(color, colorParams, settings, startVisible);
			}
		}
		
		public function as_addDamage(vehicleID:int, params:Object):void
		{
			if (this.storage[vehicleID])
			{
				this.storage[vehicleID].addDamage(params);
			}
		}
		
		public function as_updateDamage(vehicleID:int, text:String):void
		{
			if (this.storage[vehicleID])
			{
				this.storage[vehicleID].updateDamage(text);
			}
		}
		
		public function as_setVehicleDead(vehicleID:int):void
		{
			if (this.storage[vehicleID])
			{
				this.storage[vehicleID].setDeath();
			}
		}
		
		public function as_setSpottedPosition(vehicleID:int):void
		{
			var listitem:* = this.getWGListitem(vehicleID, true);
			if (listitem)
			{
				var spottedIndicator:SpottedIndicator = listitem.spottedIndicator;
				spottedIndicator.scaleX = spottedIndicator.scaleY = 1.5;
				spottedIndicator.y = -6;
				spottedIndicator.x = -335;
			}
		}
		
		public function as_colorBlindBars(hpColor:String):void
		{
			for each (var item:ListItem in this.storage)
			{
				if (item.isEnemy)
				{
					item.setColor(hpColor);
				}
			}
		}
		
		public function as_setPlayersDamageVisible(vis:Boolean):void
		{
			for each (var item:ListItem in this.storage)
			{
				item.setDamageVisible(vis);
			}
		}
		
		private function getWGListitem(vehicleID:int, enemy:Boolean):*
		{
			if (this.playersPanel)
			{
				var list:*   = enemy ? this.playersPanel.listRight : this.playersPanel.listLeft;
				var holder:* = list.getHolderByVehicleID(vehicleID);
				if (holder)
				{
					return holder.getListItem();
				}
			}
			return null;
		}
	}
}