package net.armagomen.battleobserver.battle.components.maingun
{
	import flash.events.Event;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class MainGunUI extends ObserverBattleDisplayable
	{
		private var mainGun:TextExt = null;
		
		public function MainGunUI()
		{
			super();
		}
		
		override protected function onPopulate():void 
		{
			super.onPopulate();
			var settings:Object = this.getSettings().settings;
			this.x = (App.appWidth >> 1) + settings.x;
			this.y = settings.y;
			this.mainGun = new TextExt(0, 0, Filters.largeText, settings.align, getShadowSettings(), this);
		}
		
		override protected function onBeforeDispose():void 
		{
			super.onBeforeDispose();
			this.mainGun = null;
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
			this.x = (App.appWidth >> 1) + this.getSettings().settings.x;
		}
	}
}