package net.armagomen.battle_observer.battle.components
{
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.TextExt;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class ExtendedDamageLogsUI extends ObserverBattleDisplayable
	{
		private var logs:Vector.<TextExt> = null;
		
		public function ExtendedDamageLogsUI()
		{
			super();
		}
		
		override protected function onPopulate():void 
		{
			super.onPopulate();
			var page:*           = parent;
			var damageLogPanel:* = page.getComponent(BATTLE_VIEW_ALIASES.BATTLE_DAMAGE_LOG_PANEL);
			if (damageLogPanel)
			{
				var settings:Object = this.getSettings();
				var top:TextExt    = new TextExt(settings.settings.x + this.isComp7Battle() ? 50 : 30, settings.settings.y + 4, null, settings.settings.align, damageLogPanel._detailsTopContainer, settings.top_enabled);
				var bottom:TextExt = new TextExt(settings.settings.x + 20, settings.settings.y, null, settings.settings.align, damageLogPanel._detailsBottomContainer, settings.bottom_enabled);
				this.logs = new <TextExt>[top, bottom];
				this.logs.fixed = true;
				App.utils.data.cleanupDynamicObject(settings);
			}
		}
		
		override protected function onBeforeDispose():void
		{
			if (this.logs)
			{
				var page:*           = parent;
				var damageLogPanel:* = page.getComponent(BATTLE_VIEW_ALIASES.BATTLE_DAMAGE_LOG_PANEL);
				damageLogPanel._detailsTopContainer.removeChild(this.logs[0])
				damageLogPanel._detailsBottomContainer.removeChild(this.logs[1])
				this.logs = null;
			}
			super.onBeforeDispose();
		}
		
		public function as_updateExtendedLog(log_id:int, text:String):void
		{
			if (this.logs)
			{
				this.logs[log_id].htmlText = text;
			}
		}
	}
}