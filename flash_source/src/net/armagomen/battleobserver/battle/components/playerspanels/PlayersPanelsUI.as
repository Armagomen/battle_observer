package net.armagomen.battleobserver.battle.components.playerspanels
{
	import flash.display.Sprite;
	import flash.events.Event;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.ProgressBar;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.gui.battle.components.stats.playersPanel.SpottedIndicator;
	import net.armagomen.battleobserver.battle.components.playerspanels.ListItem
	
	public class PlayersPanelsUI extends ObserverBattleDisplayable
	{
		private var playersPanel:* = null;
		private var storage:Object = new Object();
		public var onAddedToStorage:Function;
		public var createNewStorage:Function;
		
		public function PlayersPanelsUI(panels:*)
		{
			this.playersPanel = panels;
			super();
		}
		
		public function as_clearStorage():void
		{
			App.utils.data.cleanupDynamicObject(storage);
		}
		
		override protected function onPopulate():void 
		{
			super.onPopulate();
			this.playersPanel.addEventListener(Event.CHANGE, this.onChange);
		}

		override protected function onBeforeDispose():void
		{
			this.as_clearStorage();
			this.playersPanel.removeEventListener(Event.CHANGE, this.onChange);
			super.onBeforeDispose();
		}
		
		private function onChange(eve:Event):void
		{
			this.as_clearStorage();
			this.createNewStorage();
		}
		
		public function as_AddVehIdToList(vehicleID:int, enemy:Boolean):void
		{
			var listitem:* = this.getWGListitem(vehicleID, enemy);
				if (listitem && !listitem.hasOwnProperty("battleObserver")){
				this.storage[vehicleID] = new ListItem(enemy, animationEnabled(), getShadowSettings());
				this.onAddedToStorage(vehicleID, enemy);
				listitem.addChild(this.storage[vehicleID]);
			}
		}
		
		public function as_updateHealthBar(vehicleID:int, scale:Number, text:String):void
		{
			if (this.storage.hasOwnProperty(vehicleID))
			{
				this.storage[vehicleID].updateHealth(scale, text);
			}
		}
		
		public function as_setHealthBarsVisible(vehicles:Array, vis:Boolean):void
		{
			for each (var item:ListItem in storage)
			{
				item.setHealthVisible(vis);
			}
		}
		
		public function as_addHealthBar(vehicleID:int, color:String, colors:Object, settings:Object, team:String, startVisible:Boolean):void
		{
			if (this.storage.hasOwnProperty(vehicleID)){
				this.storage[vehicleID].addHealth(color, colors, settings, startVisible);
			}
		}
		
		public function as_addDamage(vehicleID:int, params:Object):void
		{
			if (this.storage.hasOwnProperty(vehicleID)){
				this.storage[vehicleID].addDamage(params);
			}
		}
		
		public function as_updateDamage(vehicleID:int, text:String):void
		{
			if (this.storage.hasOwnProperty(vehicleID)){
				this.storage[vehicleID].updateDamage(text);
			}
		}
		
		
		public function as_setVehicleDead(vehicleID:int):void
		{
			if (this.storage.hasOwnProperty(vehicleID)){
				this.storage[vehicleID].alpha = 0.6;
				this.storage[vehicleID].updateHealth(0, "");
				this.storage[vehicleID].setHealthVisible(false);
			}
		}
		
		public function as_setSpottedPosition(vehicleID:int):void
		{
			var listitem:* = this.getWGListitem(vehicleID, true);
			if (listitem){
				var spottedIndicator:SpottedIndicator = listitem.spottedIndicator;
				spottedIndicator.scaleX = spottedIndicator.scaleY = 1.5;
				spottedIndicator.y = -6;
				spottedIndicator.x = -335;
			}
			else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_setSpottedPosition - listitem is Null !!!");
		}
		
		public function as_colorBlindPPbars(vehicleID:int, hpColor:String):void
		{
			if (this.storage.hasOwnProperty(vehicleID)){
				this.storage[vehicleID].setColor(hpColor);
			}
		}
		
		public function as_setPlayersDamageVisible(vis:Boolean):void
		{
			if (this.storage){
				for each (var item:ListItem in this.storage){
					item.setDamageVisible(vis);
				}
			}
		}
		
		private function getWGListitem(vehicleID:int, enemy:Boolean):*
		{
			if (playersPanel){
				var list:*   = enemy ? playersPanel.listRight : playersPanel.listLeft;
				var holder:* = list.getHolderByVehicleID(vehicleID);
				if (holder){
					return holder.getListItem();
				}
				else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] getListitem - holder is Null !!!");
			}
			else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] getListitem - playersPanel is Null !!!");
			
			return null;
		}
	}
}