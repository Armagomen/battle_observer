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
		private var playersPanel:*      = null;
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
				var battlePage:* = parent;
				this.playersPanel = battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
				if (this.playersPanel)
				{
					this.playersPanel.addEventListener(Event.CHANGE, this.reloadAll, false, 0, true);
					this.playersPanel.addEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.reloadAll, false, 0, true);
					this.playersPanel.listRight.addEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE, this.addToRight, false, 0, true);
					setTimeout(this.loadLists, 100);
				}
			}
			else
			{
				super.onPopulate();
			}
		}
		
		override protected function onBeforeDispose():void
		{
			if (this.playersPanel)
			{
				this.as_clearStorage();
				if (this.playersPanel.hasEventListener(Event.CHANGE))
				{
					this.playersPanel.removeEventListener(Event.CHANGE, this.reloadAll);
				}
				
				if (this.playersPanel.hasEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE))
				{
					this.playersPanel.removeEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.reloadAll);
				}
				
				if (this.playersPanel.listRight)
				{
					this.playersPanel.listRight.removeEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE, this.addToRight);
				}
				this.playersPanel = null;
			}
			super.onBeforeDispose();
		}
		
		private function addToRight(eve:Event = null):void
		{
			if (this.playersPanel)
			{
				for each (var item:* in this.playersPanel.listRight._items)
				{
					this.addVehIdToList(item.vehicleData.vehicleID, true, item._listItem);
					if (this.spotted_fix)
					{
						this.setSpottedPosition(item._listItem);
					}
				}
			}
		}
		
		private function loadLists():void
		{
			if (this.playersPanel)
			{
				for each (var item:* in this.playersPanel.listLeft._items)
				{
					this.addVehIdToList(item.vehicleData.vehicleID, false, item._listItem);
				}
				this.addToRight();
			}
		}
		
		private function reloadAll(eve:Event):void
		{
			this.loadLists();
		}
		
		private function addVehIdToList(vehicleID:int, enemy:Boolean, item:*):void
		{
			if (!this.storage[vehicleID])
			{
				this.storage[vehicleID] = new ListItem(enemy);
				item.addChild(this.storage[vehicleID]);
				this.onAddedToStorage(vehicleID, enemy);
			}
			else
			{
				item.addChild(this.storage[vehicleID]);
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