package net.armagomen.battle_observer.battle.components
{
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.utils.setTimeout;
	import flash.geom.ColorTransform;
	import flash.text.TextFieldAutoSize;
	import flash.text.TextFormat;
	import net.armagomen.battle_observer.utils.Utils;
	import net.wg.data.constants.generated.BATTLEATLAS;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.data.constants.generated.PLAYERS_PANEL_STATE;
	import net.wg.gui.battle.components.events.PlayersPanelListEvent;
	import net.wg.gui.battle.random.views.stats.components.playersPanel.events.PlayersPanelEvent;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	
	public class StatisticsAndIcons extends ObserverBattleDisplayable
	{
		private var battleLoading:*                 = null;
		private var fullStats:*                     = null;
		private var panels:*                        = null;
		private var _isComp7Battle:Boolean          = false;
		
		private var iconColors:Object               = {};
		private var statisticsData:Object           = {};
		private var iconsEnabled:Boolean            = false;
		private var iconMultiplier:Number           = -1.25;
		private var cutWidth:Number                 = 60.0;
		private var fullWidth:Number                = 150.0;
		private static const DEAD_TEXT_ALPHA:Number = 0.65;
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
			this.battleLoading = battlePage.getComponent(BATTLE_VIEW_ALIASES.BATTLE_LOADING);
			this.fullStats = battlePage.getComponent(BATTLE_VIEW_ALIASES.FULL_STATS);
			this.panels = battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
			this._isComp7Battle = this.isComp7Battle();
			this.setIconColors(colors["vehicle_types_colors"]);
			this.iconMultiplier = settings["icons_blackout"];
			this.iconsEnabled = settings["icons"];
			this.cutWidth = settings["statistics_panels_cut_width"];
			this.fullWidth = settings["statistics_panels_full_width"];
			this.addEventListeners();
			setTimeout(this.updateALL, 100);
		}
		
		private function addEventListeners():void
		{
			this.panels.addEventListener(Event.CHANGE, this.onChange, false, 0, true);
			this.panels.addEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.onChange, false, 0, true);
			this.panels.listLeft.addEventListener(MouseEvent.ROLL_OVER, this.onChange, false, 0, true);
			this.panels.listLeft.addEventListener(MouseEvent.ROLL_OUT, this.onChange, false, 0, true);
			this.panels.listRight.addEventListener(MouseEvent.ROLL_OVER, this.onChange, false, 0, true);
			this.panels.listRight.addEventListener(MouseEvent.ROLL_OUT, this.onChange, false, 0, true);
			this.panels.listRight.addEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE, this.onChange, false, 0, true);
		}
		
		private function removeEventListeners():void
		{
			if (this.panels.hasEventListener(Event.CHANGE))
			{
				this.panels.removeEventListener(Event.CHANGE, this.onChange);
			}
			if (this.panels.hasEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE))
			{
				this.panels.removeEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.onChange);
			}
			if (this.panels.listLeft && this.panels.listLeft.hasEventListener(MouseEvent.ROLL_OVER))
			{
				this.panels.listLeft.removeEventListener(MouseEvent.ROLL_OVER, this.onChange);
			}
			if (this.panels.listLeft && this.panels.listLeft.hasEventListener(MouseEvent.ROLL_OUT))
			{
				this.panels.listLeft.removeEventListener(MouseEvent.ROLL_OUT, this.onChange);
			}
			if (this.panels.listRight && this.panels.listRight.hasEventListener(MouseEvent.ROLL_OVER))
			{
				this.panels.listRight.removeEventListener(MouseEvent.ROLL_OVER, this.onChange);
			}
			if (this.panels.listRight && this.panels.listRight.hasEventListener(MouseEvent.ROLL_OUT))
			{
				this.panels.listRight.removeEventListener(MouseEvent.ROLL_OUT, this.onChange);
			}
			if (this.panels.listRight && this.panels.listRight.hasEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE))
			{
				this.panels.listRight.removeEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE, this.onChange);
			}
		}
		
		override protected function onBeforeDispose():void
		{
			this.removeEventListeners();
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
			this.updateALL();
		}
		
		public function as_updateAll(timeout:Number):void
		{
			setTimeout(this.updateALL, timeout);
		}
		
		public function as_updateFullStatsOnkey(timeout:Number):void
		{
			setTimeout(this.updateFullStats, timeout);
		}
		
		private function updateALL():void
		{
			if (this.panels)
			{
				this.updatePlayersPanel();
			}
			if (this.fullStats)
			{
				this.updateFullStats();
			}
			if (this.battleLoading && this.battleLoading.visible && !this._isComp7Battle)
			{
				this.updateBattleloading();
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
		
		private function onChange(eve:Event):void
		{
			setTimeout(this.updateALL, 50);
		}
		
		private function updatePlayersPanel():void
		{
			for each (var itemL:* in this.panels.listLeft._items)
			{
				this.updatePlayersPanelItem(itemL);
			}
			for each (var itemR:* in this.panels.listRight._items)
			{
				this.updatePlayersPanelItem(itemR);
			}
		}
		
		private function updatePlayersPanelItem(holder:*):void
		{
			if (holder.vehicleData && holder.vehicleData.vehicleType != BATTLEATLAS.UNKNOWN)
			{
				var vehicleID:int = holder.vehicleData.vehicleID;
				var listItem:*    = holder.getListItem();
				if (this.iconsEnabled)
				{
					var tColor:ColorTransform = listItem.vehicleIcon.transform.colorTransform;
					tColor.color = this.iconColors[holder.vehicleData.vehicleType];
					tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
					listItem.vehicleIcon.transform.colorTransform = tColor;
				}
				
				if (this.statisticsData[vehicleID])
				{
					if (this.statisticsData[vehicleID].vehicleTextColor)
					{
						listItem.vehicleTF.textColor = Utils.colorConvert(this.statisticsData[vehicleID].vehicleTextColor);
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
		}
		
		private function updateFullStats():void
		{
			var tableCtrl:* = this.fullStats.tableCtrl;
			if (tableCtrl && this.fullStats.visible)
			{
				if (tableCtrl.allyRenderers)
				{
					for each (var ally:* in tableCtrl.allyRenderers)
					{
						this.updateFullStatsItem(ally, false);
					}
				}
				if (tableCtrl.enemyRenderers)
				{
					for each (var enemy:* in tableCtrl.enemyRenderers)
					{
						this.updateFullStatsItem(enemy, true);
					}
				}
			}
		}
		
		private function updateFullStatsItem(holder:*, isEnemy:Boolean):void
		{
			if (holder.data && holder.data.vehicleType != BATTLEATLAS.UNKNOWN)
			{
				var vehicleID:int = holder.data.vehicleID;
				if (this.iconsEnabled)
				{
					var tColor:ColorTransform = holder.statsItem._vehicleIcon.transform.colorTransform;
					tColor.color = this.iconColors[holder.data.vehicleType];
					tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
					holder.statsItem._vehicleIcon.transform.colorTransform = tColor;
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
						holder.statsItem._vehicleNameTF.textColor = Utils.colorConvert(this.statisticsData[vehicleID].vehicleTextColor);
					}
					if (!holder.data.isAlive())
					{
						holder.statsItem._playerNameTF.alpha = DEAD_TEXT_ALPHA;
						holder.statsItem._vehicleNameTF.alpha = DEAD_TEXT_ALPHA;
					}
				}
			}
		}
		
		private function updateBattleloading():void
		{
			var form:* = this.battleLoading.form;
			if (form)
			{
				if (form._enemyRenderers)
				{
					for each (var enemy:* in form._enemyRenderers)
					{
						this.updateBattleloadingItem(enemy);
					}
				}
				if (form._allyRenderers)
				{
					for each (var ally:* in form._allyRenderers)
					{
						this.updateBattleloadingItem(ally);
					}
				}
			}
		}
		
		private function updateBattleloadingItem(holder:*):void
		{
			if (holder.model && holder.model.vehicleType != BATTLEATLAS.UNKNOWN)
			{
				var vehicleID:int = holder.model.vehicleID;
				if (this.iconsEnabled)
				{
					var tColor:ColorTransform = holder._vehicleIcon.transform.colorTransform;
					tColor.color = this.iconColors[holder.model.vehicleType];
					tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
					holder._vehicleIcon.transform.colorTransform = tColor;
				}
				if (this.statisticsData[vehicleID])
				{
					if (this.statisticsData[vehicleID].fullName)
					{
						holder._textField.htmlText = this.statisticsData[vehicleID].fullName;
					}
					if (this.statisticsData[vehicleID].vehicleTextColor)
					{
						holder._vehicleField.textColor = Utils.colorConvert(this.statisticsData[vehicleID].vehicleTextColor);
					}
				}
			}
		}
	}
}