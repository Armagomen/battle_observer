package net.armagomen.battleobserver.battle.components.maingun
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.utils.Filters;
	import net.armagomen.battleobserver.battle.utils.TextExt;
	import net.wg.gui.battle.components.*;

	public class MainGunUI extends BattleDisplayable
	{
		private var mainGun:TextField = null;
		private var mgunXCache:int = 255;
		public var getShadowSettings:Function;

		public function MainGunUI(compName:String)
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

		public function as_clearScene():void
		{
			while (this.numChildren > 0){
				this.removeChildAt(0);
			}
			this.mainGun = null;
			var page:* = parent;
			page.unregisterComponent(this.name);
		}

		public function as_startUpdate(data:Object):void
		{
			this.x = (App.appWidth >> 1) + data.x;
			this.y = data.y;
			this.mgunXCache = data.x;
			this.mainGun = new TextExt("mainGun", 0, 0, Filters.largeText, data.align, getShadowSettings(), this);
			App.utils.data.cleanupDynamicObject(data);
		}

		public function as_mainGunText(GunText:String):void
		{
			if (this.mainGun){
				this.mainGun.htmlText = GunText;
			}
		}

		private function _onResizeHandle(event:Event):void
		{
			this.x = (App.appWidth >> 1) + this.mgunXCache;
		}
	}
}