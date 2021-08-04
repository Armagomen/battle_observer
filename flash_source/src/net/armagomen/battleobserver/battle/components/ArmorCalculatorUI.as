package net.armagomen.battleobserver.battle.components
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class ArmorCalculatorUI extends ObserverBattleDispalaysble
	{
		private var armorCalc:TextField;
		public var getShadowSettings:Function;
		private var loaded:Boolean = false;
		
		public function ArmorCalculatorUI()
		{
			super();
		}
		
		public function as_startUpdate(calc:Object):void
		{
			if (!this.loaded)
			{
				this.armorCalc = new TextExt("armorCalc", calc.position.x, calc.position.y, Filters.armorText, TextFieldAutoSize.CENTER, getShadowSettings(), this);
				App.utils.data.cleanupDynamicObject(calc);
				this.loaded = true;
			}
		}
		
		public function as_onCrosshairPositionChanged(x:Number, y:Number):void
		{
			this.x = x;
			this.y = y;
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