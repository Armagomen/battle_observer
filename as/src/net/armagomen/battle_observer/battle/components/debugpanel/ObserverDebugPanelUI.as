package net.armagomen.battle_observer.battle.components.debugpanel
{
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
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
			if (this.notInitialized())
			{
				var styles:Object   = {"minimal": Minimal, "modern": Modern, "big_lag": BigLag};
				var settings:Object = this.getSettings();
				this.debugPanel = this.addChild(new styles[settings.style](settings));
				this.hideComponent(BATTLE_VIEW_ALIASES.DEBUG_PANEL);
			}
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
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