package net.armagomen.battle_observer.battle.components.playerspanels
{
	import flash.display.Shape;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.utils.setTimeout;
	import flash.utils.clearTimeout;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.battle.components.playerspanels.ListItem;
	import net.wg.data.constants.generated.PLAYERS_PANEL_STATE;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.stats.playersPanel.SpottedIndicator;
	
	public class PlayersPanelsUI extends ObserverBattleDisplayable
	{
		private var timeoutID:Number;
		private var playersPanel:* = null;
		private var storage:Object = new Object();
		public var onAddedToStorage:Function;
		
		public function PlayersPanelsUI()
		{
			super();
		}
		
		public function as_clearStorage():void
		{
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
			var battlePage:* = parent;
			this.playersPanel = battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
			if (this.playersPanel)
			{
				this.playersPanel.addEventListener(Event.CHANGE, this.onChange);
			}
			super.onPopulate();
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
		
		private function reloadLists():void
		{
			this.as_clearStorage();
			for each (var itemL:* in this.playersPanel.listLeft._items)
			{
				this.as_AddVehIdToList(itemL.vehicleData.vehicleID, false);
			}
			for each (var itemR:* in this.playersPanel.listRight._items)
			{
				this.as_AddVehIdToList(itemR.vehicleData.vehicleID, true);
			}
		}
		
		private function onChange(eve:Event):void
		{
			if (this.timeoutID)
			{
				clearTimeout(this.timeoutID);
			}
			this.timeoutID = setTimeout(this.reloadLists, 1000);
		}
		
		public function as_AddVehIdToList(vehicleID:int, enemy:Boolean):void
		{
			if (!this.storage[vehicleID])
			{
				var listitem:* = this.getWGListitem(vehicleID, enemy);
				if (listitem)
				{
					this.storage[vehicleID] = new ListItem(enemy);
					listitem.addChild(this.storage[vehicleID]);
					this.onAddedToStorage(vehicleID, enemy);
				}
				else
				{
					DebugUtils.LOG_WARNING("[BATTLE_OBSERVER]: playersPanel list item holder is null: " + vehicleID.toString());
				}
			}
		}
		
		public function as_updateHealthBar(vehicleID:int, percent:Number, text:String):void
		{
			if (this.storage[vehicleID])
			{
				this.storage[vehicleID].updateHealth(percent, text);
			}
		}
		
		public function as_setHealthBarsVisible(vis:Boolean):void
		{
			for each (var item:ListItem in storage)
			{
				item.setHealthVisible(vis);
			}
		}
		
		public function as_addHealthBar(vehicleID:int, color:String, visible:Boolean):void
		{
			if (this.storage[vehicleID])
			{
				this.storage[vehicleID].addHealth(color, this.getColors().global, visible);
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
				
				var indicator:Sprite = new Sprite();
				indicator.addChild(spottedIndicator);
				listitem.addChild(indicator);
				indicator.x = -45;
				indicator.y = -12;
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
				DebugUtils.LOG_WARNING("[BATTLE_OBSERVER]: playersPanel list item holder is not found: " + vehicleID.toString());
			}
			return null;
		}
		
		public function as_updateDamageLogPosition():void
		{
			var page:* = parent;
			try
			{
				page.updateDamageLogPosition();
			}
			catch (err:Error)
			{
				page.updateDamageLogPosition(page.epicRandomPlayersPanel.state);
			}
		}
	}
}