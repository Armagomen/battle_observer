package net.armagomen.battleobserver.battle.components.maingun
{
	import flash.events.Event;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class MainGunUI extends ObserverBattleDispalaysble
	{
		private var mainGun:TextExt = null;
		private var mgunXCache:int  = 255;
		public var getShadowSettings:Function;
		private var loaded:Boolean  = false;
		
		public function MainGunUI()
		{
			super();
		}
		
		public function as_startUpdate(data:Object):void
		{
			if (!this.loaded)
			{
				this.x = (App.appWidth >> 1) + data.x;
				this.y = data.y;
				this.mgunXCache = data.x;
				this.mainGun = new TextExt("mainGun", 0, 0, Filters.largeText, data.align, getShadowSettings(), this);
				App.utils.data.cleanupDynamicObject(data);
				this.loaded = true;
			}
		}
		
		public function as_mainGunText(GunText:String):void
		{
			if (this.mainGun)
			{
				this.mainGun.htmlText = GunText;
			}
		}
		
		override public function onResizeHandle(event:Event):void
		{
			this.x = (App.appWidth >> 1) + this.mgunXCache;
		}
	}
}