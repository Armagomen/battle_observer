package net.armagomen.battle_observer.battle.components
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.text.TextField;
	import flash.text.TextFieldAutoSize;
	import flash.utils.Dictionary;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.Utils;
	import net.wg.data.constants.generated.BATTLEATLAS;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.events.PlayersPanelListEvent;
	import net.wg.gui.battle.random.views.stats.components.playersPanel.events.PlayersPanelEvent;
	
	public class StatisticsAndIcons extends ObserverBattleDisplayable
	{
		private var battleLoading:* = null;
		private var fullStats:* = null;
		private var panels:* = null;
		private var statisticsData:Dictionary = new Dictionary();
		private var iconsEnabled:Boolean = false;
		private var iconMultiplier:Number = -1.25;
		private var cutWidth:Number = 60.0;
		private var fullWidth:Number = 150.0;
		private var colorCache:Dictionary = new Dictionary();
		private var statisticsLoaded:Boolean = false;
		
		public var getVehicleClassColors:Function;
		
		private static const DEAD_ALT_TEXT_ALPHA:Number = 0.7;
		
		public function StatisticsAndIcons()
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
				this.panels.stage.frameRate = 30;
				this.fullStats = this.battlePage.getComponent(BATTLE_VIEW_ALIASES.FULL_STATS);
				this.setIconColorsCache(this.getVehicleClassColors());
				this.iconMultiplier = settings["icons_blackout"];
				this.iconsEnabled = settings["icons"];
				this.cutWidth = settings["statistics_panels_cut_width"];
				this.fullWidth = settings["statistics_panels_full_width"];
				this.addListeners();
				this.updateItems();
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
			this.removeListeners();
			App.utils.data.cleanupDynamicObject(this.statisticsData);
			App.utils.data.cleanupDynamicObject(this.colorCache);
			this.battleLoading = null;
			this.fullStats = null;
			this.panels = null;
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
		
		public function as_update_wgr_data(statsData:Object):void
		{
			for (var key:String in statsData)
			{
				this.statisticsData[int(key)] = statsData[key];
			}
			App.utils.data.cleanupDynamicObject(statsData);
			this.statisticsLoaded = true;
		}
		
		private function setIconColorsCache(colors:Object):void
		{
			for (var vehicleType:String in colors)
			{
				var tColor:ColorTransform = new ColorTransform();
				tColor.color = Utils.colorConvert(colors[vehicleType]);
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
				this.colorCache[vehicleType] = tColor;
			}
			App.utils.data.cleanupDynamicObject(colors);
		}
		
		private function updatePanelItems(items:*):void
		{
			if (items)
			{
				for each (var item:* in items)
				{
					var vehicleID:int = item.vehicleData.vehicleID;
					var listItem:* = item._listItem;
					listItem.playerNameCutTF.width = this.cutWidth;
					listItem.setPlayerNameFullWidth(this.fullWidth);
					
					this.updateByVehicleID(vehicleID, listItem._isRightAligned);
				}
			}
		}
		
		private function updateItems(eve:Event = null):void
		{
			var targetList:Array = eve && eve.type == PlayersPanelListEvent.ITEMS_COUNT_CHANGE ? [eve.target] : [this.panels.listLeft, this.panels.listRight];
			for each (var list:* in targetList)
			{
				this.updatePanelItems(list._items);
			}
		}
		
		private function updateVehicleIconColor(vehicleIcon:*, vehicleType:String):void
		{
			if (vehicleType != BATTLEATLAS.UNKNOWN && vehicleIcon.transform.colorTransform.color != this.colorCache[vehicleType].color)
			{
				vehicleIcon.transform.colorTransform = this.colorCache[vehicleType];
			}
		}
		
		private function setVehicleTextColor(field:TextField, vehicleTextColor:uint):void
		{
			if (field.visible && vehicleTextColor > 0 && field.textColor != vehicleTextColor)
			{
				field.textColor = vehicleTextColor;
			}
		}
		
		private function updateHtmlText(field:TextField, htmlText:String):void
		{
			if (field.visible)
			{
				field.htmlText = htmlText;
			}
		}
		
		private function updateAutoSize(field:TextField, autoSize:String):void
		{
			if (field.autoSize != autoSize)
			{
				field.autoSize = autoSize;
			}
		}
		
		public function updateByVehicleID(vehicleID:int, isEnemy:Boolean):void
		{
			var item:* = this.getPanelHolderByVehicleID(vehicleID, isEnemy)
			var listItem:* = item._listItem;
			if (this.iconsEnabled)
			{
				this.updateIconsVID(item, isEnemy);
			}
			if (this.statisticsLoaded && this.statisticsData[vehicleID])
			{
				this.updateStatisticsVID(item, isEnemy, this.statisticsData[vehicleID]);
			}
			if (!listItem.isAlive && listItem.playerNameFullTF.alpha != DEAD_ALT_TEXT_ALPHA)
			{
				listItem.playerNameFullTF.alpha = listItem.playerNameCutTF.alpha = listItem.vehicleTF.alpha = listItem.vehicleIcon.alpha = DEAD_ALT_TEXT_ALPHA;
			}
		}
		
		private function updateIconsVID(item:*, isEnemy:Boolean):void
		{
			this.updateVehicleIconColor(item._listItem.vehicleIcon, item.vehicleData.vehicleType);
			if (this.battleLoading.visible)
			{
				var loadingHolder:* = this.getLoadingHolderByVehicleID(item.vehicleData.vehicleID, isEnemy);
				if (loadingHolder && loadingHolder._vehicleIcon)
				{
					this.updateVehicleIconColor(loadingHolder._vehicleIcon, loadingHolder.model.vehicleType);
				}
			}
		}
		
		private function updateStatisticsVID(item:*, isEnemy:Boolean, data:Object):void
		{
			this.setVehicleTextColor(item._listItem.vehicleTF, data.vehicleTextColor);
			this.updateHtmlText(item._listItem.playerNameFullTF, data.fullName);
			this.updateHtmlText(item._listItem.playerNameCutTF, data.cutName);
			if (this.battleLoading.visible)
			{
				var loadingHolder:* = this.getLoadingHolderByVehicleID(item.vehicleData.vehicleID, isEnemy);
				this.updateAutoSize(loadingHolder._textField, loadingHolder._isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT)
				this.updateHtmlText(loadingHolder._textField, data.fullName);
				if (loadingHolder._vehicleField)
				{
					this.setVehicleTextColor(loadingHolder._vehicleField, data.vehicleTextColor);
				}
			}
		}
		
		private function getPanelHolderByVehicleID(vehicleID:int, isEnemy:Boolean):*
		{
			var list:* = isEnemy ? this.panels.listLeft : this.panels.listRight;
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