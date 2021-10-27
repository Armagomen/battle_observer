package net.armagomen.battleobserver.battle.components.ststistics.liasItem 
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import net.wg.gui.battle.components.BattleAtlasSprite;

	
	public class PanelsListItem extends ListItemBase 
	{
		
		public function PanelsListItem(item:*, statisticsEn:Boolean, iconEn:Boolean, colorEn:Boolean, iconCol:uint, multiplier:Number) 
		{
			super(item, statisticsEn, iconEn, colorEn, iconCol, multiplier);
		}
		
		private function updateTextFields():void
		{
			this.item._listItem.playerNameFullTF.htmlText = this.statStringFull;
			this.item._listItem.playerNameCutTF.htmlText = this.statStringCut;
			if (this.colorEnabled){
				this.item._listItem.vehicleTF.textColor = this.vehicleNameColor;
			}
		}

		override public function onRenderHendle(eve:Event):void
		{
			var icon:* = item._listItem.vehicleIcon;
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
			super.addItemListener(item._listItem.vehicleIcon);
		}
		
		public function removeListener():void 
		{
			super.removeItemListener(item._listItem.vehicleIcon);
		}
	}

}