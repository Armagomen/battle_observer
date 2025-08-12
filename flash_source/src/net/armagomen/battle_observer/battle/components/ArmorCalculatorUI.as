package net.armagomen.battle_observer.battle.components
{
	import flash.text.TextFieldAutoSize;
	import flash.text.TextFormat;
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
				var settings:Object = this.getSettings();
				var fmt:TextFormat = Constants.cloneTextFormat(Constants.largeText);
				fmt.size = settings.text_size;
				this.armorCalc = new TextExt(settings.position.x, settings.position.y, fmt, TextFieldAutoSize.CENTER, this);
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
		
		public function as_updateColor(color:uint):void
		{
			if (this.armorCalc.textColor != color)
			{
				this.armorCalc.textColor = color;
			}
			
		}
		
		public function as_armorCalc(text:String):void
		{
			this.armorCalc.text = text;
		}
	}
}