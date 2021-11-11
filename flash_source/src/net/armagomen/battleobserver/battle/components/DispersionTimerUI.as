package net.armagomen.battleobserver.battle.components
{
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	
	public class DispersionTimerUI extends ObserverBattleDisplayable
	{
		private var dispersionTime:TextExt;
		
		public function DispersionTimerUI()
		{
			super();
		}
		
		override protected function onPopulate():void 
		{
			super.onPopulate();
			if (this.dispersionTime == null)
			{
				var settings:Object = this.getSettings();
				this.dispersionTime = new TextExt(settings.timer_position_x, settings.timer_position_y, Filters.middleText, settings.timer_align, this.getShadowSettings(), this);
			}
		}
		
		override protected function onBeforeDispose():void 
		{
			super.onBeforeDispose();
			this.dispersionTime = null;
		}
		
		public function as_upateTimerText(text:String):void
		{
			this.dispersionTime.htmlText = text;
		}
	}
}