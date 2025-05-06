package net.armagomen.battle_observer.utils
{
	import flash.filters.GlowFilter;
	import flash.text.*;
	import net.armagomen.battle_observer.utils.Constants;
	
	public class TextExt extends TextField
	{
		public function TextExt(x:Number, y:Number, format:TextFormat, align:String, ui:*, enabled:Boolean = true)
		{
			super();
			if (format == null)
			{
				format = Constants.normalText;
			}
			this.x = x;
			this.y = y;
			this.width = 1;
			this.defaultTextFormat = format;
			this.antiAliasType = AntiAliasType.ADVANCED;
			this.autoSize = align;
			this.filters = [new GlowFilter(0, 0.6, 2, 2, 4)];
			this.selectable = false;
			this.multiline = true;
			this.visible = enabled;
			this.htmlText = "";
			ui.addChild(this);
		}
	}
}