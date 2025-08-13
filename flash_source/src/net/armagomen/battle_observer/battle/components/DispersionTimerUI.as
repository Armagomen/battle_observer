package net.armagomen.battle_observer.battle.components
{
	import flash.text.TextFormat;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	
	public class DispersionTimerUI extends ObserverBattleDisplayable
	{
		private var dispersionTime:TextExt;
		
		public function DispersionTimerUI()
		{
			super();
		}
		
		override protected function onPopulate():void 
		{
			if (not_initialized)
			{
				super.onPopulate();
				var settings:Object = this.getSettings();
				var fmt:TextFormat = Constants.cloneTextFormat(Constants.middleText);
				fmt.size = settings.text_size;
				this.dispersionTime = new TextExt(settings.x, settings.y, fmt, settings.align, this);
			}
			else
			{
				super.onPopulate();
			}
		}
		
		override protected function onBeforeDispose():void 
		{
			super.onBeforeDispose();
			this.dispersionTime = null;
		}
		
		public function as_upateTimerText(text:String, color:uint):void
		{
			this.dispersionTime.textColor = color;
			this.dispersionTime.text = text;
		}
	}
}