package net.armagomen.battleobserver.battle.utils
{
	public class Utils
	{
		public static function colorConvert(color:String):uint
		{
			return uint(parseInt("0x" + color.substr(1), 16));
		}
	}
}