package net.armagomen.battleobserver.battle.components
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.data.Constants;
	import net.wg.gui.battle.components.*;

	public class OwnHealthUI extends BattleDisplayable
	{
		private var own_health:TextField;
		public var getShadowSettings:Function;
		private var currentControlMode:String = "arcade";
		private var loaded:Boolean = false;

		public function OwnHealthUI()
		{
			super();
		}

		public function as_startUpdate(data:Object):void
		{
			if (this.loaded) return;
			this.doResize();
			if (data.enabled)
			{
				own_health = new TextExt("own_health", data.x, data.y, Filters.middleText, data.align, getShadowSettings(), this);
			}
			App.utils.data.cleanupDynamicObject(data);
			this.loaded = true;
		}

		public function as_setOwnHealth(text:String):void
		{
			own_health.htmlText = text;
		}
		
		public function as_onControlModeChanged(mode:String):void
		{
			this.currentControlMode = mode;
			this.doResize();
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
			this.doResize();
		}

		private function doResize():void
		{
			this.x = App.appWidth >> 1;
			this.y = App.appHeight >> 1;
			if (this.currentControlMode == "arcade")
			{
				this.y -= Constants.CONTROL_MODE_OFFSET;
			}
		}
	}
}