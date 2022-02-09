package net.armagomen.battleobserver.battle 
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.utils.Utils;
	import net.wg.data.constants.generated.PLAYERS_PANEL_STATE;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;

	public class StatisticsAndIcons 
	{
		private var battleLoading:* = null;
		private var fullStats:* = null;
		private var panels:* = null;
		
		private var statisticsData:Object = null;
		private var statisticsEnabled:Boolean       = false;
		private var iconsEnabled:Boolean            = false;
	
		
		private static const DEAD_TEXT_ALPHA:Number = 0.68;
		
		public function StatisticsAndIcons(battlePage:*, statisticsEnabled:Boolean, iconsEnabled:Boolean, data:Object, cutWidth:Number, fullWidth:Number) 
		{
			this.battleLoading = battlePage.getComponent(BATTLE_VIEW_ALIASES.BATTLE_LOADING);
			this.fullStats = battlePage.getComponent(BATTLE_VIEW_ALIASES.FULL_STATS);
			this.panels = battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
			this.statisticsData = data;
			this.statisticsEnabled = statisticsEnabled;
			this.iconsEnabled = iconsEnabled;
			this.addListeners(cutWidth, fullWidth)
		}
		
		public function addListeners(cutWidth:Number, fullWidth:Number):void
		{		
			for each (var itemL:* in this.panels.listLeft._items)
			{
				itemL._listItem.vehicleIcon.addEventListener(Event.RENDER, this.onRenderPanels, false, 0, true);
				itemL._listItem.playerNameCutTF.width = cutWidth;
				itemL._listItem.setPlayerNameFullWidth(fullWidth);
			}
			
			for each (var itemR:* in this.panels.listRight._items)
			{
				itemR._listItem.vehicleIcon.addEventListener(Event.RENDER, this.onRenderPanels, false, 0, true);
				itemR._listItem.playerNameCutTF.width = cutWidth;
				itemR._listItem.setPlayerNameFullWidth(fullWidth);
			}
			if (this.statisticsEnabled)
			{
				var oldMode:int = int(this.panels.state);
				this.panels.as_setPanelMode(PLAYERS_PANEL_STATE.HIDDEN);
				this.panels.as_setPanelMode(PLAYERS_PANEL_STATE.FULL);
				this.panels.as_setPanelMode(oldMode);
				this.panels.parent.updateDamageLogPosition();
			}
		}
		
		
		private function onRenderPanels(eve:Event):void
		{
			var isEnemy:Boolean = eve.target.parent._isRightAligned;
			var list:*   = isEnemy ? this.panels.listRight : this.panels.listLeft;
			var holder:* = list.getItemHolderByIndex(eve.target.parent.holderItemID);
			var vehicleData:Object = this.statisticsData[holder.vehicleData.vehicleID];
			if (holder && vehicleData)
			{
				var listItem:* = holder.getListItem();
				if (this.iconsEnabled && vehicleData.iconColor)
				{
					var tColor:ColorTransform = listItem.vehicleIcon.transform.colorTransform;
					tColor.color = Utils.colorConvert(vehicleData.iconColor);
					tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = vehicleData.iconMultiplier;
					listItem.vehicleIcon.transform.colorTransform = tColor;
				}
				if (this.statisticsEnabled)
				{
					if (vehicleData.vehicleTextColor)
					{
						listItem.vehicleTF.textColor = Utils.colorConvert(vehicleData.vehicleTextColor);
					}
					if (vehicleData.fullName)
					{
						listItem.playerNameFullTF.htmlText = vehicleData.fullName;
					}
					if (vehicleData.cutName)
					{
						listItem.playerNameCutTF.htmlText = vehicleData.cutName;
					}
					if (!listItem._isAlive)
					{
						listItem.playerNameCutTF.alpha = DEAD_TEXT_ALPHA;
						listItem.playerNameFullTF.alpha = DEAD_TEXT_ALPHA;
						listItem.vehicleTF.alpha = DEAD_TEXT_ALPHA;
					}
				}
				if (this.fullStats && this.fullStats.visible){
					this.updateFullstats(holder.vehicleData.vehicleID, vehicleData, isEnemy);
				}
				
				if (this.battleLoading && this.battleLoading.visible){
					this.updateBattleloading(holder.vehicleData.vehicleID, vehicleData, isEnemy);
				}
			}
		}
		
		private function updateFullstats(vehicleID:int, vehicleData:Object, isEnemy:Boolean):void
		{
			var holder:* = this.getFullStatsHolderByVehicleID(vehicleID, isEnemy);
			if (!holder)
			{
				return;
			}
			if (this.iconsEnabled && vehicleData.iconColor)
			{
				var tColor:ColorTransform = new ColorTransform();
				tColor.color = Utils.colorConvert(vehicleData.iconColor);
				tColor.alphaMultiplier = holder.statsItem._vehicleIcon.transform.colorTransform.alphaMultiplier;
				tColor.alphaOffset = holder.statsItem._vehicleIcon.transform.colorTransform.alphaOffset;
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = vehicleData.iconMultiplier;
				holder.statsItem._vehicleIcon.transform.colorTransform = tColor;
			}
			if (this.statisticsEnabled)
			{
				if (vehicleData.fullName)
				{
					holder.statsItem._playerNameTF.autoSize = isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT;
					holder.statsItem._playerNameTF.htmlText = vehicleData.fullName;
				}
				if (vehicleData.vehicleTextColor)
				{
					holder.statsItem._vehicleNameTF.textColor = Utils.colorConvert(vehicleData.vehicleTextColor);
				}
				if (!holder.data.isAlive())
				{
					holder.statsItem._playerNameTF.alpha = DEAD_TEXT_ALPHA;
					holder.statsItem._vehicleNameTF.alpha = DEAD_TEXT_ALPHA;
				}
			}
		}
		
		private function updateBattleloading(vehicleID:int, vehicleData:Object, isEnemy:Boolean):void
		{
			var holder:* = this.getLoadingHolderByVehicleID(vehicleID, isEnemy);
			if (!holder)
			{
				return;
			}
			if (this.iconsEnabled && vehicleData.iconColor)
			{
				var tColor:ColorTransform = new ColorTransform();
				tColor.color = Utils.colorConvert(vehicleData.iconColor);
				tColor.alphaMultiplier = holder._vehicleIcon.transform.colorTransform.alphaMultiplier;
				tColor.alphaOffset = holder._vehicleIcon.transform.colorTransform.alphaOffset;
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = vehicleData.iconMultiplier;
				holder._vehicleIcon.transform.colorTransform = tColor;
			}
			if (this.statisticsEnabled)
			{
				if (vehicleData.fullName)
				{
					holder._textField.htmlText = vehicleData.fullName;
				}
				if (vehicleData.vehicleTextColor)
				{
					holder._vehicleField.textColor = Utils.colorConvert(vehicleData.vehicleTextColor);
				}
			}
		}
		
		private function getFullStatsHolderByVehicleID(vehicleID:int, isEnemy:Boolean):*
		{
			var tableCtrl:* = this.fullStats._tableCtrl;
			if (!tableCtrl){
				return null;
			}
			if (isEnemy && tableCtrl._enemyRenderers)
			{
				for each (var enemy:* in tableCtrl._enemyRenderers)
				{
					if (enemy.data && enemy.data.vehicleID == vehicleID)
					{
						return enemy;
					}
				}
			}
			else if (tableCtrl._allyRenderers)
			{
				for each (var ally:* in tableCtrl._allyRenderers)
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
			if (!form || !this.battleLoading.visible){
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