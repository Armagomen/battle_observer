package net.armagomen.battle_observer.battle.components
{
	import flash.events.Event;
	import flash.geom.Rectangle;
	import flash.utils.setTimeout;
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
			if (not_initialized)
			{
				super.onPopulate();
				var settings:Object = this.getSettings().settings;
				this.x = settings.x;
				this.y = settings.y;
				this.top_log = new TextExt(0, 0, Constants.largeText, settings.align, this);
				
				if (settings.inCenter)
				{
					this.x = Math.ceil(App.appWidth >> 1) + this.getSettings().settings.x;
					this.testBounds();
				}
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
			this.top_log = null;
		}
		
		public function as_updateTopLog(text:String):void
		{
			this.top_log.htmlText = text;
		}
		
		private function testBounds():void
		{
			var team_health:ObserverBattleDisplayable = this.battlePage.getComponent("Observer_TeamsHP_UI");
			if (team_health && this.hitTestObject(team_health))
			{
				var bounds:Rectangle = team_health.getBounds(App.stage);
				this.x = bounds.x - 10;
			}
		}
		
		override public function onResizeHandle(event:Event):void
		{
			if (this.top_log && this.getSettings().settings.inCenter)
			{
				this.x = Math.ceil(App.appWidth >> 1) + this.getSettings().settings.x;
				setTimeout(this.testBounds, 1000);
			}
		}
	}
}