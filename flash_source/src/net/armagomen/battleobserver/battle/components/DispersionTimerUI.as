package net.armagomen.battleobserver.battle.components
{
	
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.gui.battle.components.*;
	
	
	public class DispersionTimerUI extends BattleDisplayable
	{
		private var dispersionTime:TextField;
		public var getShadowSettings:Function;
		private var loaded:Boolean = false;
		
		public function DispersionTimerUI()
		{
			super();
		}
		
		public function as_startUpdate(config:Object):void
		{
			if (!this.loaded)
			{
				dispersionTime = new TextExt("dispersionTimer", config.timer_position_x, config.timer_position_y, Filters.middleText, config.timer_align, getShadowSettings(), this);
				App.utils.data.cleanupDynamicObject(config);
				this.loaded = true;
			}
		}
		
		public function as_onCrosshairPositionChanged(x:Number, y:Number):void
		{
			this.x = x;
			this.y = y;
		}
		
		public function as_upateTimerText(text:String):void
		{
			dispersionTime.htmlText = text;
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