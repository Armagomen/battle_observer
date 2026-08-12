package net.armagomen.battle_observer.battle.components
{
	
	import flash.display.Bitmap;
	import flash.display.BitmapData;
	import flash.display.DisplayObject;
	import flash.geom.ColorTransform;
	import flash.utils.Dictionary;
	import flash.utils.setTimeout;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.wg.data.constants.generated.BATTLEATLAS;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.events.PlayersPanelListEvent;
	
	public class ColoredIconsUI extends ObserverBattleDisplayable
	{
		private var battleLoading:* = null;
		private var panels:* = null;
		private var iconMultiplier:Number = -1.25;
		private var colorCache:Dictionary = new Dictionary();
		private var iconsUpdated:Dictionary = new Dictionary();
		
		private static const DEAD_ALPHA:Number = 0.7;
		
		public var getConvertedColors:Function;
		
		public function ColoredIconsUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			if (this.notInitialized())
			{
				var settings:Object = this.getSettings();
				this.panels = this.battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
				this.battleLoading = this.battlePage.getComponent(BATTLE_VIEW_ALIASES.BATTLE_LOADING);
				
				this.addListeners();
				this.iconMultiplier = settings["icons_blackout"];
				this.setIconColorsCache();
				if (!this.isComp7Battle()) setTimeout(this.updateAllIcons, 1000);
			}
		}
		
		private function addListeners():void
		{
			
			if (this.panels.listRight)
			{
				this.panels.listRight.addEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE, this.updateAllIcons, false, 0, true);
			}
		}
		
		override protected function onBeforeDispose():void
		{
			this.removeListeners();
			App.utils.data.cleanupDynamicObject(this.colorCache);
			App.utils.data.cleanupDynamicObject(this.iconsUpdated);
			this.battleLoading = null;
			this.panels = null;
			super.onBeforeDispose();
		}
		
		private function removeListeners():void
		{
			
			if (this.panels.listRight)
			{
				this.removeListener(this.panels.listRight, PlayersPanelListEvent.ITEMS_COUNT_CHANGE, this.updateAllIcons);
			}
		}
		
		private function removeListener(target:*, type:String, listener:Function):void
		{
			if (!target) return;
			if (target.hasEventListener(type))
			{
				target.removeEventListener(type, listener);
			}
		}
		
		private function replaceWithSnapshot(vehicleIcon:DisplayObject, vehicleType:String, vehicleID:int, isEnemy:Boolean):void
		{
			
			if (vehicleType == BATTLEATLAS.UNKNOWN) return;
			
			var bmd:BitmapData = new BitmapData(vehicleIcon.width, vehicleIcon.height, true, 0x00000000);
			
			bmd.draw(vehicleIcon);
			
			var copy:Bitmap = new Bitmap(bmd);
			copy.x = vehicleIcon.x;
			copy.y = vehicleIcon.y;
			copy.scaleX = vehicleIcon.scaleX;
			copy.scaleY = vehicleIcon.scaleY;
			copy.rotation = vehicleIcon.rotation;
			
			copy.transform.colorTransform = this.colorCache[vehicleType];
			copy.alpha = 1;
			
			if (isEnemy)
			{
				copy.scaleY *= -1;
			}
			
			if (vehicleIcon.parent)
			{
				var idx:int = vehicleIcon.parent.getChildIndex(vehicleIcon);
				vehicleIcon.parent.addChildAt(copy, idx);
				vehicleIcon.parent.removeChild(vehicleIcon);
			}
			this.iconsUpdated[vehicleID] = copy;
		}
		
		public function updateAllIcons(eve:* = null):void
		{
			var targetList:Array = eve && eve.type == PlayersPanelListEvent.ITEMS_COUNT_CHANGE ? [eve.target] : [this.panels.listLeft, this.panels.listRight];
			for each (var list:* in targetList)
			{
				for each (var item:* in list._items)
				{
					if (!item || !item._listItem || this.iconsUpdated[item.vehicleData.vehicleID]) continue;
					
					var isEnemy:Boolean = item._listItem._isRightAligned;
					
					var loadingHolder:* = this.getLoadingHolderByVehicleID(item.vehicleData.vehicleID, isEnemy);
					if (loadingHolder && loadingHolder._vehicleIcon)
					{
						this.replaceWithSnapshot(loadingHolder._vehicleIcon, loadingHolder.model.vehicleType, item.vehicleData.vehicleID, isEnemy);
					}
					
					this.replaceWithSnapshot(item._listItem.vehicleIcon, item.vehicleData.vehicleType, item.vehicleData.vehicleID, isEnemy);
				}
			}
		}
		
		private function setIconColorsCache():void
		{
			var colors:Object = this.getConvertedColors()
			for (var vehicleType:String in colors)
			{
				var tColor:ColorTransform = new ColorTransform();
				tColor.color = colors[vehicleType];
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier - 0.4;
				this.colorCache[vehicleType] = tColor;
			}
		}
		
		public function as_on_killed(vehicleID:int):void
		{
			if (this.iconsUpdated[vehicleID])
			{
				this.iconsUpdated[vehicleID].alpha = DEAD_ALPHA;
			}
		}
		
		// holder getters
		
		private function getPanelHolderByVehicleID(vehicleID:int, isEnemy:Boolean):*
		{
			var list:* = isEnemy ? this.panels.listRight : this.panels.listLeft;
			for each (var item:* in list._items)
			{
				if (item.vehicleData.vehicleID == vehicleID)
				{
					return item;
				}
			}
			return null;
		}
		
		private function getLoadingHolderByVehicleID(vehicleID:int, isEnemy:Boolean):*
		{
			var form:* = this.battleLoading.form;
			if (form)
			{
				var renderers:* = isEnemy ? form._enemyRenderers : form._allyRenderers;
				for each (var render:* in renderers)
				{
					if (render.model.vehicleID == vehicleID)
					{
						return render;
					}
				}
			}
			return null;
		}
	
	}

}