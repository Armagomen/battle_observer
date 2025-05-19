package net.armagomen.battle_observer.battle.components.debugpanel
{
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class ObserverDebugPanelUI extends ObserverBattleDisplayable
	{
		private var debugPanel:*;
		private const MINIMAL:String = "minimal";
		private const MODERN:String  = "modern";
		private const BIG_LAG:String = "big_lag";
		
		public function ObserverDebugPanelUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			
			if (not_initialized)
			{
				super.onPopulate();
				var styles:Object   = {MINIMAL: Minimal, MODERN: Modern, BIG_LAG: BigLag};
				var settings:Object = this.getSettings();
				this.debugPanel = this.addChild(new styles[settings.style](settings));
				this.hideComponent(BATTLE_VIEW_ALIASES.DEBUG_PANEL);
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