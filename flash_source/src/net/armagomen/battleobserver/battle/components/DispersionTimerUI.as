package net.armagomen.battleobserver.battle.components
{
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	
	public class DispersionTimerUI extends ObserverBattleDispalaysble
	{
		private var dispersionTime:TextExt;
		
		public function DispersionTimerUI()
		{
			super();
		}
		
		public function as_startUpdate(config:Object):void
		{
			if (this.dispersionTime == null)
			{
				dispersionTime = new TextExt("dispersionTimer", config.timer_position_x, config.timer_position_y, Filters.middleText, config.timer_align, getShadowSettings(), this);
			}
		}
		
		public function as_upateTimerText(text:String):void
		{
			dispersionTime.htmlText = text;
		}
	}
}