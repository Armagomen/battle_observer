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
		
		override protected function onPopulate():void 
		{
			super.onPopulate();
			if (this.flightTime == null)
			{
				var settings:Object = this.getSettings();
				this.flightTime = new TextExt("flyTime", settings.x, settings.y, Filters.middleText, settings.align, getShadowSettings(), this);
			}
		}
		
		public function as_flightTime(text:String):void
		{
			this.flightTime.htmlText = text;
		}
	}
}