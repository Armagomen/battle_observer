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
			if (not_initialized)
			{
				super.onPopulate();
				var damageLogPanel:* = this.battlePage.getComponent(BATTLE_VIEW_ALIASES.BATTLE_DAMAGE_LOG_PANEL);
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
					
					this.logs = new <TextExt>[new TextExt(settings.settings.x + this.isComp7Battle() ? 50 : 30, settings.settings.y + 4, null, settings.settings.align, damageLogPanel._detailsTopContainer, settings.top_enabled), new TextExt(settings.settings.x + 20, settings.settings.y, null, settings.settings.align, damageLogPanel._detailsBottomContainer, settings.bottom_enabled)];
					this.logs.fixed = true;
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
			super.onBeforeDispose();
			for each (var item:TextExt in this.logs) 
			{
				item.parent.removeChild(item);
			}
		}
		
		public function as_updateExtendedLog(log_id:int, text:String):void
		{
			this.logs[log_id].htmlText = text;
		}
	}
}