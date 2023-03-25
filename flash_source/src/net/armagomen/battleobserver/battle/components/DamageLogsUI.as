package net.armagomen.battleobserver.battle.components
{
	import flash.display.Sprite;
	import flash.events.Event;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class DamageLogsUI extends ObserverBattleDisplayable
	{
		private var top_log_inCenter:Boolean = true;
		private var top_log:TextExt          = null;
		private var logs:Vector.<TextExt>    = null;
		
		public function DamageLogsUI()
		{
			super();
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.top_log = null;
			this.logs = null;
		}
		
		public function as_createTopLog(settings:Object):void
		{
			this.top_log_inCenter = settings.inCenter;
			this.x = !this.top_log_inCenter ? 0 : Math.ceil(App.appWidth >> 1);
			this.top_log = new TextExt(settings.x, settings.y, Filters.largeText, settings.align, this);
		}
		
		public function as_createExtendedLogs(position:Object, top_enabled:Boolean, bottom_enabled:Boolean):void
		{
			var damageLogPanel:* = parent.getComponent(BATTLE_VIEW_ALIASES.BATTLE_DAMAGE_LOG_PANEL);
			if (damageLogPanel)
			{
				if (this.logs)
				{
					damageLogPanel._detailsTopContainer.removeChild(this.logs[0])
					damageLogPanel._detailsBottomContainer.removeChild(this.logs[1])
				}
				var top:TextExt = new TextExt(position.x + 35, position.y, null, position.align, damageLogPanel._detailsTopContainer, top_enabled);
				var bottom:TextExt = new TextExt(position.x + 20, position.y, null, position.align, damageLogPanel._detailsBottomContainer, bottom_enabled);
				this.logs = new <TextExt>[top, bottom];
				this.logs.fixed = true;
			}
		}
		
		public function as_updateTopLog(text:String):void
		{
			this.top_log.htmlText = text;
		}
		
		public function as_updateExtendedLog(log_id:int, text:String):void
		{
			if (this.logs)
			{
				this.logs[log_id].htmlText = text;
			}
		}
		
		override public function onResizeHandle(event:Event):void
		{
			if (this.top_log && this.top_log_inCenter)
			{
				this.x = Math.ceil(App.appWidth >> 1);
			}
		}
	}
}