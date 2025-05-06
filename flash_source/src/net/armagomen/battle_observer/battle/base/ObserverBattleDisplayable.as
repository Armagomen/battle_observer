package net.armagomen.battle_observer.battle.base
{
	import flash.events.Event;
	import net.wg.gui.battle.components.BattleDisplayable;
	
	public class ObserverBattleDisplayable extends BattleDisplayable
	{
		public var getSettings:Function;
		public var getColors:Function;
		public var isComp7Battle:Function;
		public var doLog:Function;
		public var not_initialized:Boolean = true;
		public var battlePage:*;
		
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
			this.battlePage = parent;
			super.onPopulate();
			this.not_initialized = false;
		}
		
		override protected function onDispose():void
		{
			this.removeEventListener(Event.RESIZE, this.onResizeHandle);
			this.removeChildren();
			super.onDispose();
			App.utils.data.cleanupDynamicObject(this);
		}
		
		public function onResizeHandle(event:Event):void {}
		
		public function as_onCrosshairPositionChanged(x:Number, y:Number):void
		{
			this.x = x;
			this.y = y;
		}
		
		public function hideComponent(alias):void
		{
			var component:* = this.battlePage.getComponent(alias);
			if (component)
			{
				component.visible = false;
				component.alpha = 0;
				component.removeChildren();
				this.battlePage.removeChild(component);
			}
		}
	}
}