package net.armagomen.battleobserver.battle.components
{
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class ArmorCalculatorUI extends ObserverBattleDispalaysble
	{
		private var armorCalc:TextExt;
		
		public function ArmorCalculatorUI()
		{
			super();
		}
		
		public function as_startUpdate(calc:Object):void
		{
			if (this.armorCalc == null)
			{
				this.armorCalc = new TextExt("armorCalc", calc.position.x, calc.position.y, Filters.armorText, TextFieldAutoSize.CENTER, getShadowSettings(), this);
			}
		}
		
		public function as_armorCalc(text:String):void
		{
			if (armorCalc)
			{
				armorCalc.htmlText = text;
			}
		}
	
	}
}