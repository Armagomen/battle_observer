package net.armagomen.battle_observer.battle.components
{
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	
	public class FlightTimeUI extends ObserverBattleDisplayable
	{
		private var flightTime:TextExt;
		
		public function FlightTimeUI()
		{
			super();
		}
		
		override protected function onPopulate():void 
		{
			super.onPopulate();
			if (this.flightTime)
			{
				this.removeChildren();
				this.flightTime = null;
			}
			var settings:Object = this.getSettings();
			this.flightTime = new TextExt(settings.x, settings.y, Constants.middleText, settings.align, this);
		}
		
		override protected function onBeforeDispose():void 
		{
			super.onBeforeDispose();
			this.flightTime = null;
		}
		
		public function as_flightTime(text:String):void
		{
			this.flightTime.htmlText = text;
		}
	}
}