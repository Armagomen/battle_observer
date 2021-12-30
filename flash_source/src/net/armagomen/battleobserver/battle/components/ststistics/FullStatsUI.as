package net.armagomen.battleobserver.battle.components.ststistics
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.text.TextFieldAutoSize;
	import flash.utils.setTimeout;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Utils;
	
	public class FullStatsUI extends ObserverBattleDisplayable
	{
		public var py_getStatisticString:Function;
		public var py_getIconColor:Function;
		public var py_getIconMultiplier:Function;
		private var fullStats:*               = null;
		private var statisticsEnabled:Boolean = false;
		private var iconEnabled:Boolean       = false;
		private var iconMultiplier:Number     = -1.25;
		
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
		
		public function as_updateInfo():void
		{
			for each (var ally:* in this.fullStats._tableCtrl._allyRenderers)
			{
				this.updateItem(ally);
			}
			for each (var enemy:* in this.fullStats._tableCtrl._enemyRenderers)
			{
				this.updateItem(enemy);
			}
		}
		
		private function updateItem(item:*):void
		{
			if (this.iconEnabled)
			{
				var tColor:ColorTransform = new ColorTransform();
				tColor.color = Utils.colorConvert(py_getIconColor(item.data.vehicleType));
				tColor.alphaMultiplier = item.statsItem._vehicleIcon.transform.colorTransform.alphaMultiplier;
				tColor.alphaOffset = item.statsItem._vehicleIcon.transform.colorTransform.alphaOffset;
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
				item.statsItem._vehicleIcon.transform.colorTransform = tColor;
			}
			if (this.statisticsEnabled && item.data.accountDBID != 0)
			{
				item.statsItem._playerNameTF.autoSize = item.statsItem._isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT;
				item.statsItem._playerNameTF.htmlText = py_getStatisticString(item.data.accountDBID, item.statsItem._isEnemy, item.data.clanAbbrev);
				if (!item.data.isAlive())
				{
					item.statsItem._playerNameTF.alpha = 0.66;
				}
			}
		}
	}
}