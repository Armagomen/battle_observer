package net.armagomen.battleobserver.battle.components.sixthsense
{
	import flash.display.*;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.net.URLRequest;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Constants;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.utils.tween.Tween;
	
	public class SixthSenseUI extends ObserverBattleDisplayable
	{
		private var loader:Loader;
		private var params:Object;
		private var timer:TextExt;
		private var _container:Sprite;
		private var hideAnimation:Tween;
		private var hideAnimation2:Tween;
		private const POSITION:Number = 135;
		
		[Embed(source = "error.png")]
		private var DefaultIcon:Class;
		
		public function SixthSenseUI()
		{
			super();
			this.loader = new Loader();
			this.loader.contentLoaderInfo.addEventListener(Event.COMPLETE, this.imageLoaded);
			this.loader.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR, this.onLoadError);
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			this.params = this.getSettings();
			this.x = App.appWidth >> 1;
			this._container = new Sprite()
			this._container.x = -80;
			this._container.y = this.POSITION;
			this.addChild(_container);
			if (this.params.default_icon)
			{
				this.loader.load(new URLRequest('../maps/icons/battle_observer/sixth_sense/' + this.params.default_icon_name));
			}
			else
			{
				this.loader.load(new URLRequest('../../../' + this.params.user_icon));
			}
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.loader.contentLoaderInfo.removeEventListener(Event.COMPLETE, this.imageLoaded);
			this.loader.contentLoaderInfo.removeEventListener(IOErrorEvent.IO_ERROR, this.onLoadError);
			this.loader = null;
			this.hideAnimation.stop();
			this.hideAnimation2.stop();
			this.hideAnimation = null;
			this.hideAnimation2 = null;
			this._container.removeChildren();
			this.timer = null;
			this._container = null;
			App.utils.data.cleanupDynamicObject(this.params);
		}
		
		private function addLoadedImageAndTimer(image:Bitmap):void
		{
			image.width = 150;
			image.height = 150;
			image.smoothing = true;
			this._container.addChild(image);
			this.timer = new TextExt(image.width >> 1, image.height - 20, Constants.middleText, TextFieldAutoSize.CENTER, this._container);
			this.hideAnimation = new Tween(this._container, "y", this.POSITION, -150);
			this.hideAnimation2 = new Tween(this._container, "alpha", 1.0, 0);
			this._container.alpha = 0;
		}
		
		public function as_show():void
		{
			if (this.hideAnimation.isPlaying)
			{
				this.hideAnimation.stop();
				this.hideAnimation2.stop();
			}
			this._container.y = this.POSITION;
			this._container.alpha = 1.0;
		}
		
		public function as_hide():void
		{
			this.hideAnimation.start();
			this.hideAnimation2.start();
		}
		
		public function as_updateTimer(text:String):void
		{
			this.timer.htmlText = text;
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