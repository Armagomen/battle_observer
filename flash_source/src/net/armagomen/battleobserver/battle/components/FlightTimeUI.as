package net.armagomen.battleobserver.battle.components
{
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class FlightTimeUI extends ObserverBattleDispalaysble
	{
		private var flightTime:TextExt;
		
		public function FlightTimeUI()
		{
			super();
		}
		
		public function as_startUpdate(flyght:Object):void
		{
			if (this.flightTime == null)
			{
				flightTime = new TextExt("flyTime", flyght.x, flyght.y, Filters.middleText, flyght.align, getShadowSettings(), this);
			}
		}
		
		public function as_flightTime(text:String):void
		{
			flightTime.htmlText = text;
		}
	}
}