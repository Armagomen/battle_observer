package net.armagomen.battleobserver.battle.utils
{
	import flash.filters.BitmapFilterQuality;
	import flash.filters.GlowFilter;
	import flash.text.*;

	public class TextExt extends TextField
	{
		public function TextExt(name:String, x:Number, y:Number, style:TextFormat, align:String, shadowSettings:Object, ui:*)
		{
			super();
			this.name = name;
			this.x = x;
			this.y = y;
			this.width = 1;
			this.defaultTextFormat = style;
			this.antiAliasType = AntiAliasType.ADVANCED;
			this.autoSize = align;
			this.filters = [new GlowFilter(Utils.colorConvert(shadowSettings.color), shadowSettings.alpha, shadowSettings.blurX, shadowSettings.blurY, shadowSettings.strength, BitmapFilterQuality.LOW, shadowSettings.inner, shadowSettings.knockout)];
			this.selectable = false;
			this.multiline = true;
			ui.addChild(this);
		}
	}
}