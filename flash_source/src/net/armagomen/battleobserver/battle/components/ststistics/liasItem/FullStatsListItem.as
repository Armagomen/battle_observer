package net.armagomen.battleobserver.battle.components.ststistics.liasItem
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import net.wg.gui.battle.components.BattleAtlasSprite;
	
	public class FullStatsListItem extends ListItemBase
	{
		
		public function FullStatsListItem(item:*, statisticsEnabled:Boolean, iconEnabled:Boolean, colorEnabled:Boolean, iconColor:uint, multiplier:Number)
		{
			super(item, statisticsEnabled, iconEnabled, colorEnabled, iconColor, multiplier);
		}
		
		private function updateTextFields():void
		{
			this.item.statsItem._playerNameTF.htmlText = this.statStringFull;
		}
		
		override public function onRenderHendle(eve:Event):void
		{
			var icon:BattleAtlasSprite = this.item.statsItem._vehicleIcon;
			if (this.iconEnabled && icon.transform.colorTransform.color != this.iconColor)
			{
				var newTransform:ColorTransform = new ColorTransform();
				newTransform.color = this.iconColor;
				newTransform.alphaMultiplier = icon.transform.colorTransform.alphaMultiplier;
				newTransform.alphaOffset = icon.transform.colorTransform.alphaOffset;
				newTransform.redMultiplier = newTransform.greenMultiplier = newTransform.blueMultiplier = this.iconMultiplier;
				icon.transform.colorTransform = newTransform;
			}
			if (this.statisticsEnabled)
			{
				this.updateTextFields();
			}
		}
		
		public function addListener():void 
		{
			super.addItemListener(this.item.statsItem._vehicleIcon);
		}
		
		public function removeListener():void 
		{
			super.removeItemListener(this.item.statsItem._vehicleIcon);
		}
	}
}

