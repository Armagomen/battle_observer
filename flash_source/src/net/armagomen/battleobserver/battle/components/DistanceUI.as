package net.armagomen.battleobserver.battle.components
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.gui.battle.components.*;
	
	public class DistanceUI extends BattleDisplayable
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
		
		override protected function configUI():void
		{
			super.configUI();
			this.tabEnabled = false;
			this.tabChildren = false;
			this.mouseEnabled = false;
			this.mouseChildren = false;
			this.buttonMode = false;
		}
		
		public function as_onCrosshairPositionChanged(x:Number, y:Number):void
		{
			this.x = x;
			this.y = y;
		}
	}
}