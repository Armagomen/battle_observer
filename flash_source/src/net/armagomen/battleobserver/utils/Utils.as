package net.armagomen.battleobserver.utils
{
	import flash.display.DisplayObject;
	import flash.geom.ColorTransform;
	
	public class Utils
	{
		public static function colorConvert(color:String):uint
		{
			if (color)
			{
				if (color == "#000000")
				{
					color = "#000001";
				}
				return uint(parseInt("0x" + color.substr(1), 16));
			}
			else
			{
				return null;
			}
		}
		
		public static function updateColor(object:DisplayObject, hpColor:String):void
		{
			var colorInfo:ColorTransform = object.transform.colorTransform;
			colorInfo.color = colorConvert(hpColor);
			object.transform.colorTransform = colorInfo;
		}
	}
}