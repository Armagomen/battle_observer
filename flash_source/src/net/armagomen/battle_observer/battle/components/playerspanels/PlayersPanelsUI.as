package net.armagomen.battle_observer.battle.components.playerspanels
{
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.utils.setTimeout;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.battle.components.playerspanels.ListItem;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.events.PlayersPanelListEvent;
	import net.wg.gui.battle.components.stats.playersPanel.SpottedIndicator;
	import net.wg.gui.battle.random.views.stats.components.playersPanel.events.PlayersPanelEvent;
	
	public class PlayersPanelsUI extends ObserverBattleDisplayable
	{
		private var panels:*            = null;
		private var storage:Object      = new Object();
		private var spotted_fix:Boolean = false;
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
					item.parent.removeChild(item);
					item.remove();
				}
			}
			App.utils.data.cleanupDynamicObject(this.storage);
		}
		
		override protected function onPopulate():void
		{
			if (not_initialized)
			{
				super.onPopulate();
				this.spotted_fix = this.getSettings().panels_spotted_fix;
				this.panels = this.battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
				if (this.panels)
				{
					this.addListeners();
					setTimeout(this.updateItems, 1000);
				}
			}
			else
			{
				super.onPopulate();
			}
		}
		
		private function addListeners():void
		{
			this.panels.addEventListener(Event.CHANGE, this.updateItems, false, 0, true);
			this.panels.addEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.updateItems, false, 0, true);
			
			if (this.panels.listRight && !this.panels.listRight.hasEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE))
			{
				this.panels.listRight.addEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE, this.updateItems, false, 0, true);
			}
		}
		
		override protected function onBeforeDispose():void
		{
			if (this.panels)
			{
				this.removeListeners();
				this.as_clearStorage();
			}
			super.onBeforeDispose();
		}
		
		private function removeListeners():void
		{
			this.removeListener(this.panels, Event.CHANGE, this.updateItems);
			this.removeListener(this.panels, PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.updateItems);
			this.removeListener(this.panels.listRight, PlayersPanelListEvent.ITEMS_COUNT_CHANGE, this.updateItems);
		}
		
		private function removeListener(target:*, type:String, listener:Function):void
		{
			if (!target) return;
			if (target.hasEventListener(type))
			{
				target.removeEventListener(type, listener);
			}
		}
		
		private function updatePanelItems(items:*):void
		{
			if (items)
			{
				for each (var item:* in items)
				{
					var listItem:* = item._listItem;
					if (this.spotted_fix && listItem._isRightAligned)
					{
						this.setSpottedPosition(listItem);
					}
					this.addVehIdToList(item.vehicleData.vehicleID, listItem);
				}
			}
		}
		
		private function updateItems(eve:Event = null):void
		{
			var targetList:Array = [this.panels.listLeft, this.panels.listRight];
			for each (var list:* in targetList)
			{
				this.updatePanelItems(list._items);
			}
		}
		
		private function addVehIdToList(vehicleID:int, listItem:*):void
		{
			if (!this.storage[vehicleID])
			{
				var enemy:Boolean = listItem._isRightAligned;
				this.storage[vehicleID] = new ListItem(enemy);
				listItem.addChild(this.storage[vehicleID]);
				this.onAddedToStorage(vehicleID, enemy);
			}
			else
			{
				listItem.addChild(this.storage[vehicleID]);
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
		
		private function setSpottedPosition(listitem:*):void
		{
			var spottedIndicator:SpottedIndicator = listitem.spottedIndicator;
			spottedIndicator.scaleX = spottedIndicator.scaleY = 1.5;
			
			var indicator:Sprite = new Sprite();
			indicator.addChild(spottedIndicator);
			listitem.addChild(indicator);
			indicator.x = -45;
			indicator.y = -12;
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
		
		public function as_updateDamageLogPosition():void
		{
			try
			{
				this.battlePage.updateDamageLogPosition();
			}
			catch (err:Error)
			{
				this.battlePage.updateDamageLogPosition(this.battlePage.epicRandomPlayersPanel.state);
			}
		}
	}
}