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
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.logs = null;
		}
		
		public function as_createExtendedLogs(position:Object, top_enabled:Boolean, bottom_enabled:Boolean):void
		{
			var page:*           = parent;
			var damageLogPanel:* = page.getComponent(BATTLE_VIEW_ALIASES.BATTLE_DAMAGE_LOG_PANEL);
			if (damageLogPanel)
			{
				if (this.logs)
				{
					damageLogPanel._detailsTopContainer.removeChild(this.logs[0])
					damageLogPanel._detailsBottomContainer.removeChild(this.logs[1])
				}
				var top:TextExt    = new TextExt(position.x + this.isComp7Battle() ? 50 : 30, position.y + 4, null, position.align, damageLogPanel._detailsTopContainer, top_enabled);
				var bottom:TextExt = new TextExt(position.x + 20, position.y, null, position.align, damageLogPanel._detailsBottomContainer, bottom_enabled);
				this.logs = new <TextExt>[top, bottom];
				this.logs.fixed = true;
			}
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