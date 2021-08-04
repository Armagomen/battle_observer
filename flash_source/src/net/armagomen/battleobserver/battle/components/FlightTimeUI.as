package net.armagomen.battleobserver.battle.components
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class FlightTimeUI extends ObserverBattleDispalaysble
	{
		private var flyTime:TextField;
		public var getShadowSettings:Function;
		private var loaded:Boolean = false;
		
		public function FlightTimeUI()
		{
			super();
		}
		
		public function as_startUpdate(flyght:Object):void
		{
			if (!this.loaded)
			{
				flyTime = new TextExt("flyTime", flyght.x, flyght.y, Filters.middleText, flyght.align, getShadowSettings(), this);
				App.utils.data.cleanupDynamicObject(flyght);
				this.loaded = true;
			}
		}
		
		public function as_flightTime(text:String):void
		{
			flyTime.htmlText = text;
		}
		
		public function as_onCrosshairPositionChanged(x:Number, y:Number):void
		{
			this.x = x;
			this.y = y;
		}
	}
}