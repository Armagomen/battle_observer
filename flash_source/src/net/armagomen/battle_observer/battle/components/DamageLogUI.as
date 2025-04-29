package net.armagomen.battle_observer.battle.components
{
	import flash.events.Event;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	
	public class DamageLogUI extends ObserverBattleDisplayable
	{
		private var top_log:TextExt = null;
		
		public function DamageLogUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			if (this.top_log)
			{
				this.removeChildren();
				this.top_log = null;
			}
			var settings:Object = this.getSettings().settings;
			this.x = !settings.inCenter ? 0 : Math.ceil(App.appWidth >> 1);
			this.top_log = new TextExt(settings.x, settings.y, Constants.largeText, settings.align, this);
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.removeChildren();
			this.top_log = null;
		}
		
		public function as_updateTopLog(text:String):void
		{
			this.top_log.htmlText = text;
		}
		
		override public function onResizeHandle(event:Event):void
		{
			if (this.top_log && this.getSettings().settings.inCenter)
			{
				this.x = Math.ceil(App.appWidth >> 1);
			}
		}
	}
}