package fl.transitions
{
   import flash.display.MovieClip;
   import flash.events.Event;
   import flash.events.EventDispatcher;
   import flash.events.TimerEvent;
   import flash.utils.Timer;
   import flash.utils.getTimer;
   
   [Event(name="motionStop",type="fl.transitions.TweenEvent")]
   [Event(name="motionStart",type="fl.transitions.TweenEvent")]
   [Event(name="motionResume",type="fl.transitions.TweenEvent")]
   [Event(name="motionLoop",type="fl.transitions.TweenEvent")]
   [Event(name="motionFinish",type="fl.transitions.TweenEvent")]
   [Event(name="motionChange",type="fl.transitions.TweenEvent")]
   public class Tween extends EventDispatcher
   {
      
      protected static var _mc:MovieClip = new MovieClip();
       
      
      private var _position:Number = NaN;
      
      public var prevTime:Number = NaN;
      
      public var prevPos:Number = NaN;
      
      public var isPlaying:Boolean = false;
      
      private var _fps:Number = NaN;
      
      private var _time:Number = NaN;
      
      public var begin:Number = NaN;
      
      private var _finish:Number = NaN;
      
      public var change:Number = NaN;
      
      public var looping:Boolean = false;
      
      private var _intervalID:uint = 0;
      
      public var func:Function;
      
      private var _timer:Timer = null;
      
      private var _startTime:Number = NaN;
      
      public var prop:String = "";
      
      private var _duration:Number = NaN;
      
      public var obj:Object = null;
      
      public var useSeconds:Boolean = false;
      
      public function Tween(obj:Object, prop:String, func:Function, begin:Number, finish:Number, duration:Number, useSeconds:Boolean = false)
      {
         func = function(t:Number, b:Number, c:Number, d:Number):Number
         {
            return c * t / d + b;
         };
         super();
         if(!arguments.length)
         {
            return;
         }
         this.obj = obj;
         this.prop = prop;
         this.begin = begin;
         this.position = begin;
         this.duration = duration;
         this.useSeconds = useSeconds;
         if(func is Function)
         {
            this.func = func;
         }
         this.finish = finish;
         this._timer = new Timer(100);
         this.start();
      }
      
      public function continueTo(finish:Number, duration:Number) : void
      {
         this.begin = this.position;
         this.finish = finish;
         if(!isNaN(duration))
         {
            this.duration = duration;
         }
         this.start();
      }
      
      protected function startEnterFrame() : void
      {
         var milliseconds:Number = NaN;
         if(isNaN(this._fps))
         {
            _mc.addEventListener(Event.ENTER_FRAME,this.onEnterFrame,false,0,true);
         }
         else
         {
            milliseconds = 1000 / this._fps;
            this._timer.delay = milliseconds;
            this._timer.addEventListener(TimerEvent.TIMER,this.timerHandler,false,0,true);
            this._timer.start();
         }
         this.isPlaying = true;
      }
      
      public function stop() : void
      {
         this.stopEnterFrame();
         this.dispatchEvent(new TweenEvent(TweenEvent.MOTION_STOP,this._time,this._position));
      }
      
      private function fixTime() : void
      {
         if(this.useSeconds)
         {
            this._startTime = getTimer() - this._time * 1000;
         }
      }
      
      public function set FPS(fps:Number) : void
      {
         var oldIsPlaying:Boolean = this.isPlaying;
         this.stopEnterFrame();
         this._fps = fps;
         if(oldIsPlaying)
         {
            this.startEnterFrame();
         }
      }
      
      public function get finish() : Number
      {
         return this.begin + this.change;
      }
      
      public function get duration() : Number
      {
         return this._duration;
      }
      
      protected function stopEnterFrame() : void
      {
         if(isNaN(this._fps))
         {
            _mc.removeEventListener(Event.ENTER_FRAME,this.onEnterFrame);
         }
         else
         {
            this._timer.stop();
         }
         this.isPlaying = false;
      }
      
      public function set time(t:Number) : void
      {
         this.prevTime = this._time;
         if(t > this.duration)
         {
            if(this.looping)
            {
               this.rewind(t - this._duration);
               this.update();
               this.dispatchEvent(new TweenEvent(TweenEvent.MOTION_LOOP,this._time,this._position));
            }
            else
            {
               if(this.useSeconds)
               {
                  this._time = this._duration;
                  this.update();
               }
               this.stop();
               this.dispatchEvent(new TweenEvent(TweenEvent.MOTION_FINISH,this._time,this._position));
            }
         }
         else if(t < 0)
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
      
      public function getPosition(t:Number = NaN) : Number
      {
         if(isNaN(t))
         {
            t = this._time;
         }
         return this.func(t,this.begin,this.change,this._duration);
      }
      
      public function set finish(value:Number) : void
      {
         this.change = value - this.begin;
      }
      
      public function set duration(d:Number) : void
      {
         this._duration = d <= 0 ? Number(Infinity) : Number(d);
      }
      
      public function get position() : Number
      {
         return this.getPosition(this._time);
      }
      
      public function setPosition(p:Number) : void
      {
         this.prevPos = this._position;
         if(this.prop.length)
         {
            this.obj[this.prop] = this._position = p;
         }
         this.dispatchEvent(new TweenEvent(TweenEvent.MOTION_CHANGE,this._time,this._position));
      }
      
      public function resume() : void
      {
         this.fixTime();
         this.startEnterFrame();
         this.dispatchEvent(new TweenEvent(TweenEvent.MOTION_RESUME,this._time,this._position));
      }
      
      public function fforward() : void
      {
         this.time = this._duration;
         this.fixTime();
      }
      
      protected function onEnterFrame(event:Event) : void
      {
         this.nextFrame();
      }
      
      public function yoyo() : void
      {
         this.continueTo(this.begin,this.time);
      }
      
      public function nextFrame() : void
      {
         if(this.useSeconds)
         {
            this.time = (getTimer() - this._startTime) / 1000;
         }
         else
         {
            this.time = this._time + 1;
         }
      }
      
      protected function timerHandler(timerEvent:TimerEvent) : void
      {
         this.nextFrame();
         timerEvent.updateAfterEvent();
      }
      
      public function get FPS() : Number
      {
         return this._fps;
      }
      
      public function rewind(t:Number = 0) : void
      {
         this._time = t;
         this.fixTime();
         this.update();
      }
      
      public function set position(p:Number) : void
      {
         this.setPosition(p);
      }
      
      public function get time() : Number
      {
         return this._time;
      }
      
      private function update() : void
      {
         this.setPosition(this.getPosition(this._time));
      }
      
      public function start() : void
      {
         this.rewind();
         this.startEnterFrame();
         this.dispatchEvent(new TweenEvent(TweenEvent.MOTION_START,this._time,this._position));
      }
      
      public function prevFrame() : void
      {
         if(!this.useSeconds)
         {
            this.time = this._time - 1;
         }
      }
   }
}
