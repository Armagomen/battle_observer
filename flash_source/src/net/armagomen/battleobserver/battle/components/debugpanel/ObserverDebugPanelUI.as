package net.armagomen.battleobserver.battle.components.debugpanel
{
	import flash.display.Sprite;
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
				this.debugPanel = new Modern(settings);
			}
			else
			{
				this.debugPanel = new Minimal(settings);
			}
			this.addChild(this.debugPanel as Sprite);
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