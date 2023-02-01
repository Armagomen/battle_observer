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
		private var damageLogPanel:*         = null;
		private var d_log:TextExt            = null;
		private var in_log:TextExt           = null;
		private var top_log:TextExt          = null;
		private const D_LOG:String           = "d_log";
		
		public function DamageLogsUI(dlPanel:*)
		{
			super();
			this.damageLogPanel = dlPanel;
		}
		
		override protected function onBeforeDispose():void 
		{
			super.onBeforeDispose();
			this.removeChildren();
			this.d_log = null;
			this.in_log = null;
			this.top_log = null;
		}
		
		public function as_createTopLog(settings:Object):void
		{
			this.top_log_inCenter = settings.inCenter;
			this.x = !this.top_log_inCenter ? 0 : Math.ceil(App.appWidth >> 1);
			this.top_log = new TextExt(settings.x, settings.y, Filters.largeText, settings.align, getShadowSettings(), this);
		}
		
		public function as_createExtendedLogs(settings:Object):void
		{
			if (this.damageLogPanel)
			{
				this.d_log = new TextExt(settings.x + 35, settings.y, null, settings.align, getShadowSettings(), this.damageLogPanel._detailsTopContainer);
				this.in_log = new TextExt(settings.x + 20, settings.y - 20, null, settings.align, getShadowSettings(), this.damageLogPanel._detailsBottomContainer);
			}
		}
		
		public function as_updateTopLog(text:String):void
		{
			this.top_log.htmlText = text;
		}
		
		public function as_updateExtendedLog(target:String, text:String):void
		{
			if (target == D_LOG)
			{
				this.d_log.htmlText = text;
			}
			else
			{
				this.in_log.htmlText = text;
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