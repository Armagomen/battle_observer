package net.armagomen.battle_observer.battle.components
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.text.TextFieldAutoSize;
	import flash.text.TextFormat;
	import flash.utils.setTimeout;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.Utils;
	import net.wg.data.constants.generated.BATTLEATLAS;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.events.PlayersPanelListEvent;
	import net.wg.gui.battle.random.views.stats.components.playersPanel.events.PlayersPanelEvent;
	
	public class StatisticsAndIcons extends ObserverBattleDisplayable
	{
		private var battleLoading:*                 = null;
		private var fullStats:*                     = null;
		private var panels:*                        = null;
		private var iconColors:Object               = {};
		private var statisticsData:Object           = {};
		private var iconsEnabled:Boolean            = false;
		private var iconMultiplier:Number           = -1.25;
		private var cutWidth:Number                 = 60.0;
		private var fullWidth:Number                = 150.0;
		private static const DEAD_TEXT_ALPHA:Number = 0.68;
		private var format:TextFormat;
		private var _statisticsEnabled:Boolean      = false;
		
		public var statisticsEnabled:Function;
		
		public function StatisticsAndIcons()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			var battlePage:*    = this.parent;
			var settings:Object = this.getSettings();
			var colors:Object   = this.getColors();
			
			this._statisticsEnabled = this.statisticsEnabled();
			this.format = new TextFormat();
			this.format.bold = true;
			this.panels = battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
			if (this.isComp7Battle())
			{
				this.fullStats = battlePage.getComponent(BATTLE_VIEW_ALIASES.FULL_STATS);
			}
			else
			{
				this.battleLoading = battlePage.getComponent(BATTLE_VIEW_ALIASES.BATTLE_LOADING);
			}
			this.setIconColors(colors["vehicle_types_colors"]);
			this.iconMultiplier = settings["icons_blackout"];
			this.iconsEnabled = settings["icons"];
			this.cutWidth = settings["statistics_panels_cut_width"];
			this.fullWidth = settings["statistics_panels_full_width"];
			this.panels.addEventListener(Event.CHANGE, this.onChange, false, 0, true);
			this.panels.addEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.updateRight, false, 0, true);
			if (this.panels.listRight && !this.panels.listRight.hasEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE))
			{
				this.panels.listRight.addEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE, this.updateRight, false, 0, true);
			}
			setTimeout(this.updateItems, 200);
		}
		
		override protected function onBeforeDispose():void
		{
			if (this.panels.hasEventListener(Event.CHANGE))
			{
				this.panels.removeEventListener(Event.CHANGE, this.onChange);
			}
			
			if (this.panels.hasEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE))
			{
				this.panels.removeEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.updateRight);
			}
			
			if (this.panels.listRight && this.panels.listRight.hasEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE))
			{
				this.panels.listRight.removeEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE, this.updateRight);
			}
			this.battleLoading = null;
			this.fullStats = null;
			this.panels = null;
			super.onBeforeDispose();
		}
		
		public function as_update_wgr_data(statsData:Object):void
		{
			for (var key:String in statsData)
			{
				this.statisticsData[key] = statsData[key];
			}
			App.utils.data.cleanupDynamicObject(statsData);
		}
		
		private function updateRight(eve:Event = null):void
		{
			for each (var item:* in this.panels.listRight._items)
			{
				if (!item._listItem.vehicleIcon.hasEventListener(Event.RENDER))
				{
					item._listItem.vehicleIcon.addEventListener(Event.RENDER, this.onRenderPanels, false, 0, true);
					item._listItem["item"] = item;
					item._listItem.playerNameCutTF.width = this.cutWidth;
					item._listItem.setPlayerNameFullWidth(this.fullWidth);
				}
			}
		}
		
		private function setIconColors(colors:Object):void
		{
			for (var classTag:String in colors)
			{
				this.iconColors[classTag] = Utils.colorConvert(colors[classTag]);
			}
			App.utils.data.cleanupDynamicObject(colors);
		}
		
		private function updateItems():void
		{
			for each (var item:* in this.panels.listLeft._items)
			{
				if (!item._listItem.vehicleIcon.hasEventListener(Event.RENDER))
				{
					item._listItem.vehicleIcon.addEventListener(Event.RENDER, this.onRenderPanels, false, 0, true);
					item._listItem["item"] = item;
					item._listItem.playerNameCutTF.width = this.cutWidth;
					item._listItem.setPlayerNameFullWidth(this.fullWidth);
				}
			}
			this.updateRight();
		}
		
		private function onChange(eve:Event):void
		{
			setTimeout(this.updateItems, 1000);
		}
		
		private function updateVehicleIconColor(vehicleIcon:*, vehicleType:String):void
		{
			if (vehicleType != BATTLEATLAS.UNKNOWN)
			{
				var tColor:ColorTransform = vehicleIcon.transform.colorTransform;
				tColor.color = this.iconColors[vehicleType];
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
				vehicleIcon.transform.colorTransform = tColor;
			}
		}
		
		private function onRenderPanels(eve:Event):void
		{
			var listItem:*    = eve.target.parent;
			var vehicleID:int = listItem.item.vehicleData.vehicleID;
			
			if (this.iconsEnabled)
			{
				this.updateVehicleIconColor(eve.target, listItem.item.vehicleData.vehicleType);
			}
			if (this._statisticsEnabled)
			{
				this.updatePanelsItem(vehicleID, listItem);
			}
			
			if (this.battleLoading && this.battleLoading.visible)
			{
				this.updateBattleloading(vehicleID, listItem._isRightAligned);
			}
			
			if (this.fullStats && this.fullStats.visible)
			{
				this.updateFullstats(vehicleID, listItem._isRightAligned);
			}
		}
		
		private function updatePanelsItem(vehicleID:int, listItem:*):void
		{
			if (this.statisticsData[vehicleID])
			{
				if (this.statisticsData[vehicleID].vehicleTextColor)
				{
					listItem.vehicleTF.textColor = this.statisticsData[vehicleID].vehicleTextColor;
					listItem.vehicleTF.setTextFormat(this.format);
				}
				listItem.playerNameFullTF.htmlText = this.statisticsData[vehicleID].fullName;
				listItem.playerNameCutTF.htmlText = this.statisticsData[vehicleID].cutName;
				if (!listItem._isAlive)
				{
					listItem.playerNameCutTF.alpha = DEAD_TEXT_ALPHA;
					listItem.playerNameFullTF.alpha = DEAD_TEXT_ALPHA;
					listItem.vehicleTF.alpha = DEAD_TEXT_ALPHA;
				}
			}
		}
		
		private function updateFullstats(vehicleID:int, isEnemy:Boolean):void
		{
			var holder:* = this.getFullStatsHolderByVehicleID(vehicleID, isEnemy);
			if (!holder)
			{
				return;
			}
			if (this.iconsEnabled)
			{
				this.updateVehicleIconColor(holder.statsItem._vehicleIcon, holder.data.vehicleType);
			}
			if (this._statisticsEnabled && this.statisticsData[vehicleID])
			{
				holder.statsItem._playerNameTF.autoSize = isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT;
				holder.statsItem._playerNameTF.htmlText = this.statisticsData[vehicleID].fullName;
				if (this.statisticsData[vehicleID].vehicleTextColor)
				{
					holder.statsItem._vehicleNameTF.textColor = this.statisticsData[vehicleID].vehicleTextColor;
				}
				if (!holder.data.isAlive())
				{
					holder.statsItem._playerNameTF.alpha = DEAD_TEXT_ALPHA;
					holder.statsItem._vehicleNameTF.alpha = DEAD_TEXT_ALPHA;
				}
			}
		}
		
		private function updateBattleloading(vehicleID:int, isEnemy:Boolean):void
		{
			var holder:* = this.getLoadingHolderByVehicleID(vehicleID, isEnemy);
			if (holder)
			{
				if (this.iconsEnabled && holder._vehicleIcon)
				{
					this.updateVehicleIconColor(holder._vehicleIcon, holder.model.vehicleType);
				}
				if (this._statisticsEnabled && this.statisticsData[vehicleID])
				{
					holder._textField.htmlText = this.statisticsData[vehicleID].fullName;
					if (this.statisticsData[vehicleID].vehicleTextColor)
					{
						holder._vehicleField.textColor = this.statisticsData[vehicleID].vehicleTextColor;
					}
				}
			}
		
		}
		
		private function getFullStatsHolderByVehicleID(vehicleID:int, isEnemy:Boolean):*
		{
			var tableCtrl:* = this.fullStats.tableCtrl;
			if (tableCtrl)
			{
				if (isEnemy && tableCtrl.enemyRenderers)
				{
					for each (var enemy:* in tableCtrl.enemyRenderers)
					{
						if (enemy.data.vehicleID == vehicleID)
						{
							return enemy;
						}
					}
				}
				else if (tableCtrl.allyRenderers)
				{
					for each (var ally:* in tableCtrl.allyRenderers)
					{
						if (ally.data.vehicleID == vehicleID)
						{
							return ally;
						}
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
				if (isEnemy && form._enemyRenderers)
				{
					for each (var enemy:* in form._enemyRenderers)
					{
						if (enemy.model.vehicleID == vehicleID)
						{
							return enemy;
						}
					}
				}
				else if (form._allyRenderers)
				{
					for each (var ally:* in form._allyRenderers)
					{
						if (ally.model.vehicleID == vehicleID)
						{
							return ally;
						}
					}
				}
			}
			return null;
		}
	}
}