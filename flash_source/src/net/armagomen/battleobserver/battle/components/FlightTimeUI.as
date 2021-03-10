package net.armagomen.battleobserver.battle.components
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.data.Constants;
	import net.wg.gui.battle.components.*;
	

	public class FlightTimeUI extends BattleDisplayable
	{
		private var flyTime:TextField;
		public var getShadowSettings:Function;
		private var currentControlMode:String = "arcade";

		public function FlightTimeUI(compName:String)
		{
			super();
			this.name = compName;
		}

		public function as_startUpdate(flyght:Object):void
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
			if (flyght.enabled)
			{
				flyTime = new TextExt("flyTime", flyght.x, flyght.y, Filters.middleText, flyght.align, getShadowSettings(), this);
			}
			App.utils.data.cleanupDynamicObject(flyght);
		}

		public function as_flightTime(text:String):void
		{
			flyTime.htmlText = text;
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