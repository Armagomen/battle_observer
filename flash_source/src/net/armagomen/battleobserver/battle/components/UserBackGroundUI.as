package net.armagomen.battleobserver.battle.components
{
	import flash.display.*;
	import flash.events.Event;
	import flash.net.URLRequest;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	
	public class UserBackGroundUI extends ObserverBattleDisplayable
	{
		private var groupMap:Array;
		
		public function UserBackGroundUI()
		{
			super();
		}
		
		override protected function onBeforeDispose():void 
		{
			super.onBeforeDispose();
			for each (var item:Object in this.groupMap){
				App.utils.data.cleanupDynamicObject(item);
			}
			this.groupMap = null;
		}
		
		override public function as_onAfterPopulate():void 
		{
			super.as_onAfterPopulate();
			if (this.groupMap == null)
			{
				this.groupMap = this.getSettings().user_background as Array;
				if (this.groupMap.length > 0)
				{
					this.setUserBackgounds();
				}
			}
		}
		
		private function setUserBackgounds():void
		{
			for each (var item:Object in this.groupMap)
			{
				if (item.enabled)
				{
					var loader:Loader = new Loader();
					loader.z = this.groupMap.indexOf(item);
					loader.contentLoaderInfo.addEventListener(Event.COMPLETE, imageLoaded, false, 0, true);
					loader.load(new URLRequest('../../../' + item.img));
				}
			}
		}
		
		private function imageLoaded(evt:Event):void
		{
			var loaderInfo:LoaderInfo = evt.target as LoaderInfo;
			if (loaderInfo.hasEventListener(Event.COMPLETE))
			{
				loaderInfo.removeEventListener(Event.COMPLETE, imageLoaded);
			}
			var settings:Object = this.groupMap[loaderInfo.loader.z] as Object;
			var image:Bitmap    = loaderInfo.content as Bitmap;
			if (settings.hasOwnProperty("smoothing"))
			{
				image.smoothing = settings.smoothing;
			}
			image.alpha = settings.alpha;
			image.x = settings.centeredX ? settings.x + (App.appWidth >> 1) : settings.x < 0 ? settings.x + App.appWidth : settings.x;
			image.y = settings.centeredY ? settings.y + (App.appHeight >> 1) : settings.y < 0 ? settings.y + App.appHeight : settings.y;
			image.z = 0;
			image.width = settings.width;
			image.height = settings.height;
			if (settings.hasOwnProperty("layer") && settings.layer == "debugPanel")
			{
				var battlePage:* = parent;
				var debug:*      = battlePage.getComponent("Observer_DebugPanel_UI");
				if (debug)
				{
					debug.addChild(image);
				}
				return;
			}
			this.addChild(image);
		}
	}
}