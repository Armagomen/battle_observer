package net.armagomen.battle_observer.battle.components.sixthsense
{
	import flash.display.*;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.events.TimerEvent;
	import flash.net.URLRequest;
	import flash.text.TextFieldAutoSize;
	import flash.text.TextFormat;
	import flash.utils.Timer;
	import flash.utils.clearTimeout;
	import flash.utils.setTimeout;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.RadialProgressBar;
	import net.armagomen.battle_observer.utils.TextExt;
	import net.armagomen.battle_observer.utils.Utils;
	import net.armagomen.battle_observer.utils.tween.Tween;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class SixthSenseUI extends ObserverBattleDisplayable
	{
		private const SECOND_IN_MS:int  = 1000;
		private const DELAY:int         = 100;
		private const TICKS_PER_SECOND:int = SECOND_IN_MS / DELAY;
		
		private var loader:Loader;
		private var params:Object;
		private var timer_text:TextExt;
		private var _container:Sprite;
		private var hideAnimation:Tween;
		private var hideAnimation2:Tween;
		private var POSITION_Y:Number;
		private var _image:Bitmap;
		private var radial_progress:RadialProgressBar;
		private var timeoutID:Number;
		private var _timer:Timer        = null;
		
		public var getIconPatch:Function;
		public var playSound:Function;
		
		[Embed(source = "error.png")]
		private var DefaultIcon:Class;
		
		public function SixthSenseUI()
		{
			super();
			this.loader = new Loader();
			this.loader.contentLoaderInfo.addEventListener(Event.COMPLETE, this.imageLoaded);
			this.loader.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR, this.onLoadError);
			this._timer = new Timer(this.DELAY);
		}
		
		override protected function onPopulate():void
		{
			if (this.not_initialized)
			{
				super.onPopulate();
				this.params = this.getSettings();
				this.x = App.appWidth >> 1;
				this._container = new Sprite()
				this._container.alpha = 0;
				this.addChild(this._container);
				this.loader.load(new URLRequest(this.getIconPatch()));
				this.hideComponent(BATTLE_VIEW_ALIASES.SIXTH_SENSE);
				this._timer.addEventListener(TimerEvent.TIMER, this.timerHandler, false, 0, true);
			}
			else
			{
				super.onPopulate();
			}
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.removeChildren();
			this.clearTimers();
			this._timer.removeEventListener(TimerEvent.TIMER, this.timerHandler);
			this.hideAnimation.stop();
			this.hideAnimation2.stop();
			this.hideAnimation = null;
			this.hideAnimation2 = null;
			this._container.removeChildren();
			App.utils.data.cleanupDynamicObject(this.params);
		}
		
		private function addAnimations():void
		{
			this.hideAnimation = new Tween(this._container, "y", this.POSITION_Y, 0, 0.5);
			this.hideAnimation2 = new Tween(this._container, "alpha", 1.0, 0, 0.5);
		}
		
		private function rewind():void
		{
			if (this.hideAnimation && this.hideAnimation.isPlaying)
			{
				this.hideAnimation.stop();
				this.hideAnimation.rewind();
			}
			if (this.hideAnimation2 && this.hideAnimation2.isPlaying)
			{
				this.hideAnimation2.stop();
				this.hideAnimation2.rewind();
			}
		}
		
		private function updateParams():void
		{
			var size:Number         = this.params.icon_size;
			if (size % 2 != 0)
			{
				size += 1;
			}
			var scale:Number        = App.appHeight / 1080.0;
			var afterScaleWH:Number = Math.min(180.0, Math.ceil(size * scale));
			if (afterScaleWH % 2 != 0)
			{
				afterScaleWH -= 1;
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
				if (this.timer_text)
				{
					this._container.removeChild(this.timer_text);
					this.timer_text = null;
				}
				var text_size:Number      = Math.ceil(18 * scale);
				var textformat:TextFormat = new TextFormat("$TitleFont", text_size, 0xFFFFFF);
				var _y:Number             = half_size + (text_size >> 1);
				this.timer_text = new TextExt(0, _y, textformat, TextFieldAutoSize.CENTER, this._container);
				this.timer_text.alpha = 0.80;
			}
			if (!this.hideAnimation)
			{
				this.addAnimations();
			}
			if (!this.radial_progress)
			{
				this.radial_progress = new RadialProgressBar(this._container);
			}
			var radius:Number = Math.round(this.params.show_timer_graphics_radius * scale) || half_size;
			this.radial_progress.setParams(0, half_size, radius, scale, Utils.colorConvert(this.params.show_timer_graphics_color));
			this._container.alpha = 0;
		}
		
		public function as_show(seconds:Number):void
		{
			if (seconds <= 0) {
				return;
			}
			this.rewind();
			this._container.y = this.POSITION_Y;
			this._container.alpha = 1.0;
			this.clearTimers();
			
			if (this.params.show_timer || this.params.show_timer_graphics || this.params.playTickSound)
			{
				if (this.params.show_timer)
				{
					this.timer_text.text = seconds.toFixed(1);
				}
				
				if (this.params.show_timer_graphics)
				{
					this.radial_progress.updateProgressBar(1.0);
				}
				this._timer.repeatCount = seconds * this.TICKS_PER_SECOND;
				this._timer.start();
			}
			else
			{
				this.timeoutID = setTimeout(this.as_hide, seconds * this.SECOND_IN_MS)
			}
		}
		
		private function clearTimers():void
		{
			this._timer.reset();
			if (this.timeoutID > 0)
			{
				clearTimeout(this.timeoutID);
				this.timeoutID = 0;
			}
		}
		
		public function as_hide():void
		{
			this.clearTimers();
			if (this._container.alpha)
			{
				if (this.timer_text)
				{
					this.timer_text.text = "";
				}
				this.hideAnimation.start();
				this.hideAnimation2.start();
			}
		}
		
		protected function timerHandler(timerEvent:TimerEvent):void
		{
			this.updateProgress();
			timerEvent.updateAfterEvent();
		}
		
		private function updateProgress():void
		{
			var remainingTicks:int = this._timer.repeatCount - this._timer.currentCount;
			if (this.params.show_timer_graphics)
			{
				this.radial_progress.updateProgressBar(remainingTicks / this._timer.repeatCount);
			}
			if (this.params.show_timer)
			{
				this.timer_text.text = (remainingTicks / this.TICKS_PER_SECOND).toFixed(1);
			}
			if (this.params.playTickSound && remainingTicks % this.TICKS_PER_SECOND == 0)
			{
				this.playSound();
			}
			if (remainingTicks == 0)
			{
				this.as_hide();
			}
		}
		
		private function removeListeners():void
		{
			this.loader.contentLoaderInfo.removeEventListener(Event.COMPLETE, this.imageLoaded);
			this.loader.contentLoaderInfo.removeEventListener(IOErrorEvent.IO_ERROR, this.onLoadError);
			this.loader.close();
			this.loader = null;
		}
		
		private function onLoadError(e:IOErrorEvent):void
		{
			this._image = new DefaultIcon() as Bitmap;
			this.updateParams();
			this.removeListeners();
		}
		
		private function imageLoaded(e:Event):void
		{
			this._image = this.loader.content as Bitmap;
			this.updateParams();
			this.loader.unload();
			this.removeListeners();
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