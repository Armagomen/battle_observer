package net.armagomen.battleobserver.utils
{
	import flash.display.DisplayObject;
	import flash.geom.ColorTransform;
	
	public class Utils
	{
		private static const REGIONS:Vector.<String> = new <String>["EU", "NA", "ASIA", "CT", "KR", "CN"];
		
		public static function colorConvert(color:String):uint
		{
			return uint(parseInt(color.substr(1), 16));
		}
		
		public static function updateColor(object:DisplayObject, hpColor:String):void
		{
			var colorInfo:ColorTransform = object.transform.colorTransform;
			colorInfo.color = colorConvert(hpColor);
			object.transform.colorTransform = colorInfo;
		}
		
		public static function checkRegion(region:String):Boolean
		{
			for each (var code:String in REGIONS)
			{
				if (code == region) return true;
			}
			return false;
		}
	}
}