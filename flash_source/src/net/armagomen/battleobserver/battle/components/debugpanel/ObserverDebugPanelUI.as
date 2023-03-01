package net.armagomen.battleobserver.battle.components.debugpanel
{
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	
	public class ObserverDebugPanelUI extends ObserverBattleDisplayable
	{
		
		private var debugPanel:* = null;
		
		public function ObserverDebugPanelUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			var settings:Object       = this.getSettings();
			var shadowSettings:Object = this.getShadowSettings()
			
			if (settings.style == "modern")
			{
				this.debugPanel = new modern(shadowSettings, settings);
			}
			else
			{
				this.debugPanel = new minimal(shadowSettings, settings);
			}
			this.addChild(this.debugPanel);
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