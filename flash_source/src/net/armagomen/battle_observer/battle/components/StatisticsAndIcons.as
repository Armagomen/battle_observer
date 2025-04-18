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
			
			this.format = new TextFormat();
			this.format.bold = true;
			this.panels = battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
			if (!this.isComp7Battle())
			{
				this.battleLoading = battlePage.getComponent(BATTLE_VIEW_ALIASES.BATTLE_LOADING);
			}
			else
			{
				this.fullStats = battlePage.getComponent(BATTLE_VIEW_ALIASES.FULL_STATS);
			}
			this.setIconColors(colors["vehicle_types_colors"]);
			this.iconMultiplier = settings["icons_blackout"];
			this.iconsEnabled = settings["icons"];
			this.cutWidth = settings["statistics_panels_cut_width"];
			this.fullWidth = settings["statistics_panels_full_width"];
			this.panels.addEventListener(Event.CHANGE, this.onChange, false, 0, true);
			this.panels.addEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.onCountChange, false, 0, true);
			if (this.panels.listRight && !this.panels.listRight.hasEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE))
			{
				this.panels.listRight.addEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE, this.onCountChange, false, 0, true);
			}
			this.updateItems();
		}
		
		override protected function onBeforeDispose():void
		{
			if (this.panels.hasEventListener(Event.CHANGE))
			{
				this.panels.removeEventListener(Event.CHANGE, this.onChange);
			}
			
			if (this.panels.hasEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE))
			{
				this.panels.removeEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.onCountChange);
			}
			
			if (this.panels.listRight && this.panels.listRight.hasEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE))
			{
				this.panels.listRight.removeEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE, this.onCountChange);
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
				//this.statisticsData[key].vehicleTextColor = Utils.colorConvert(statsData[key].vehicleTextColor);
			}
		}
		
		private function onCountChange(eve:Event):void
		{
			for each (var itemR:* in this.panels.listRight._items)
			{
				if (!itemR._listItem.vehicleIcon.hasEventListener(Event.RENDER))
				{
					itemR._listItem.vehicleIcon.addEventListener(Event.RENDER, this.onRenderPanels, false, 0, true);
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
			for each (var itemL:* in this.panels.listLeft._items)
			{
				if (!itemL._listItem.vehicleIcon.hasEventListener(Event.RENDER))
				{
					itemL._listItem.vehicleIcon.addEventListener(Event.RENDER, this.onRenderPanels, false, 0, true);
					itemL._listItem.playerNameCutTF.width = this.cutWidth;
					itemL._listItem.setPlayerNameFullWidth(this.fullWidth);
				}
			}
			
			for each (var itemR:* in this.panels.listRight._items)
			{
				if (!itemR._listItem.vehicleIcon.hasEventListener(Event.RENDER))
				{
					itemR._listItem.vehicleIcon.addEventListener(Event.RENDER, this.onRenderPanels, false, 0, true);
					itemR._listItem.playerNameCutTF.width = this.cutWidth;
					itemR._listItem.setPlayerNameFullWidth(this.fullWidth);
				}
			}
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
			var isEnemy:Boolean = eve.currentTarget.parent._isRightAligned;
			var list:*          = isEnemy ? this.panels.listRight : this.panels.listLeft;
			var holder:*        = list.getItemHolderByIndex(eve.target.parent.holderItemID);
			if (holder)
			{
				var vehicleID:int = holder.vehicleData.vehicleID;
				this.updatePanelsItem(vehicleID, holder);
				
				if (this.fullStats && this.fullStats.visible)
				{
					this.updateFullstats(vehicleID, isEnemy);
				}
				
				if (this.battleLoading && this.battleLoading.visible)
				{
					this.updateBattleloading(vehicleID, isEnemy);
				}
			}
		}
		
		private function updatePanelsItem(vehicleID:int, holder:*):void
		{
			var listItem:* = holder.getListItem();
			if (this.iconsEnabled && holder.vehicleData)
			{
				this.updateVehicleIconColor(listItem.vehicleIcon, holder.vehicleData.vehicleType);
			}

			if (this.statisticsData[vehicleID])
			{
				if (this.statisticsData[vehicleID].vehicleTextColor)
				{
					listItem.vehicleTF.textColor = this.statisticsData[vehicleID].vehicleTextColor;
					listItem.vehicleTF.setTextFormat(this.format);
				}
				if (this.statisticsData[vehicleID].fullName)
				{
					listItem.playerNameFullTF.htmlText = this.statisticsData[vehicleID].fullName;
				}
				if (this.statisticsData[vehicleID].cutName)
				{
					listItem.playerNameCutTF.htmlText = this.statisticsData[vehicleID].cutName;
				}
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
			if (this.iconsEnabled && holder.data)
			{
				this.updateVehicleIconColor(holder.statsItem._vehicleIcon, holder.data.vehicleType);
			}
			if (this.statisticsData[vehicleID])
			{
				if (this.statisticsData[vehicleID].fullName)
				{
					holder.statsItem._playerNameTF.autoSize = isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT;
					holder.statsItem._playerNameTF.htmlText = this.statisticsData[vehicleID].fullName;
				}
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
			if (!holder)
			{
				return;
			}
			if (this.iconsEnabled && holder.model)
			{
				this.updateVehicleIconColor(holder._vehicleIcon, holder.model.vehicleType);
			}
			if (this.statisticsData[vehicleID])
			{
				if (this.statisticsData[vehicleID].fullName)
				{
					holder._textField.htmlText = this.statisticsData[vehicleID].fullName;
				}
				if (this.statisticsData[vehicleID].vehicleTextColor)
				{
					holder._vehicleField.textColor = this.statisticsData[vehicleID].vehicleTextColor;
				}
			}
		}
		
		private function getFullStatsHolderByVehicleID(vehicleID:int, isEnemy:Boolean):*
		{
			var tableCtrl:* = this.fullStats.tableCtrl;
			if (!tableCtrl)
			{
				return null;
			}
			if (isEnemy && tableCtrl.enemyRenderers)
			{
				for each (var enemy:* in tableCtrl.enemyRenderers)
				{
					if (enemy.data && enemy.data.vehicleID == vehicleID)
					{
						return enemy;
					}
				}
			}
			else if (tableCtrl.allyRenderers)
			{
				for each (var ally:* in tableCtrl.allyRenderers)
				{
					if (ally.data && ally.data.vehicleID == vehicleID)
					{
						return ally;
					}
				}
			}
			return null;
		}
		
		private function getLoadingHolderByVehicleID(vehicleID:int, isEnemy:Boolean):*
		{
			var form:* = this.battleLoading.form;
			if (!form || !this.battleLoading.visible)
			{
				return null;
			}
			if (isEnemy && form._enemyRenderers)
			{
				for each (var enemy:* in form._enemyRenderers)
				{
					if (enemy.model && enemy.model.vehicleID == vehicleID)
					{
						return enemy;
					}
				}
			}
			else if (form._allyRenderers)
			{
				for each (var ally:* in form._allyRenderers)
				{
					if (ally.model && ally.model.vehicleID == vehicleID)
					{
						return ally;
					}
				}
			}
			return null;
		}
	}
}