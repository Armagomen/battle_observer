package net.armagomen.battleobserver.battle.components.ststistics
{
	import flash.geom.ColorTransform;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Utils;
	
	public class FullStatsUI extends ObserverBattleDisplayable
	{
		public var py_getIconMultiplier:Function;
		private var fullStats:*                     = null;
		private var statisticsEnabled:Boolean       = false;
		private var iconEnabled:Boolean             = false;
		private var iconMultiplier:Number           = -1.25;
		//private static const DEAD_TEXT_ALPHA:Number = 0.68;
		
		public function FullStatsUI(fullStats:*, statsEnabled:Boolean, iconEnabled:Boolean)
		{
			this.fullStats = fullStats;
			this.statisticsEnabled = statsEnabled;
			this.iconEnabled = iconEnabled;
			super();
		}
		
		override public function as_onAfterPopulate():void
		{
			this.iconMultiplier = py_getIconMultiplier();
		}
		
		private function getHolderByVehicleID(isEnemy:Boolean, vehicleID:int):*
		{
			if (isEnemy)
			{
				for each (var enemy:* in this.fullStats._tableCtrl._enemyRenderers)
				{
					if (enemy.data.vehicleID == vehicleID)
					{
						return enemy;
					}
				}
			}
			else
			{
				for each (var ally:* in this.fullStats._tableCtrl._allyRenderers)
				{
					if (ally.data.vehicleID == vehicleID)
					{
						return ally;
					}
				}
			}
			return null;
		}
		
		public function as_updateVehicle(isEnemy:Boolean, vehicleID:int, iconColor:String, fullName:String, cutName:String, vehicleTextColor:String):void
		{
			var item:* = this.getHolderByVehicleID(isEnemy, vehicleID);
			if (!item)
			{
				doLog("full stats item is null ".concat(vehicleID));
				return;
			}
			if (this.iconEnabled && iconColor)
			{
				var tColor:ColorTransform = new ColorTransform();
				tColor.color = Utils.colorConvert(iconColor);
				tColor.alphaMultiplier = item.statsItem._vehicleIcon.transform.colorTransform.alphaMultiplier;
				tColor.alphaOffset = item.statsItem._vehicleIcon.transform.colorTransform.alphaOffset;
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
				item.statsItem._vehicleIcon.transform.colorTransform = tColor;
			}
			if (this.statisticsEnabled)
			{
				if (fullName)
				{
					item.statsItem._playerNameTF.autoSize = isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT;
					item.statsItem._playerNameTF.htmlText = fullName;
				}
				if (vehicleTextColor)
				{
					item.statsItem._vehicleNameTF.textColor = Utils.colorConvert(vehicleTextColor);
				}
				//if (!item.data.isAlive())
				//{
					//item.statsItem._playerNameTF.alpha = DEAD_TEXT_ALPHA;
					//item.statsItem._vehicleNameTF.alpha = DEAD_TEXT_ALPHA;
				//}
			}
		}
	}
}