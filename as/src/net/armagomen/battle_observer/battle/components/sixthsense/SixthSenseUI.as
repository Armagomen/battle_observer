package net.armagomen.battle_observer.battle.components.sixthsense
{
	import flash.display.*;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.net.URLRequest;
	import flash.text.TextFieldAutoSize;
	import flash.text.TextFormat;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.RadialProgressBar;
	import net.armagomen.battle_observer.utils.TextExt;
	import net.armagomen.battle_observer.utils.Utils;
	import net.armagomen.battle_observer.utils.tween.Tween;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class SixthSenseUI extends ObserverBattleDisplayable
	{
		private var loader:Loader;
		private var params:Object;
		private var timer_text:TextExt;
		private var _container:Sprite;
		private var hideAnimation:Tween;
		private var hideAnimation2:Tween;
		private var POSITION_Y:Number;
		private var _image:Bitmap;
		private var radial_progress:RadialProgressBar;
		
		public var getIconName:Function;
		
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
			if (this.notInitialized())
			{
				this.params = this.getSettings();
				this.x = App.appWidth >> 1;
				this._container = new Sprite()
				this._container.alpha = 0;
				this.addChild(this._container);
				this.loader.load(new URLRequest("../maps/icons/battle_observer/sixth_sense/" + this.getIconName()));
				this.hideComponent(BATTLE_VIEW_ALIASES.SIXTH_SENSE);
			}
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.removeChildren();
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
		
		private function hideIcon():void
		{
			if (!this.hideAnimation.isPlaying)
			{
				this.hideAnimation.start();
				this.hideAnimation2.start();
			}
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
		
		private function makeEven(n:Number):Number
		{
			return (n & 1) ? n + 1 : n;
		}
		
		private function updateParams():void
		{
			var scale:Number = Math.sqrt(App.appHeight / 1080.0);
			var size:Number = makeEven(this.params.icon_size);
			var afterScaleWH:Number = makeEven(Math.min(180.0, Math.ceil(size * scale)));
			var half_size:int = afterScaleWH >> 1;
			
			this.POSITION_Y = Math.ceil(App.appHeight / 7 + half_size);
			this._image.width = this._image.height = afterScaleWH;
			this._image.smoothing = true;
			this._image.x = -half_size;
			if (!this._container.contains(this._image)) this._container.addChild(this._image);
			
			if (this.params.show_timer)
			{
				var text_size:Number = Math.ceil(18 * scale);
				var fmt:TextFormat = new TextFormat("$TitleFont", text_size, 0xFFFFFF);
				
				if (this.timer_text)
				{
					if (Number(this.timer_text.getTextFormat().size) != text_size)
					{
						this.timer_text.defaultTextFormat = fmt;
						this.timer_text.setTextFormat(fmt);
					}
					this.timer_text.y = half_size + (text_size >> 1);
				}
				else
				{
					this.timer_text = new TextExt(0, half_size + (text_size >> 1), fmt, TextFieldAutoSize.CENTER, this._container);
				}
				this.timer_text.alpha = 0.85;
			}
			
			if (!this.hideAnimation) this.addAnimations();
			
			if (this.params.show_timer_graphics)
			{
				if (!this.radial_progress) this.radial_progress = new RadialProgressBar(this._container);
				var radius:Number = Math.round(this.params.show_timer_graphics_radius * scale) || half_size;
				this.radial_progress.setParams(0, half_size, radius, scale, Utils.colorConvert(this.params.show_timer_graphics_color));
			}
			this._container.alpha = 0;
		}
		
		private function hide():void
		{
			if (this._container.alpha)
			{
				if (this.timer_text)
				{
					this.timer_text.text = "";
				}
				this.hideIcon();
			}
		}
		
		public function as_show():void
		{
			this.rewind();
			this._container.y = this.POSITION_Y;
			this._container.alpha = 1.0;
		}
		
		public function as_invoke(time:Number, percentage:Number):void
		{
			if (time <= 0.0)
			{
				this.hide();
				return;
			}
			if (this.timer_text)
			{
				this.timer_text.text = time.toFixed(1);
			}
			if (this.radial_progress)
			{
				this.radial_progress.updateProgressBar(percentage);
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