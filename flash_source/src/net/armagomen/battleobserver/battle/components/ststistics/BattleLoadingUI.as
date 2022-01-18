package net.armagomen.battleobserver.battle.components.ststistics
{
	import flash.geom.ColorTransform;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Utils;
	
	public class BattleLoadingUI extends ObserverBattleDisplayable
	{
		private var loading:*;
		public var py_getIconMultiplier:Function;
		private var statisticsEnabled:Boolean = false;
		private var iconEnabled:Boolean       = false;
		private var colorEnabled:Boolean      = false;
		private var iconMultiplier:Number     = -1.25;
		
		public function BattleLoadingUI(loading:*, statsEnabled:Boolean, iconEnabled:Boolean)
		{
			this.loading = loading;
			this.statisticsEnabled = statsEnabled;
			this.iconEnabled = iconEnabled;
			super();
		}
		
		override public function as_onAfterPopulate():void
		{
			this.iconMultiplier = this.py_getIconMultiplier();
		}
		
		private function getHolderByVehicleID(isEnemy:Boolean, vehicleID:int):*
		{
			if (isEnemy)
			{
				for each (var enemy:* in this.loading.form._enemyRenderers)
				{
					if (enemy.model.vehicleID == vehicleID)
					{
						return enemy;
					}
				}
			}
			else
			{
				for each (var ally:* in this.loading.form._allyRenderers)
				{
					if (ally.model.vehicleID == vehicleID)
					{
						return ally;
					}
				}
			}
			return null;
		}
		
		public function as_updateVehicle(isEnemy:Boolean, vehicleID:int, iconColor:String, dataString:String, vehicleTextColor:String):void
		{
			var item:* = this.getHolderByVehicleID(isEnemy, vehicleID);
			if (!item)
			{
				doLog("battle loading item is null ".concat(vehicleID));
				return;
			}
			if (this.iconEnabled)
			{
				var tColor:ColorTransform = new ColorTransform();
				tColor.color = Utils.colorConvert(iconColor);
				tColor.alphaMultiplier = item._vehicleIcon.transform.colorTransform.alphaMultiplier;
				tColor.alphaOffset = item._vehicleIcon.transform.colorTransform.alphaOffset;
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
				item._vehicleIcon.transform.colorTransform = tColor;
			}
			if (this.statisticsEnabled && dataString)
			{
				item._textField.htmlText = dataString;
				if (vehicleTextColor)
				{
					item._vehicleField.textColor = Utils.colorConvert(vehicleTextColor);
				}
			}
		}
	}
}