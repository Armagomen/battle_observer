package net.armagomen.battleobserver.battle
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.utils.Utils;
	import net.wg.data.constants.generated.BATTLEATLAS;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.data.constants.generated.PLAYERS_PANEL_STATE;
	import net.wg.gui.battle.random.views.stats.components.playersPanel.events.PlayersPanelEvent;
	
	public class StatisticsAndIcons
	{
		private var battleLoading:*                 = null;
		private var fullStats:*                     = null;
		private var panels:*                        = null;
		private var alis:String						= null;
		
		private var iconColors:Object               = {};
		private var statisticsData:Object           = null;
		private var iconsEnabled:Boolean            = false;
		private var iconMultiplier:Number           = -1.25;
		private var cutWidth:Number                 = 60.0;
		private var fullWidth:Number                = 150.0;
		private static const DEAD_TEXT_ALPHA:Number = 0.68;
		private static const COMP_7_BATTLE:String	= "comp7BattlePage";
		
		public function StatisticsAndIcons(battlePage:*, iconsEnabled:Boolean, statsData:Object, cutWidth:Number, fullWidth:Number, typeColors:Object, iconMultiplier:Number)
		{
			this.battleLoading = battlePage.getComponent(BATTLE_VIEW_ALIASES.BATTLE_LOADING);
			this.fullStats = battlePage.getComponent(BATTLE_VIEW_ALIASES.FULL_STATS);
			this.panels = battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
			this.alis = battlePage.getAlias();
			this.setIconColors(typeColors);
			this.iconMultiplier = iconMultiplier;
			this.statisticsData = statsData;
			this.iconsEnabled = iconsEnabled;
			this.cutWidth = cutWidth;
			this.fullWidth = fullWidth;
			this.panels.addEventListener(Event.CHANGE, this.onChange, false, 0, true);
			this.panels.addEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.onCountChange, false, 0, true);
			this.onChange(null);
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
		
		private function onChange(eve:Event = null):void
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
		
		private function onRenderPanels(eve:Event):void
		{
			var isEnemy:Boolean = eve.currentTarget.parent._isRightAligned;
			var list:*          = isEnemy ? this.panels.listRight : this.panels.listLeft;
			var holder:*        = list.getItemHolderByIndex(eve.target.parent.holderItemID);
			if (holder && holder.vehicleData.vehicleType != BATTLEATLAS.UNKNOWN)
			{
				var listItem:* = holder.getListItem();
				if (this.iconsEnabled)
				{
					var tColor:ColorTransform = listItem.vehicleIcon.transform.colorTransform;
					tColor.color = this.iconColors[holder.vehicleData.vehicleType];
					tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
					listItem.vehicleIcon.transform.colorTransform = tColor;
				}
				var vehicleID:int = holder.vehicleData.vehicleID;
				if (this.statisticsData && this.statisticsData[vehicleID])
				{
					if (this.statisticsData[vehicleID].vehicleTextColor)
					{
						listItem.vehicleTF.textColor = Utils.colorConvert(this.statisticsData[vehicleID].vehicleTextColor);
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
		
		private function updateFullstats(vehicleID:int, isEnemy:Boolean):void
		{
			var holder:* = this.getFullStatsHolderByVehicleID(vehicleID, isEnemy);
			if (!holder)
			{
				return;
			}
			if (this.iconsEnabled && holder.data)
			{
				var tColor:ColorTransform = holder.statsItem._vehicleIcon.transform.colorTransform;
				tColor.color = this.iconColors[holder.data.vehicleType];
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
				holder.statsItem._vehicleIcon.transform.colorTransform = tColor;
			}
			if (this.statisticsData && this.statisticsData[vehicleID])
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
		
		private function updateBattleloading(vehicleID:int, isEnemy:Boolean):void
		{
			var holder:* = this.getLoadingHolderByVehicleID(vehicleID, isEnemy);
			if (!holder)
			{
				return;
			}
			if (this.alis != COMP_7_BATTLE && this.iconsEnabled && holder.model)
			{
				var tColor:ColorTransform = holder._vehicleIcon.transform.colorTransform;
				tColor.color = this.iconColors[holder.model.vehicleType];
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
				holder._vehicleIcon.transform.colorTransform = tColor;
			}
			if (this.statisticsData && this.statisticsData[vehicleID])
			{
				if (this.statisticsData[vehicleID].fullName)
				{
					holder._textField.htmlText = this.statisticsData[vehicleID].fullName;
				}
				if (this.alis != COMP_7_BATTLE && this.statisticsData[vehicleID].vehicleTextColor)
				{
					holder._vehicleField.textColor = Utils.colorConvert(this.statisticsData[vehicleID].vehicleTextColor);
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