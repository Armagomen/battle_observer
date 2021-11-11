package net.armagomen.battleobserver.battle.components.batlletimer
{
	import flash.events.Event;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
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
			super.onPopulate();
			if (this.battleTimer == null)
			{
				this.x = App.appWidth;
				this.battleTimer = new TextExt(-8, 0, Filters.largeText, TextFieldAutoSize.RIGHT, this.getShadowSettings(), this);
			}
		}
		
		override protected function onBeforeDispose():void 
		{
			super.onBeforeDispose();
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