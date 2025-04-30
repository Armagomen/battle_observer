package net.armagomen.battle_observer.battle.components
{
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.TextExt;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class ExtendedDamageLogsUI extends ObserverBattleDisplayable
	{
		private var logs:Vector.<TextExt> = null;
		private var top:TextExt           = null;
		private var bottom:TextExt        = null;
		
		public function ExtendedDamageLogsUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			if (not_initialized)
			{
				super.onPopulate();
				var page:*           = parent;
				var damageLogPanel:* = page.getComponent(BATTLE_VIEW_ALIASES.BATTLE_DAMAGE_LOG_PANEL);
				if (damageLogPanel)
				{
					var settings:Object = this.getSettings();
					
					if (settings.top_enabled)
					{
						damageLogPanel._detailsTopContainer.removeChildren();
					}
					if (settings.bottom_enabled)
					{
						damageLogPanel._detailsBottomContainer.removeChildren();
					}
					this.top = new TextExt(settings.settings.x + this.isComp7Battle() ? 50 : 30, settings.settings.y + 4, null, settings.settings.align, damageLogPanel._detailsTopContainer, settings.top_enabled);
					this.bottom = new TextExt(settings.settings.x + 20, settings.settings.y, null, settings.settings.align, damageLogPanel._detailsBottomContainer, settings.bottom_enabled);
					App.utils.data.cleanupDynamicObject(settings);
				}
			}
			else
			{
				super.onPopulate();
			}
		}
		
		override protected function onBeforeDispose():void
		{
			this.top.htmlText = "";
			this.bottom.htmlText = "";
			super.onBeforeDispose();
		}
		
		public function as_updateExtendedLog(log_id:int, text:String):void
		{
			if (log_id == 0)
			{
				this.top.htmlText = text;
			}
			else
			{
				this.bottom.htmlText = text;
			}
		
		}
	}
}