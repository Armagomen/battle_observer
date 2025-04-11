package net.armagomen.battle_observer.battle.components.sixthsense
{
	import flash.display.*;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.net.URLRequest;
	import flash.text.TextFieldAutoSize;
	import flash.text.TextFormat;
	import flash.utils.clearInterval;
	import flash.utils.clearTimeout;
	import flash.utils.setInterval;
	import flash.utils.setTimeout;
	
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.RadialProgressBar;
	import net.armagomen.battle_observer.utils.TextExt;
	import net.armagomen.battle_observer.utils.Utils;
	import net.armagomen.battle_observer.utils.tween.Tween;
	
	public class SixthSenseUI extends ObserverBattleDisplayable
	{
		private var loader:Loader;
		private var params:Object;
		private var timer:TextExt;
		private var _container:Sprite;
		private var hideAnimation:Tween;
		private var showAnimation:Tween;
		private var hideAnimation2:Tween;
		private var POSITION_Y:Number;
		private var _image:Bitmap;
		private var radial_progress:RadialProgressBar;
		private var timerId:Number;
		private var timeoutID:Number;
		private var progress:Number    = 10000;
		private var show_time:Number   = 10000;
		private var is_visible:Boolean = false;
		
		public var playSound:Function;
		public var getTimerString:Function;
		
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
			this.clearTimers();
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
		
		private function addAnimations():void
		{
			this.hideAnimation = new Tween(this._container, "y", this.POSITION_Y, 0, 0.5);
			this.hideAnimation2 = new Tween(this._container, "alpha", 1.0, 0, 0.5);
			this.showAnimation = new Tween(this._container, "alpha", 0, 1.0, 0.1);
			this._container.alpha = 0;
		}
		
		private function updateParams():void
		{
			var size:Number         = this.params.icon_size || 90.0;
			var scale:Number        = App.appHeight / 1080.0;
			var afterScaleWH:Number = Math.min(180.0, Math.ceil(size * scale));
			if (afterScaleWH % 2 != 0)
			{
				afterScaleWH += 1;
			}
			var half_size:Number = afterScaleWH >> 1;
			this.POSITION_Y = Math.ceil(App.appHeight / 7 + half_size);
			this._image.width = afterScaleWH;
			this._image.height = afterScaleWH;
			this._image.smoothing = true;
			this._image.x = -half_size;
			this._container.addChild(this._image);
			if (this.params.show_timer)
			{
				if (this.timer)
				{
					this._container.removeChild(this.timer);
					this.timer = null;
				}
				var textformat:TextFormat = new TextFormat("$TitleFont", Math.ceil(16 * scale), 0xFFFFFF);
				var _y:Number             = afterScaleWH - (this.params.show_timer_graphics ? -2 : 2);
				this.timer = new TextExt(0, _y, textformat, TextFieldAutoSize.CENTER, this._container);
			}
			
			if (this.hideAnimation)
			{
				this.hideAnimation.finish = -afterScaleWH;
				this.hideAnimation.begin = this.POSITION_Y;
			}
			if (!this.radial_progress)
			{
				this.radial_progress = this._container.addChild(new RadialProgressBar()) as RadialProgressBar;
			}
			var radius:Number = Math.round(this.params.show_timer_graphics_radius * scale) || half_size;
			this.radial_progress.setParams(0, half_size, radius, scale, Utils.colorConvert(this.params.show_timer_graphics_color));
		}
		
		public function as_show(seconds:Number):void
		{
			if (this.hideAnimation.isPlaying)
			{
				this.hideAnimation.stop();
				this.hideAnimation.rewind();
				this.hideAnimation2.stop();
				this.hideAnimation2.rewind();
			}
			if (seconds)
			{
				this.clearTimers();
				this.progress = this.show_time = seconds * 1000;
				if (this.params.show_timer)
				{
					this.timer.htmlText = this.getTimerString(seconds);
				}
				if (this.params.show_timer_graphics)
				{
					this.radial_progress.updateProgressBar(this.progress / this.show_time);
					this.timerId = setInterval(this.updateProgress, 100);
					
				}
				else
				{
					this.timeoutID = setTimeout(as_hide, this.show_time)
					if (this.params.playTickSound)
					{
						this.timerId = setInterval(this.playSound, 1000);
					}
				}
			}
			this._container.y = this.POSITION_Y;
			this.showAnimation.start();
			this.is_visible = true;
		}
		
		private function clearTimers():void
		{
			if (this.timerId)
			{
				clearInterval(this.timerId);
				this.timerId = 0;
			}
			if (this.timeoutID)
			{
				clearTimeout(this.timeoutID);
				this.timeoutID = 0;
			}
		}
		
		public function as_hide():void
		{
			this.clearTimers();
			if (this.is_visible)
			{
				this.hideAnimation.start();
				this.hideAnimation2.start();
				this.is_visible = false;
			}
		}
		
		private function updateProgress():void
		{
			this.progress -= 100;
			this.radial_progress.updateProgressBar(this.progress / this.show_time);
			if (this.params.show_timer)
			{
				this.timer.htmlText = this.getTimerString(this.progress / 1000);
			}
			if (this.params.playTickSound && this.progress >= 1000 && this.progress % 1000 == 0)
			{
				this.playSound();
			}
			if (this.progress == 0)
			{
				this.as_hide();
			}
		}
		
		private function onLoadError(e:IOErrorEvent):void
		{
			this.loader.close();
			this._image = new DefaultIcon() as Bitmap;
			this.addAnimations();
			this.updateParams();
		}
		
		private function imageLoaded(e:Event):void
		{
			this._image = this.loader.content as Bitmap;
			this.addAnimations();
			this.updateParams();
			this.loader.unload();
		}
		
		override public function onResizeHandle(event:Event):void
		{
			this.x = App.appWidth >> 1;
			if (this._image)
			{
				this.updateParams();
			}
		}
	}
}