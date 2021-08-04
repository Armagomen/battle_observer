package net.armagomen.battleobserver.battle.components.batlletimer
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class ObserverBattleTimerUI extends ObserverBattleDispalaysble
	{
		private var battleTimer:TextExt;
		public var getShadowSettings:Function;
		private var loaded:Boolean = false;
		
		public function ObserverBattleTimerUI()
		{
			super();
		}
		
		public function as_startUpdate():void
		{
			if (!this.loaded)
			{
				this.x = App.appWidth;
				this.battleTimer = new TextExt("_timer", -8, 0, Filters.largeText, TextFieldAutoSize.RIGHT, getShadowSettings(), this);
				var battlePage:* = parent;
				var component:*  = battlePage.getComponent(BATTLE_VIEW_ALIASES.BATTLE_TIMER);
				if (component)
				{
					parent.removeChild(component);
				}
				this.loaded = true;
			}
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