package net.armagomen.battleobserver.battle.components.debugpanel
{
	import flash.display.Sprite;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.ProgressBar;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
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
			this.debugPanel.update(ping, fps, lag);
		}
	}
}