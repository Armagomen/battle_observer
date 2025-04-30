package net.armagomen.battle_observer.battle.components.debugpanel
{
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	
	public class ObserverDebugPanelUI extends ObserverBattleDisplayable
	{
		
		private var debugPanel:*;
		
		public function ObserverDebugPanelUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			var settings:Object = this.getSettings();
			var _class:* = settings.style == "modern" ? Modern: Minimal;
			this.debugPanel = new _class(settings, this)
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.removeChildren();
			this.debugPanel = null;
		}
		
		public function as_update(ping:int, fps:int, lag:Boolean):void
		{
			if (this.debugPanel)
			{
				this.debugPanel.update(ping, fps, lag);
			}
		}
	}
}