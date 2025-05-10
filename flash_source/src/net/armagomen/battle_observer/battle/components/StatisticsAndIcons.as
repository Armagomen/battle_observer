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
		private var battleLoading:*           = null;
		private var fullStats:*               = null;
		private var panels:*                  = null;
		private var statisticsData:Dictionary = new Dictionary();
		private var iconsEnabled:Boolean      = false;
		private var iconMultiplier:Number     = -1.25;
		private var cutWidth:Number           = 60.0;
		private var fullWidth:Number          = 150.0;
		private var colorCache:Dictionary     = new Dictionary();
		private var statisticsLoaded:Boolean  = false;
		private var holdersCache:Array        = new Array();
		
		private static const DEAD_ALT_TEXT_ALPHA:Number = 0.73;
		
		public function StatisticsAndIcons()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			
			if (not_initialized)
			{
				super.onPopulate();
				this.holdersCache[0] = new Dictionary();
				this.holdersCache[1] = new Dictionary();
				
				var settings:Object = this.getSettings();
				var colors:Object = this.getColors();
				this.panels = this.battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
				this.battleLoading = this.battlePage.getComponent(BATTLE_VIEW_ALIASES.BATTLE_LOADING);
				this.panels.stage.frameRate = 30;
				this.fullStats = this.battlePage.getComponent(BATTLE_VIEW_ALIASES.FULL_STATS);
				this.setIconColorsCache(colors["vehicle_types_colors"]);
				this.iconMultiplier = settings["icons_blackout"];
				this.iconsEnabled = settings["icons"];
				this.cutWidth = settings["statistics_panels_cut_width"];
				this.fullWidth = settings["statistics_panels_full_width"];
				this.addListeners();
				this.updateItems();
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
			this.removeListeners();
			for each (var item:* in this.holdersCache)
			{
				App.utils.data.cleanupDynamicObject(item);
			}
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
			
			this.removeEventListeners(this.panels.listRight);
			this.removeEventListeners(this.panels.listLeft);
		}
		
		private function removeEventListeners(list:*):void
		{
			if (!list) return;
			for each (var item:Object in list._items)
			{
				this.removeListener(item.getListItem().vehicleIcon, Event.RENDER, onRenderPanels);
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
					var listItem:*    = item._listItem;
					if (!listItem.vehicleIcon.hasEventListener(Event.RENDER))
					{
						listItem.vehicleIcon.addEventListener(Event.RENDER, this.onRenderPanels, false, 0, true);
					}
					listItem["item"] = item;
					listItem.playerNameCutTF.width = this.cutWidth;
					listItem.setPlayerNameFullWidth(this.fullWidth);
					this.holdersCache[0][vehicleID] = this.getLoadingHolderByVehicleID(vehicleID, listItem._isRightAligned);
					this.holdersCache[1][vehicleID] = this.getFullStatsHolderByVehicleID(vehicleID, listItem._isRightAligned);
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
		
		private function onRenderPanels(eve:Event):void
		{
			var listItem:*    = eve.target.parent;
			var vehicleID:int = listItem.item.vehicleData.vehicleID;
			if (this.iconsEnabled)
			{
				this.updateIcons(listItem, this.holdersCache[0][vehicleID], this.holdersCache[1][vehicleID]);
			}
			if (this.statisticsLoaded && this.statisticsData[vehicleID])
			{
				this.updateStatistics(listItem, this.holdersCache[0][vehicleID], this.holdersCache[1][vehicleID], this.statisticsData[vehicleID]);
			}
		}
		
		private function updateIcons(listItem:*, loadingHolder:*, statsHolder:*):void
		{
			if (this.panels.visible)
			{
				this.updateVehicleIconColor(listItem.vehicleIcon, listItem.item.vehicleData.vehicleType);
			}
			if (this.battleLoading.visible && loadingHolder && loadingHolder._vehicleIcon)
			{
				this.updateVehicleIconColor(loadingHolder._vehicleIcon, loadingHolder.model.vehicleType);
			}
			if (this.fullStats.visible && statsHolder)
			{
				this.updateVehicleIconColor(statsHolder.statsItem._vehicleIcon, statsHolder.data.vehicleType);
			}
		}
		
		private function updateStatistics(listItem:*, loadingHolder:*, statsHolder:*, data:Object):void
		{
			if (this.panels.visible)
			{
				this.setVehicleTextColor(listItem.vehicleTF, data.vehicleTextColor);
				this.updateHtmlText(listItem.playerNameFullTF, data.fullName);
				this.updateHtmlText(listItem.playerNameCutTF, data.cutName);
				if (listItem.deadAltBg.visible)
				{
					listItem.playerNameFullTF.alpha = listItem.playerNameCutTF.alpha = listItem.vehicleTF.alpha = listItem.deadAltBg.visible ? DEAD_ALT_TEXT_ALPHA : listItem._originalTFAlpha;
				}
			}
			if (this.battleLoading.visible && loadingHolder)
			{
				this.updateAutoSize(loadingHolder._textField, loadingHolder._isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT)
				this.updateHtmlText(loadingHolder._textField, data.fullName);
				if (loadingHolder._vehicleField)
				{
					this.setVehicleTextColor(loadingHolder._vehicleField, data.vehicleTextColor);
				}
			}
			if (this.fullStats.visible && statsHolder)
			{
				this.updateAutoSize(statsHolder.statsItem._playerNameTF, statsHolder.statsItem._isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT);
				this.updateHtmlText(statsHolder.statsItem._playerNameTF, data.fullName);
				this.setVehicleTextColor(statsHolder.statsItem._vehicleNameTF, data.vehicleTextColor);
			}
		}
		
		private function getFullStatsHolderByVehicleID(vehicleID:int, isEnemy:Boolean):*
		{
			var tableCtrl:* = this.fullStats.tableCtrl;
			if (tableCtrl)
			{
				var renderers:* = isEnemy ? tableCtrl.enemyRenderers : tableCtrl.allyRenderers;
				for each (var render:* in renderers)
				{
					if (render.data.vehicleID == vehicleID)
					{
						return render;
					}
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