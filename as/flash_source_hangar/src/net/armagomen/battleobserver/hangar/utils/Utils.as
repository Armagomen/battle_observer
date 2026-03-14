package net.armagomen.battleobserver.hangar.utils
{
	public class Utils
	{
		public static function colorConvert(color:String):uint
		{
			return uint(parseInt("0x" + color.substr(1), 16));
		}
	}
}