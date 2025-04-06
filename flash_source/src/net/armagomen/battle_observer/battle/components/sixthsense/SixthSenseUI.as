package net.armagomen.battle_observer.battle.components.sixthsense
{
	import flash.display.*;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.net.URLRequest;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	import net.armagomen.battle_observer.utils.tween.Tween;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.views.BaseBattlePage;
	
	public class SixthSenseUI extends ObserverBattleDisplayable
	{
		private var loader:Loader;
		private var params:Object;
		private var timer:TextExt;
		private var _container:Sprite;
		private var hideAnimation:Tween;
		private var showAnimation:Tween;
		private var hideAnimation2:Tween;
		private var POSITION_Y:Number = (App.appHeight >> 3) + 10;
		private var _image:Bitmap;
		
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
			this.addChild(this._container);
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
			this.showAnimation.stop();
			this.hideAnimation = null;
			this.hideAnimation2 = null;
			this.showAnimation = null;
			this._container.removeChildren();
			this.timer = null;
			this._container = null;
			App.utils.data.cleanupDynamicObject(this.params);
		}
		
		private function addTimerAndAnimations():void
		{
			this.timer = new TextExt(0, this._image.height - 4, Constants.tite16, TextFieldAutoSize.CENTER, this._container);
			this.hideAnimation = new Tween(this._container, "y", this.POSITION_Y, -this._image.height, 0.5);
			this.hideAnimation2 = new Tween(this._container, "alpha", 1.0, 0, 0.5);
			this.showAnimation = new Tween(this._container, "alpha", 0, 1.0, 0.1);
			this._container.alpha = 0;
			this._container.y = this.POSITION_Y;
		}
		
		private function updateImageScale():void
		{
			var afterScaleWH:Number = Math.min(180.0, Math.ceil(90.0 * (App.appHeight / 1080.0)));
			if (afterScaleWH % 2 != 0)
			{
				afterScaleWH = afterScaleWH > 180.0 ? afterScaleWH - 1 : afterScaleWH + 1;
			}
			this._image.width = afterScaleWH;
			this._image.height = afterScaleWH;
			this._image.smoothing = true;
			this._image.x = -afterScaleWH >> 1;
			this._container.addChild(this._image);
			if (this.timer)
			{
				this.timer.y = afterScaleWH - 4;
			}
			
			if (this.hideAnimation)
			{
				this.hideAnimation.finish = -afterScaleWH;
			}
		}
		
		public function as_show():void
		{
			if (this.hideAnimation.isPlaying)
			{
				this.hideAnimation.stop();
				this.hideAnimation.rewind();
				this.hideAnimation2.stop();
				this.hideAnimation2.rewind();
			}
			this._container.y = this.POSITION_Y;
			this.showAnimation.start();
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
			this._image = new DefaultIcon() as Bitmap;
			this.updateImageScale();
			this.addTimerAndAnimations();
		}
		
		private function imageLoaded(e:Event):void
		{
			this._image = this.loader.content as Bitmap;
			this.updateImageScale();
			this.addTimerAndAnimations();
			this.loader.unload();
		}
		
		override public function onResizeHandle(event:Event):void
		{
			this.x = App.appWidth >> 1;
			this.POSITION_Y = (App.appHeight >> 3) + 10;
			if (this._image)
			{
				this.updateImageScale();
			}
		
		}
	}
}