package net.armagomen.battleobserver.battle.components
{
	import net.armagomen.battleobserver.utils.Constants;
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
			this.dispersionTime = new TextExt(settings.x, settings.y, Constants.middleText, settings.align, this);
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