package net.armagomen.battle_observer.battle.components.statistics
{
	import flash.utils.Dictionary;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.armagomen.battle_observer.utils.Constants;
	
	public class Statistics extends ObserverBattleDisplayable
	{
		
		private var minimalItems:Dictionary = new Dictionary();
		
		public function Statistics()
		{
			super();
			Constants.statistics = true;
		}
		
		override protected function onBeforeDispose():void
		{
			App.utils.data.cleanupDynamicObject(this.minimalItems);
			super.onBeforeDispose();
		}
		
		public function createItem(vehicleID:int, data:Object):void
		{
			var item:* = this.getPanelHolderByVehicleID(vehicleID, data.isEnemy);
			if (!item || !item._listItem) return;
			
			var listItem:* = item._listItem;
			var oldItem:StatisticItem = this.minimalItems[vehicleID];
			if (oldItem && listItem.contains(oldItem))
			{
				listItem.removeChild(oldItem);
			}
			
			var minimalItem:StatisticItem = new StatisticItem(data, data.isEnemy);
			this.minimalItems[vehicleID] = minimalItem;
			listItem.addChild(minimalItem);
			minimalItem.setVisible(true);
		}
		
		public function as_updateDead(vehicleID:int):void
		{
			var item:* = this.minimalItems[vehicleID];
			if (item) item.setDead(true);
		}
		
		public function on_altMode(enabled:Boolean):void
		{
			for each (var item:* in this.minimalItems)
			{
				item.altMode(enabled);
			}
		}
		
		// holder getters
		
		private function getPanelHolderByVehicleID(vehicleID:int, isEnemy:Boolean):*
		{
			var panels:* = this.battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
			if (panels)
			{
				var list:* = isEnemy ? panels.listRight : panels.listLeft;
				for each (var item:* in list._items)
				{
					if (item.vehicleData.vehicleID == vehicleID)
					{
						return item;
					}
				}
			}
			return null;
		}
		
	}
}