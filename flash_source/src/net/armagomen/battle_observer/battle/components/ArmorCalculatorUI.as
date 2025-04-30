package net.armagomen.battle_observer.battle.components
{
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	
	public class ArmorCalculatorUI extends ObserverBattleDisplayable
	{
		private var armorCalc:TextExt;
		
		public function ArmorCalculatorUI()
		{
			super();
		}
		
		override protected function onPopulate():void 
		{
			
			if (not_initialized)
			{
				super.onPopulate();
				var settings:Object = this.getSettings().position;
				this.armorCalc = new TextExt(settings.x, settings.y, Constants.largeText, TextFieldAutoSize.CENTER, this);
			}
			else
			{
				super.onPopulate();
			}
		}
		
		override protected function onBeforeDispose():void 
		{
			super.onBeforeDispose();
			this.armorCalc = null;
		}
		
		public function as_armorCalc(text:String):void
		{
			if (armorCalc)
			{
				this.armorCalc.htmlText = text;
			}
		}
	}
}