package net.armagomen.battleobserver.utils
{
	import net.armagomen.battleobserver.utils.Utils;
	import flash.filters.*;
	import flash.text.TextFormat;

	public class Filters
	{
		public static const glowScore:GlowFilter = new GlowFilter(0, 0.9, 4, 4, 2, BitmapFilterQuality.LOW, false, false);
		public static const middleText:TextFormat = new TextFormat("$TitleFont", 18, 0xFAFAFA);
		public static const largeText:TextFormat = new TextFormat("$TitleFont", 20, 0xFAFAFA);
		public static const normalText:TextFormat = new TextFormat("$FieldFont", 16, 0xFAFAFA);
		public static const normalBold:TextFormat = new TextFormat("$TitleFont", 16, 0xFAFAFA);
		public static const scoreformat:TextFormat = new TextFormat("$TitleFont", 24, 0xFAFAFA, true);
		public static const markersFormat:TextFormat = new TextFormat("BattleObserver", 23, 0xFAFAFA);
		public static const armorText:TextFormat = new TextFormat("$TitleFont", 20, 0xFAFAFA, null, null, null, null, null, 'center');

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