package net.armagomen.battleobserver.battle.components.ststistics.liasItem
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import net.wg.gui.battle.components.BattleAtlasSprite;
	
	public class BattleLoadingListItem extends ListItemBase
	{
		
		public function BattleLoadingListItem(item:*, statisticsEn:Boolean, iconEn:Boolean, colorEn:Boolean, iconCol:uint, multiplier:Number)
		{
			super(item, statisticsEn, iconEn, colorEn, iconCol, multiplier);
		}
		
		private function updateTextFields():void
		{
			this.item._textField.htmlText = this.statStringFull;
		}
			
		override public function onRenderHendle(eve:Event):void
		{
			var icon:BattleAtlasSprite = this.item._vehicleIcon;
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
			this.addItemListener(this.item._vehicleIcon);
		}
		
		public function removeListener():void 
		{
			this.removeItemListener(this.item._vehicleIcon);
		}
	}
}
