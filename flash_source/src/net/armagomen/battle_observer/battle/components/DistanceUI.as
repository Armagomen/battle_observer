package net.armagomen.battle_observer.battle.components
{
	import flash.events.TimerEvent;
	import flash.text.TextFormat;
	import flash.utils.Timer;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	import net.armagomen.battle_observer.utils.Utils;
	
	public class DistanceUI extends ObserverBattleDisplayable
	{
		private var distance:TextExt;
		public var getUpdatedDistance:Function;
		private var _timer:Timer = null;
		
		public function DistanceUI()
		{
			super();
			this._timer = new Timer(200);
		}
		
		override protected function onPopulate():void
		{
			if (not_initialized)
			{
				super.onPopulate();
				var settings:Object = this.getSettings();
				var fmt:TextFormat  = Constants.cloneTextFormat(Constants.middleText);
				fmt.size = settings.text_size;
				fmt.color = Utils.colorConvert(settings.color);
				this.distance = new TextExt(settings.x, settings.y, fmt, settings.align, this);
				this._timer.addEventListener(TimerEvent.TIMER, this.timerHandler, false, 0, true);
			}
			else
			{
				super.onPopulate();
			}
		}
		
		override protected function onBeforeDispose():void
		{
			if (this._timer.running)
			{
				this._timer.stop();
			}
			if (this._timer.hasEventListener(TimerEvent.TIMER))
			{
				this._timer.removeEventListener(TimerEvent.TIMER, this.timerHandler);
			}
			this._timer = null;
			this.distance = null;
			super.onBeforeDispose();
		}
		
		protected function timerHandler(timerEvent:TimerEvent):void
		{
			this.update();
			timerEvent.updateAfterEvent();
		}
		
		public function as_setUpdateEnabled(enabled:Boolean):void
		{
			if (this._timer.running != enabled)
			{
				this._timer[enabled ? "start" : "stop"]();
				if (!enabled)
				{
					this.distance.text = '';
				}
			}
		}
		
		private function update():void
		{
			this.distance.text = this.getUpdatedDistance();
		}
	}
}