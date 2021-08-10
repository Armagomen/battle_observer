package net.armagomen.battleobserver.battle.base
{
	import net.wg.gui.battle.components.BattleDisplayable;
	import flash.events.Event;
	
	public class ObserverBattleDispalaysble extends BattleDisplayable
	{
		public var getSettings:Function;
		public var getShadowSettings:Function;
		public var animationEnabled:Function;
		public var isColorBlind:Function;
		public var getAlpha:Function;
		public var getColors:Function;
		
		public function ObserverBattleDispalaysble()
		{
			super();
		}
		
		override protected function configUI():void
		{
			super.configUI();
			this.tabEnabled = false;
			this.tabChildren = false;
			this.mouseEnabled = false;
			this.mouseChildren = false;
			this.buttonMode = false;
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			this.addEventListener(Event.RESIZE, this.onResizeHandle);
		}
		
		override protected function onDispose():void
		{
			this.removeEventListener(Event.RESIZE, this.onResizeHandle);
			super.onDispose();
		}
		
		public function onResizeHandle(event:Event):void {}
		
		public function as_onCrosshairPositionChanged(x:Number, y:Number):void
		{
			this.x = x;
			this.y = y;
		}
	}
}