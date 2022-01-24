package net.armagomen.battleobserver.battle.components.ststistics
{
	import flash.geom.ColorTransform;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Utils;
	import net.wg.data.constants.generated.PLAYERS_PANEL_STATE;
	
	public class PlayersPanelsStatisticUI extends ObserverBattleDisplayable
	{
		public var py_getIconMultiplier:Function;
		public var py_getCutWidth:Function;
		public var py_getFullWidth:Function;
		private var panels:*                        = null;
		private var statisticsEnabled:Boolean       = false;
		private var iconEnabled:Boolean             = false;
		private var colorEnabled:Boolean            = false;
		private var iconMultiplier:Number           = -1.25;
		private static const DEAD_TEXT_ALPHA:Number = 0.68;
		
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
			this.iconMultiplier = this.py_getIconMultiplier();
			var fullWidth:Number = py_getFullWidth();
			var cutWidth:Number  = py_getCutWidth();
			if (this.statisticsEnabled)
			{
				for each (var itemL:* in this.panels.listLeft._items)
				{
					itemL._listItem.playerNameCutTF.width = cutWidth;
					itemL._listItem.setPlayerNameFullWidth(fullWidth);
				}
				for each (var itemR:* in this.panels.listRight._items)
				{
					itemR._listItem.playerNameCutTF.width = cutWidth;
					itemR._listItem.setPlayerNameFullWidth(fullWidth);
				}
			}
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
		
		public function as_updateVehicle(isEnemy:Boolean, vehicleID:int, iconColor:String, fullName:String, cutName:String, vehicleTextColor:String):void
		{
			if (this.panels)
			{
				var list:*   = isEnemy ? this.panels.listRight : this.panels.listLeft;
				var holder:* = list.getHolderByVehicleID(vehicleID);
				if (holder)
				{
					var listItem:* = holder.getListItem();
					if (this.iconEnabled && iconColor)
					{
						var tColor:ColorTransform = listItem.vehicleIcon.transform.colorTransform;
						tColor.color = Utils.colorConvert(iconColor);
						tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
						listItem.vehicleIcon.transform.colorTransform = tColor;
					}
					if (this.statisticsEnabled)
					{
						if (vehicleTextColor)
						{
							listItem.vehicleTF.textColor = Utils.colorConvert(vehicleTextColor);
						}
						if (fullName)
						{
							listItem.playerNameFullTF.htmlText = fullName;
						}
						if (cutName)
						{
							listItem.playerNameCutTF.htmlText = cutName;
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
		}
	
		/// item._listItem, item.vehicleID, item.accountDBID, item.vehicleData.vehicleType
		/// item._listItem.playerNameCutTF, item._listItem.playerNameFullTF
		/// item._listItem.vehicleIcon, item._listItem.vehicleTF
	}
}