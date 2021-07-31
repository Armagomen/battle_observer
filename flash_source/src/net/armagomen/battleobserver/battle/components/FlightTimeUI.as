package net.armagomen.battleobserver.battle.components
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.gui.battle.components.*;
	
	public class FlightTimeUI extends BattleDisplayable
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
		
		override protected function configUI():void
		{
			super.configUI();
			this.tabEnabled = false;
			this.tabChildren = false;
			this.mouseEnabled = false;
			this.mouseChildren = false;
			this.buttonMode = false;
		
		}
	
	}
}