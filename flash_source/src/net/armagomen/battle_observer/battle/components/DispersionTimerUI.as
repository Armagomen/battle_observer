package net.armagomen.battle_observer.battle.components
{
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	
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