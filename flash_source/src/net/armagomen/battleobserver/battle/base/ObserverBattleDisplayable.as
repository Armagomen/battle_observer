package net.armagomen.battleobserver.battle.base
{
	import flash.events.Event;
	import net.wg.gui.battle.components.BattleDisplayable;
	
	public class ObserverBattleDisplayable extends BattleDisplayable
	{
		public var getSettings:Function;
		public var isColorBlind:Function;
		public var getColors:Function;
		public var isComp7Battle:Function;
		public var doLog:Function;
		
		public function ObserverBattleDisplayable()
		{
			super();
			this.addEventListener(Event.RESIZE, this.onResizeHandle);
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
			this.removeChildren();
			super.onPopulate();
		}
		
		override protected function onBeforeDispose():void 
		{
			this.removeChildren();
			super.onBeforeDispose();
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