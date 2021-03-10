package net.armagomen.battleobserver.utils
{

	public class Params
	{
		public static var allyColor:uint = 0;
		public static var enemyColor:uint = 0;
		public static var isLegue:Boolean = false;
		public static var cBlind:Boolean = false;
		public static var hpBarsEnabled:Boolean = true;
		public static var AnimationEnabled:Boolean = true;

		public function Params()
		{
			super();
		}

		public static function setAllyColor(color:uint):void
		{
			allyColor = color;
		}

		public static function setEnemyColor(color:uint):void
		{
			enemyColor = color;
		}

		public static function setIslegue(param:Boolean):void
		{
			isLegue = param;
		}

		public static function setHpBarsEnabled(param:Boolean):void
		{
			hpBarsEnabled = param;
		}

		public static function setcBlind(param:Boolean):void
		{
			cBlind = param;
		}
	}

}