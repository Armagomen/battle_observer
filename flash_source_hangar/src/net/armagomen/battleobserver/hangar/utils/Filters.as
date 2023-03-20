package net.armagomen.battleobserver.hangar.utils
{
	import flash.filters.*;
	import flash.text.TextFormat;
	import net.armagomen.battleobserver.hangar.utils.Utils;
	
	public class Filters
	{
		public static const largeText:TextFormat  = new TextFormat("$TitleFont", 24, 0xFAFAFA);
		public static const mediumText:TextFormat = new TextFormat("$TitleFont", 18, 0xFAFAFA);
		
		public function Filters()
		{
			super();
		}
		
		public static function handleGlowFilter(params:Object):GlowFilter
		{
			var filter:GlowFilter = new GlowFilter()
			filter.color = Utils.colorConvert(params.color);
			filter.alpha = params.alpha;
			filter.blurX = params.blurX;
			filter.blurY = params.blurY;
			filter.inner = params.inner;
			filter.knockout = params.knockout;
			filter.strength = params.strength;
			filter.quality = BitmapFilterQuality.MEDIUM;
			return filter;
		}
	}
}