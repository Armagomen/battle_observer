package net.armagomen.battleobserver.battle.components.ststistics.liasItem
{
	import flash.text.TextField;
	import net.wg.gui.battle.components.BattleAtlasSprite;
	import flash.events.Event;
	import flash.geom.ColorTransform;
	
	public class ListItemBase
	{
		public var item:*;
		public var iconColor:uint;
		public var iconMultiplier:Number = -1.25;
		public var statStringCut:String;
		public var statStringFull:String;
		public var vehicleNameColor:uint;
		public var statisticsEnabled:Boolean = false;
		public var iconEnabled:Boolean       = false;
		public var colorEnabled:Boolean      = false;
		
		public function ListItemBase(_item:*, statisticsEn:Boolean, iconEn:Boolean, colorEn:Boolean, iconCol:uint, multiplier:Number)
		{
			this.item = _item;
			this.iconColor = iconCol;
			this.iconMultiplier = multiplier;
			this.statisticsEnabled = statisticsEn;
			this.iconEnabled = iconEn;
			this.colorEnabled = colorEn;
		}
		
		public function setStatisticStrings(full:String, cut:String = null, nameColor:uint = undefined):void
		{
			this.statStringFull = full;
			this.statStringCut = cut;
			this.vehicleNameColor = nameColor;
		}
		
		public function addItemListener(icon:*):void
		{
			if (!icon.hasEventListener(Event.RENDER))
			{
				icon.addEventListener(Event.RENDER, this.onRenderHendle);
			}
		}
		
		public function removeItemListener(icon:*):void
		{
			if (icon.hasEventListener(Event.RENDER))
			{
				icon.removeEventListener(Event.RENDER, this.onRenderHendle);
			}

			this.iconColor = undefined;
			this.iconMultiplier = undefined;
			this.statisticsEnabled = undefined;
			this.iconEnabled = undefined;
			this.colorEnabled = undefined;
			this.statStringFull = null;
			this.statStringCut = null;
			this.vehicleNameColor = undefined;
		}
		
		public function onRenderHendle(eve:Event):void{}
	}
}