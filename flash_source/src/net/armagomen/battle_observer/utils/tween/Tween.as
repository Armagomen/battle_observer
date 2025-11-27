package net.armagomen.battle_observer.utils.tween
{
	import flash.events.Event;
	import flash.events.EventDispatcher;
	import flash.events.TimerEvent;
	import flash.utils.Timer;
	import flash.utils.getTimer;
	import scaleform.clik.motion.Tween;
	
	[Event(name = "motionStop", type = "net.armagomen.battleobserver.utils.tween.TweenEvent")]
	[Event(name = "motionStart", type = "net.armagomen.battleobserver.utils.tween.TweenEvent")]
	[Event(name = "motionResume", type = "net.armagomen.battleobserver.utils.tween.TweenEvent")]
	[Event(name = "motionLoop", type = "net.armagomen.battleobserver.utils.tween.TweenEvent")]
	[Event(name = "motionFinish", type = "net.armagomen.battleobserver.utils.tween.TweenEvent")]
	[Event(name = "motionChange", type = "net.armagomen.battleobserver.utils.tween.TweenEvent")]
	public class Tween extends EventDispatcher
	{
		private const FPS:Number      = 30;
		private var _position:Number  = NaN;
		public var isPlaying:Boolean  = false;
		private var _time:Number      = 0;
		public var begin:Number       = NaN;
		private var change:Number     = NaN;
		private var _timer:Timer      = null;
		private var _startTime:Number = NaN;
		private var prop:String       = "";
		private var _duration:Number  = NaN;
		private var obj:Object        = null;
		
		public function Tween(_obj:Object, _prop:String, _begin:Number, _finish:Number, _duration:Number = 1.0)
		{
			super();
			if (!arguments.length)
			{
				return;
			}
			this.obj = _obj;
			this.prop = _prop;
			this.begin = _begin;
			this.position = _begin;
			this.duration = _duration;
			this.finish = _finish;
			this._timer = new Timer(1000 / this.FPS);
			this._timer.addEventListener(TimerEvent.TIMER, this.timerHandler, false, 0, true);
		}
		
		public function continueTo(finish:Number, duration:Number):void
		{
			this.begin = this.position;
			this.finish = finish;
			if (!isNaN(duration))
			{
				this.duration = duration;
			}
			this.start();
		}
		
		protected function startEnterFrame():void
		{
			this._timer.start();
			this.isPlaying = true;
		}
		
		public function stop():void
		{
			this.stopEnterFrame();
			this.dispatchEvent(new TweenEvent(TweenEvent.MOTION_STOP, this._time, this._position));
		}
		
		private function fixTime():void
		{
			this._startTime = getTimer() - this._time * 1000;
		}
		
		public function get finish():Number
		{
			return this.begin + this.change;
		}
		
		public function get duration():Number
		{
			return this._duration;
		}
		
		protected function stopEnterFrame():void
		{
			
			this._timer.stop();
			this.isPlaying = false;
		}
		
		public function set time(t:Number):void
		{
			if (t > this.duration)
			{
				this._time = this._duration;
				this.update();
				this.stop();
				this.dispatchEvent(new TweenEvent(TweenEvent.MOTION_FINISH, this._time, this._position));
			}
			else if (t < 0)
			{
				this.rewind();
				this.update();
			}
			else
			{
				this._time = t;
				this.update();
			}
		}
		
		public function getPosition(t:Number = NaN):Number
		{
			if (isNaN(t))
			{
				t = this._time;
			}
			return this.change * t / this._duration + this.begin;
		}
		
		public function set finish(value:Number):void
		{
			this.change = value - this.begin;
		}
		
		public function set duration(d:Number):void
		{
			this._duration = d <= 0 ? Number(Infinity) : Number(d);
		}
		
		public function get position():Number
		{
			return this.getPosition(this._time);
		}
		
		public function setPosition(p:Number):void
		{
			if (this.prop.length)
			{
				this.obj[this.prop] = this._position = p;
			}
			this.dispatchEvent(new TweenEvent(TweenEvent.MOTION_CHANGE, this._time, this._position));
		}
		
		public function resume():void
		{
			this.fixTime();
			this.startEnterFrame();
			this.dispatchEvent(new TweenEvent(TweenEvent.MOTION_RESUME, this._time, this._position));
		}
		
		public function fforward():void
		{
			this.time = this._duration;
			this.fixTime();
		}
		
		protected function onEnterFrame(event:Event):void
		{
			this.nextFrame();
		}
		
		public function yoyo():void
		{
			this.continueTo(this.begin, this.time);
		}
		
		public function nextFrame():void
		{
			this.time = (getTimer() - this._startTime) / 1000;
		}
		
		protected function timerHandler(timerEvent:TimerEvent):void
		{
			this.nextFrame();
			timerEvent.updateAfterEvent();
		}
		
		public function rewind(t:Number = 0):void
		{
			this._time = t;
			this.fixTime();
			this.update();
		}
		
		public function set position(p:Number):void
		{
			this.setPosition(p);
		}
		
		public function get time():Number
		{
			return this._time;
		}
		
		private function update():void
		{
			this.setPosition(this.getPosition(this._time));
		}
		
		public function start():void
		{
			this.rewind();
			this.startEnterFrame();
			this.dispatchEvent(new TweenEvent(TweenEvent.MOTION_START, this._time, this._position));
		}
	}
}
