package net.armagomen.battleobserver.battle.components
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.utils.Filters;
	import net.armagomen.battleobserver.battle.utils.TextExt;
	import net.armagomen.battleobserver.battle.data.Constants;
	import net.wg.gui.battle.components.*;

	public class ArmorCalculatorUI extends BattleDisplayable
	{
		private var armorCalc:TextField;
		public var getShadowSettings:Function;
		private var currentControlMode:String = "arcade";

		public function ArmorCalculatorUI(compName:String)
		{
			super();
			this.name = compName;
		}

		override protected function configUI():void
		{
			super.configUI();
			this.tabEnabled = false;
			this.tabChildren = false;
			this.mouseEnabled = false;
			this.mouseChildren = false;
			this.buttonMode = false;
			this.addEventListener(Event.RESIZE, this._onResizeHandle);
		}

		override protected function onDispose():void
		{
			this.removeEventListener(Event.RESIZE, this._onResizeHandle);
			super.onDispose();
		}

		public function as_startUpdate(calc:Object):void
		{
			var shadowSettings:Object = getShadowSettings();
			this.x = App.appWidth >> 1;
			if (this.currentControlMode == "arcade")
			{
				this.y = (App.appHeight >> 1) - Constants.CONTROL_MODE_OFFSET;
			}
			else
			{
				this.y = App.appHeight >> 1;
			}
			if (calc.enabled && calc.showCalcPoints)
			{
				this.armorCalc = new TextExt("armorCalc", calc.calcPosition.x, calc.calcPosition.y, Filters.middleText, TextFieldAutoSize.CENTER, shadowSettings, this);
			}
			App.utils.data.cleanupDynamicObject(calc);
		}

		public function as_onControlModeChanged(mode:String):void
		{
			this.currentControlMode = mode;
			if (mode == "arcade")
			{
				this.y = (App.appHeight >> 1) - Constants.CONTROL_MODE_OFFSET;
			}
			else
			{
				this.y = App.appHeight >> 1;
			}
		}
		
		public function as_armorCalc(text:String):void
		{
			if (armorCalc)
			{
				armorCalc.htmlText = text;
			}
		}

		private function _onResizeHandle(event:Event):void
		{
			this.x = App.appWidth >> 1;
			if (this.currentControlMode == "arcade")
			{
				this.y = (App.appHeight >> 1) - Constants.CONTROL_MODE_OFFSET;
			}
			else
			{
				this.y = App.appHeight >> 1;
			}
		}
	}
}