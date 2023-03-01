package net.armagomen.battleobserver.utils
{
	import flash.filters.*;
	import flash.text.TextFormat;
	import net.armagomen.battleobserver.utils.Utils;

	public class Filters
	{
		public static const glowScore:GlowFilter = new GlowFilter(0, 0.9, 4, 4, 2, BitmapFilterQuality.LOW, false, false);
		public static const middleText:TextFormat = new TextFormat("$TitleFont", 18, 0xFFFFFF);
		public static const largeText:TextFormat = new TextFormat("$TitleFont", 20, 0xFFFFFF);
		public static const normalText:TextFormat = new TextFormat("$FieldFont", 16, 0xFFFFFF);
		public static const normalText15:TextFormat = new TextFormat("$FieldFont", 15, 0xFFFFFF);
		public static const scoreformat:TextFormat = new TextFormat("$TitleFont", 24,0xFFFFFF, true);
		public static const markersFormat:TextFormat = new TextFormat("BattleObserver", 23, 0xFFFFFF);
		public static const armorText:TextFormat = new TextFormat("$TitleFont", 20, 0xFFFFFF, null, null, null, null, null, 'center');

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