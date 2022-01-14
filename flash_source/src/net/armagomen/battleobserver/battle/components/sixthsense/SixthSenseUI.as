package net.armagomen.battleobserver.battle.components.sixthsense
{
	import flash.display.*;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.net.URLRequest;
	import flash.text.TextFieldAutoSize;
	import flash.utils.setTimeout;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.utils.tween.Tween;
	
	public class SixthSenseUI extends ObserverBattleDisplayable
	{
		private var loader:Loader;
		private var params:Object;
		private var timer:TextExt;
		private var _container:Sprite;
		private var animation:Tween;
		private var hideAnimation:Tween;
		private var hideAnimation2:Tween;
		
		[Embed(source = "SixthSenseIcon.png")]
		private var DefaultIcon:Class;
		
		public function SixthSenseUI()
		{
			super();
			this.loader = new Loader();
			this.x = App.appWidth >> 1;
			this._container = new Sprite()
			this._container.name = "image";
			this._container.visible = false;
			this.addChild(_container);
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			this.params = this.getSettings();
			this.loader.contentLoaderInfo.addEventListener(Event.COMPLETE, this.imageLoaded);
			this.loader.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR, this.onLoadError);
			this.loader.load(new URLRequest('../../../' + params.image.img));
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			App.utils.data.cleanupDynamicObject(this.params);
			this.loader.contentLoaderInfo.removeEventListener(Event.COMPLETE, this.imageLoaded);
			this.loader.contentLoaderInfo.removeEventListener(IOErrorEvent.IO_ERROR, this.onLoadError);
			if (this.animation)
			{
				this.animation.stop();
				this.animation = null;
			}
			this._container.removeChildren();
			this.timer = null;
			this._container = null;
			this.loader = null;
		}
		
		private function addLoadedImageAndTimer(image:Bitmap):void
		{
			image.smoothing = params.image.smoothing;
			image.alpha = params.image.alpha;
			image.scaleX = image.scaleY = params.image.scale;
			image.x = params.image.x - image.width * 0.5;
			image.y = params.image.y;
			this._container.addChild(image);
			if (params.showTimer)
			{
				this.timer = new TextExt(params.timer.x, params.timer.y, Filters.largeText, TextFieldAutoSize.CENTER, getShadowSettings(), this._container);
				this.animation = new Tween(this.timer, "alpha", 1.0, 0, 1, true);
			}
			this.hideAnimation = new Tween(this._container, "y", this._container.y, -this._container.height, 1.2, true);
			this.hideAnimation2 = new Tween(this._container, "alpha", 1.0, 0, 1.2, true);
		}
		
		public function as_show():void
		{
			this._container.visible = true;
		}
		
		public function as_hide():void
		{
			this.hideAnimation.start();
			this.hideAnimation2.start();
			setTimeout(this.afterHide, 1200);
		}
		
		private function afterHide():void
		{
			this._container.visible = false;
			this._container.alpha = 1.0;
			this._container.y = 0;
		}
		
		
		public function as_updateTimer(str:String):void
		{
			this.animation.start();
			this.timer.htmlText = str;
		}
		
		private function onLoadError(e:IOErrorEvent):void
		{
			this.loader.close();
			this.addLoadedImageAndTimer(new DefaultIcon() as Bitmap);
		}
		
		private function imageLoaded(e:Event):void
		{
			this.addLoadedImageAndTimer(this.loader.content as Bitmap);
			this.loader.unload();
		}
			
		override public function onResizeHandle(event:Event):void
		{
			this.x = App.appWidth >> 1;
		}
	}
}