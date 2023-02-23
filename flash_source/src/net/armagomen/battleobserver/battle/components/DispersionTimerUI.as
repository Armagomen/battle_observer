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
			var settings:Object = this.getSettings();
			this.dispersionTime = new TextExt(settings.x, settings.y, Filters.middleText, settings.align, this.getShadowSettings(), this);
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