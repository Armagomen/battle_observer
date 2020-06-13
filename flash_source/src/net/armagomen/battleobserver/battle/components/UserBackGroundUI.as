package net.armagomen.battleobserver.battle.components
{
	import flash.display.*;
	import flash.events.Event;
	import flash.net.URLRequest;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.utils.Params;
	import net.wg.gui.battle.components.*;

	public class UserBackGroundUI extends BattleDisplayable
	{
		private var groupMap:Array;

		public function UserBackGroundUI(compName:String)
		{
			super();
			this.name = compName;
		}

		public function as_startUpdate(data:Object):void
		{
			if (data.bg_vis && !Params.isLegue)
			{
				this.alpha = data.bg_alpha;
				this.graphics.beginFill(0, data.bg_alpha);
				this.graphics.drawRect(0, 0, App.appWidth, 31);
				this.graphics.endFill();
			}
			if (data.uBG.enabled)
			{
				this.groupMap = data.uBG.user_background as Array;
				if (this.groupMap.length > 0)
				{
					setUserBackgounds();
				}
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
		}

		public function as_clearScene():void
		{
			while (this.numChildren > 0){
				this.removeChildAt(0);
			}
			this.groupMap = null;
			var page:* = parent;
			page.unregisterComponent(this.name);
		}

		private function setUserBackgounds():void
		{
			for each (var item:Object in this.groupMap)
			{
				if (item.enabled)
				{
					var loader:Loader = new Loader();
					loader.cacheAsBitmap = true;
					loader.z = this.groupMap.indexOf(item);
					loader.contentLoaderInfo.addEventListener(Event.COMPLETE, imageLoaded, false, 0, true);
					loader.load(new URLRequest('../../../'+item.img));
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
			var image:Bitmap = loaderInfo.content as Bitmap;
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
				var debug:* = parent.getChildByName("Observer_DebugPanel_UI");
				if (debug){
					debug.addChild(image);
				}
				return;
			}
			this.addChild(image);
		}
	}
}