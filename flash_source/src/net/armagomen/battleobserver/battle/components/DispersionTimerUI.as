package net.armagomen.battleobserver.battle.components
{
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	
	public class DispersionTimerUI extends ObserverBattleDispalaysble
	{
		private var dispersionTime:TextExt;
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
	}
}