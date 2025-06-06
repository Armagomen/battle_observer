package net.armagomen.battle_observer.utils
{
	import flash.display.DisplayObject;
	import flash.geom.ColorTransform;
	
	public class Utils
	{
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
	}
}