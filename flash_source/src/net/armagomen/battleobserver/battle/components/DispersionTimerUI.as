package net.armagomen.battleobserver.battle.components
{
	
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	
	import net.armagomen.battleobserver.battle.utils.Filters;
	import net.armagomen.battleobserver.battle.utils.TextExt;
	import net.armagomen.battleobserver.battle.data.Constants;
	import net.wg.gui.battle.components.*;
	
	public class DispersionTimerUI extends BattleDisplayable
	{
		private var dispersionTime:TextField;
		public var getShadowSettings:Function;
		private var currentControlMode:String = "arcade";
		
		public function DispersionTimerUI(compName:String)
		{
			super();
			this.name = compName;
		}
		
		public function as_startUpdate(config:Object):void
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
			dispersionTime = new TextExt("dispersionTimer", config.timer_position_x, config.timer_position_y, Filters.middleText, TextFieldAutoSize.CENTER, getShadowSettings(), this);
			App.utils.data.cleanupDynamicObject(config);
		}
		
		public function as_onControlModeChanged(mode:String):void
		{
			if (mode == "arcade")
			{
				this.y = (App.appHeight >> 1) - Constants.CONTROL_MODE_OFFSET;
			}
			else
			{
				this.y = App.appHeight >> 1;
			}
		}
		
		public function as_upateTimerText(text:String):void
		{
			dispersionTime.htmlText = text;
		}
		
		public function as_clearScene():void
		{
			while (this.numChildren > 0)
			{
				this.removeChildAt(0);
			}
			this.dispersionTime = null;
			var page:* = parent;
			page.unregisterComponent(this.name);
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