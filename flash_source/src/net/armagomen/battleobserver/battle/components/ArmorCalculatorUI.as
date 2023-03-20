package net.armagomen.battleobserver.battle.components
{
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class ArmorCalculatorUI extends ObserverBattleDisplayable
	{
		private var armorCalc:TextExt;
		
		public function ArmorCalculatorUI()
		{
			super();
		}
		
		override protected function onPopulate():void 
		{
			super.onPopulate();
			var settings:Object = this.getSettings();
			this.armorCalc = new TextExt(settings.position.x, settings.position.y, Filters.armorText, TextFieldAutoSize.CENTER, this);
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