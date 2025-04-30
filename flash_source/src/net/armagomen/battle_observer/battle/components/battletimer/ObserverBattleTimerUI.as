package net.armagomen.battle_observer.battle.components.battletimer
{
	import flash.events.Event;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class ObserverBattleTimerUI extends ObserverBattleDisplayable
	{
		private var battleTimer:TextExt;
		
		public function ObserverBattleTimerUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			if (not_initialized)
			{
				super.onPopulate();
				this.x = App.appWidth;
				this.battleTimer = new TextExt(-8, 0, Constants.largeText, TextFieldAutoSize.RIGHT, this);
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
			this.battleTimer = null;
		}
		
		public function as_timer(timer:String):void
		{
			if (this.battleTimer)
			{
				this.battleTimer.htmlText = timer;
			}
		}
		
		override public function onResizeHandle(event:Event):void
		{
			this.x = App.appWidth;
		}
	}

}