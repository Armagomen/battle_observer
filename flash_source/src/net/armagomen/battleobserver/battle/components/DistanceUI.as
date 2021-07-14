package net.armagomen.battleobserver.battle.components
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.data.Constants;
	import net.wg.gui.battle.components.*;
	

	public class DistanceUI extends BattleDisplayable
	{
		private var distance:TextField;
		public var getShadowSettings:Function;
		private var currentControlMode:String = "arcade";
		private var loaded:Boolean = false;

		public function DistanceUI()
		{
			super();
		}

		public function as_startUpdate(flyght:Object):void
		{
			if (!this.loaded){
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
					distance = new TextExt("distance", flyght.x, flyght.y, Filters.middleText, flyght.align, getShadowSettings(), this);
				}
				App.utils.data.cleanupDynamicObject(flyght);
				this.loaded = true;
			}
		}

		public function as_setDistance(text:String):void
		{
			distance.htmlText = text;
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