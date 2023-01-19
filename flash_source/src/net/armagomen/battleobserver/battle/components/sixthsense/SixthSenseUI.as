package net.armagomen.battleobserver.battle.components.sixthsense
{
	import flash.display.*;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.net.URLRequest;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.utils.tween.Tween;
	import net.armagomen.battleobserver.utils.tween.TweenEvent;
	
	public class SixthSenseUI extends ObserverBattleDisplayable
	{
		private var loader:Loader;
		private var params:Object;
		private var timer:TextExt;
		private var _container:Sprite;
		private var timerAnimation:Tween;
		private var hideAnimation:Tween;
		private var hideAnimation2:Tween;
		private var isDefault:Boolean = false;
		
		[Embed(source = "boris.png")]
		private var DefaultIcon:Class;
		
		public function SixthSenseUI()
		{
			super();
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
			this.isDefault = this.params.default_icon;
			this.loader = new Loader();
			this.loader.contentLoaderInfo.addEventListener(Event.COMPLETE, this.imageLoaded);
			this.loader.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR, this.onLoadError);
			if (this.isDefault)
			{
				this.loader.load(new URLRequest('../maps/icons/battle_observer/sixth_sense/' + this.params.default_icon_name + ".png"));
			}
			else
			{
				this.loader.load(new URLRequest('../../../' + this.params.image.img));
			}
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.loader.contentLoaderInfo.removeEventListener(Event.COMPLETE, this.imageLoaded);
			this.loader.contentLoaderInfo.removeEventListener(IOErrorEvent.IO_ERROR, this.onLoadError);
			this.loader = null;
			if (this.timerAnimation)
			{
				this.timerAnimation.stop();
				this.timerAnimation = null;
			}
			this.hideAnimation.stop();
			this.hideAnimation2.stop();
			this.hideAnimation.removeEventListener(TweenEvent.MOTION_FINISH, this.afterAnimation);
			this.hideAnimation = null;
			this.hideAnimation2 = null;
			this._container.removeChildren();
			this.timer = null;
			this._container = null;
			App.utils.data.cleanupDynamicObject(this.params);
		}
		
		private function addLoadedImageAndTimer(image:Bitmap):void
		{
			if (this.isDefault)
			{
				image.width = 180;
				image.height = 180;
				image.smoothing = true;
				image.x = -90;
				image.y = 130;
			}
			else
			{
				image.smoothing = this.params.image.smoothing;
				image.alpha = this.params.image.alpha;
				image.scaleX = image.scaleY = this.params.image.scale;
				image.x = this.params.image.x - image.width * 0.5;
				image.y = this.params.image.y;
			}
			this._container.addChild(image);
			if (this.params.showTimer)
			{
				if (this.isDefault)
				{
					this.timer = new TextExt(0, 280, Filters.sixthSense, TextFieldAutoSize.CENTER, getShadowSettings(), this._container);
				}
				else
				{
					this.timer = new TextExt(this.params.timer.x, this.params.timer.y, Filters.sixthSense, TextFieldAutoSize.CENTER, getShadowSettings(), this._container);
				}
				this.timerAnimation = new Tween(this.timer, "alpha", this.params.timer.alpha, 0.3);
			}
			this.hideAnimation = new Tween(this._container, "y", this._container.y, -this._container.height);
			this.hideAnimation2 = new Tween(this._container, "alpha", 1.0, 0);
			this.hideAnimation.addEventListener(TweenEvent.MOTION_FINISH, this.afterAnimation, false, 0, true);
		}
		
		public function as_show():void
		{
			if (this.hideAnimation.isPlaying)
			{
				this.hideAnimation.rewind();
				this.hideAnimation2.rewind();
			}
			this._container.y = 0;
			this._container.alpha = 1.0;
			this._container.visible = true;
		}
		
		public function as_hide():void
		{
			if (!this.hideAnimation.isPlaying)
			{
				this.hideAnimation.start();
				this.hideAnimation2.start();
			}
		}
		
		private function afterAnimation(event:TweenEvent):void
		{
			this._container.visible = false;
		}
		
		public function as_updateTimer(text:String):void
		{
			this.timer.htmlText = text;
			this.timerAnimation.start();
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