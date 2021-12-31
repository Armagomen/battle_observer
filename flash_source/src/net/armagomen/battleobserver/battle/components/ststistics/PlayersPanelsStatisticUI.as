package net.armagomen.battleobserver.battle.components.ststistics
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.utils.setTimeout;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Utils;
	import net.wg.data.constants.generated.PLAYERS_PANEL_STATE;
	import net.wg.gui.battle.random.views.stats.components.playersPanel.events.PlayersPanelEvent;
	
	public class PlayersPanelsStatisticUI extends ObserverBattleDisplayable
	{
		public var py_getStatisticString:Function;
		public var py_getIconColor:Function;
		public var py_getIconMultiplier:Function;
		public var py_getCutWidth:Function;
		public var py_getFullWidth:Function;
		public var py_vehicleStatisticColorEnabled:Function;
		private var panels:*                  = null;
		private var statisticsEnabled:Boolean = false;
		private var iconEnabled:Boolean       = false;
		private var colorEnabled:Boolean      = false;
		private var iconMultiplier:Number     = -1.25;
		
		public function PlayersPanelsStatisticUI(panels:*, statsEnabled:Boolean, icon:Boolean)
		{
			this.panels = panels;
			this.statisticsEnabled = statsEnabled;
			this.iconEnabled = icon;
			super();
		}
		
		override public function as_onAfterPopulate():void
		{
			super.as_onAfterPopulate();
			this.colorEnabled = this.py_vehicleStatisticColorEnabled();
			this.iconMultiplier = this.py_getIconMultiplier();
		}
		
		override public function setCompVisible(param0:Boolean):void
		{
			super.setCompVisible(param0);
			if (this.statisticsEnabled && param0)
			{
				var oldMode:int = int(this.panels.state);
				this.panels.as_setPanelMode(PLAYERS_PANEL_STATE.HIDDEN);
				this.panels.as_setPanelMode(PLAYERS_PANEL_STATE.FULL);
				this.panels.as_setPanelMode(oldMode);
				this.panels.parent.updateDamageLogPosition();
			}
		}
		
		override protected function onBeforeDispose():void
		{
			this.panels = null;
			super.onBeforeDispose();
		}
				
		public function as_updateVehicle(isEnemy:Boolean, vehicleID:int):void
		{
			if (this.panels)
			{
				var list:*   = isEnemy ? this.panels.listRight : this.panels.listLeft;
				var holder:* = list.getHolderByVehicleID(vehicleID);
				if (holder)
				{
					this.udateInfo(holder.getListItem(), holder.vehicleData, holder.accountDBID, isEnemy);
				}
			}
		}
		
		/// item._listItem, item.vehicleID, item.accountDBID, item.vehicleData.vehicleType
		/// item._listItem.playerNameCutTF, item._listItem.playerNameFullTF
		/// item._listItem.vehicleIcon, item._listItem.vehicleTF
		private function udateInfo(listItem:*, vehicleData:*, accountDBID:int, isEnemy:Boolean):void
		{
			if (this.iconEnabled)
			{
				var tColor:ColorTransform = listItem.vehicleIcon.transform.colorTransform;
				tColor.color = Utils.colorConvert(py_getIconColor(vehicleData.vehicleType));
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
				listItem.vehicleIcon.transform.colorTransform = tColor;
			}
			if (this.statisticsEnabled)
			{
				if (accountDBID != 0)
				{
					this.setPlayerText(listItem, py_getStatisticString(accountDBID, isEnemy, vehicleData.clanAbbrev));
				}
				listItem.playerNameCutTF.width = py_getCutWidth();
				listItem.playerNameFullTF.width = py_getFullWidth();
			}
		}
		
		private function setPlayerText(listItem:*, data:Array):void
		{
			if (this.colorEnabled && data[2])
			{
				listItem.vehicleTF.textColor = data[2];
			}
			if (data[0])
			{
				listItem.playerNameFullTF.htmlText = data[0];
			}
			if (data[1])
			{
				listItem.playerNameCutTF.htmlText = data[1];
			}
			if (!listItem._isAlive)
			{
				listItem.playerNameCutTF.alpha = 0.66;
				listItem.playerNameFullTF.alpha = 0.66;
				listItem.vehicleTF.alpha = 0.66;
			}
		}
	}
}