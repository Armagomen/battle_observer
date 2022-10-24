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
		private var mainlog:TextExt          = null;
		private const IN_LOG:String          = "in_log";
		private const D_LOG:String           = "d_log";
		
		public function DamageLogsUI(battlePage:*)
		{
			super();
			this.damageLogPanel = battlePage.getComponent(BATTLE_VIEW_ALIASES.BATTLE_DAMAGE_LOG_PANEL);
		}
		
		override protected function onBeforeDispose():void 
		{
			super.onBeforeDispose();
			this.removeChildren();
			this.d_log = null;
			this.in_log = null;
			this.mainlog = null;
		}
		
		public function as_startUpdate(logTotal:Object, logExtended:Object):void
		{
			if (logTotal.enabled)
			{
				this.top_log_inCenter = logTotal.settings.inCenter;
				this.x = !this.top_log_inCenter ? 0 : Math.ceil(App.appWidth >> 1);
				this.mainlog = new TextExt(logTotal.settings.x, logTotal.settings.y, Filters.largeText, logTotal.settings.align, getShadowSettings(), this);
			}
			if (logExtended.enabled)
			{
				if (this.damageLogPanel)
				{
					var topContainer:* = this.damageLogPanel._detailsTopContainer;
					this.d_log = new TextExt(logExtended.settings.x + 35, logExtended.settings.y, null, logExtended.settings.align, getShadowSettings(), topContainer);
					var bottomContainer:* = this.damageLogPanel._detailsBottomContainer;
					this.in_log = new TextExt(logExtended.settings.x + 20, -45 + logExtended.settings.y, null, logExtended.settings.align, getShadowSettings(), bottomContainer);
				}
			}
		}
		
		public function as_updateDamage(text:String):void
		{
			if (this.mainlog)
			{
				this.mainlog.htmlText = text;
			}
		}
		
		public function as_updateLog(target:String, text:String):void
		{
			if (target == D_LOG && this.d_log)
			{
				this.d_log.htmlText = text;
			}
			else if (target == IN_LOG && this.in_log)
			{
				this.in_log.htmlText = text;
			}
		}
		
		override public function onResizeHandle(event:Event):void
		{
			if (this.mainlog && this.top_log_inCenter)
			{
				this.x = Math.ceil(App.appWidth >> 1);
			}
		}
	}
}