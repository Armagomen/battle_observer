package net.armagomen.battleobserver.hangar.utils
{
	import flash.filters.GlowFilter;
	import flash.text.*;
	
	public class TextExt extends TextField
	{
		public function TextExt(name:String, x:Number, y:Number, style:TextFormat, align:String, ui:*)
		{
			super();
			this.name = name;
			this.x = x;
			this.y = y;
			this.width = 1;
			this.defaultTextFormat = style;
			this.antiAliasType = AntiAliasType.ADVANCED;
			this.autoSize = align;
			this.filters = [new GlowFilter(0, 0.7, 2, 2, 6)];
			this.selectable = false;
			this.multiline = true;
			ui.addChild(this);
		}
	}
}