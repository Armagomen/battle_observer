package net.armagomen.battleobserver.battle.components
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class DistanceUI extends ObserverBattleDispalaysble
	{
		private var distance:TextField;
		public var getShadowSettings:Function;
		private var loaded:Boolean = false;
		
		public function DistanceUI()
		{
			super();
		}
		
		public function as_startUpdate(flyght:Object):void
		{
			if (!this.loaded)
			{
				distance = new TextExt("distance", flyght.x, flyght.y, Filters.middleText, flyght.align, getShadowSettings(), this);
				App.utils.data.cleanupDynamicObject(flyght);
				this.loaded = true;
			}
		}
		
		public function as_setDistance(text:String):void
		{
			distance.htmlText = text;
		}
		
		public function as_onCrosshairPositionChanged(x:Number, y:Number):void
		{
			this.x = x;
			this.y = y;
		}
	}
}