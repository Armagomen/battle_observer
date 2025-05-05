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
			
			if (not_initialized)
			{
				super.onPopulate();
				var styles:Object = {"minimal": Minimal, "modern": Modern, "big_lag": BigLag};
				var settings:Object = this.getSettings();
				this.debugPanel = this.addChild(new styles[settings.style](settings));
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