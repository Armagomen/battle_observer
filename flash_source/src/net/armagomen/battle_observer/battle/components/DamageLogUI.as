package net.armagomen.battle_observer.battle.components
{
	import flash.events.Event;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	
	public class DamageLogUI extends ObserverBattleDisplayable
	{
		private var top_log_inCenter:Boolean = true;
		private var top_log:TextExt          = null;
		
		public function DamageLogUI()
		{
			super();
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.top_log = null;
		}
		
		public function as_createTopLog(settings:Object):void
		{
			this.top_log_inCenter = settings.inCenter;
			this.x = !this.top_log_inCenter ? 0 : Math.ceil(App.appWidth >> 1);
			this.top_log = new TextExt(settings.x, settings.y, Constants.largeText, settings.align, this);
		}
		
		public function as_updateTopLog(text:String):void
		{
			this.top_log.htmlText = text;
		}
		
		override public function onResizeHandle(event:Event):void
		{
			if (this.top_log && this.top_log_inCenter)
			{
				this.x = Math.ceil(App.appWidth >> 1);
			}
		}
	}
}