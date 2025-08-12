package net.armagomen.battle_observer.utils
{
	import flash.text.TextFormat;
	
	public class Constants
	{
		public static const middleText:TextFormat   = new TextFormat("$TitleFont", 18, 0xFFFFFF);
		public static const middleText2:TextFormat  = new TextFormat("$TitleFont", 15, 0xFFFFFF);
		public static const diff:TextFormat         = new TextFormat("$TitleFont", 14, 0xFFFFFF);
		public static const largeText:TextFormat    = new TextFormat("$TitleFont", 20, 0xFFFFFF);
		public static const normalText:TextFormat   = new TextFormat("$FieldFont", 16, 0xFFFFFF);
		public static const normalText15:TextFormat = new TextFormat("$FieldFont", 15, 0xFFFFFF);
		public static const scoreformat:TextFormat  = new TextFormat("$TitleFont", 24, 0xFFFFFF, true);
		
		public static const ALPHA:Number            = 0.6;
		public static const BG_ALPHA:Number         = 0.3;
		public static const HUNDREDTH:Number        = 0.01;
		
		public function Constants()
		{
		
		}
		
		public static function cloneTextFormat(fmt:TextFormat):TextFormat
		{
			return new TextFormat(fmt.font, fmt.size, fmt.color, fmt.bold, fmt.italic, fmt.underline, fmt.url, fmt.target, fmt.align, fmt.leftMargin, fmt.rightMargin, fmt.indent, fmt.leading);
		}
	}
}