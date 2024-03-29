package net.armagomen.battleobserver.battle.components.debugpanel
{
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.battle.interfaces.IDebugPanel;
	
	public class ObserverDebugPanelUI extends ObserverBattleDisplayable
	{
		
		private var debugPanel:IDebugPanel;
		
		public function ObserverDebugPanelUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			var settings:Object = this.getSettings();
			if (settings.style == "modern")
			{
				this.debugPanel = this.addChild(new Modern(settings)) as IDebugPanel;
			}
			else
			{
				this.debugPanel = this.addChild(new Minimal(settings)) as IDebugPanel;
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