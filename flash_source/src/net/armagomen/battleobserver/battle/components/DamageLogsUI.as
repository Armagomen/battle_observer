package net.armagomen.battleobserver.battle.components
{
	import flash.display.Sprite;
	import flash.events.Event;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class DamageLogsUI extends ObserverBattleDispalaysble
	{
		private var top_Log:Sprite           = null;
		private var top_log_inCenter:Boolean = true;
		private var enableds:Object          = null;
		private var d_log:TextExt            = null;
		private var in_log:TextExt           = null;
		private var mainlog:TextExt          = null;
		
		private const IN_LOG:String          = "in_log";
		private const D_LOG:String           = "d_log";
		
		public function DamageLogsUI()
		{
			super();
		}
		
		public function as_startUpdate(data:Object, turned:Object):void
		{
			if (this.top_Log == null)
			{
				this.top_Log = new Sprite();
				this.enableds = turned;
				if (this.enableds.main)
				{
					this.top_log_inCenter = data.main.inCenter;
					this.top_Log.x = !this.top_log_inCenter ? 0 : Math.ceil(App.appWidth >> 1);
					this.mainlog = new TextExt(data.main.x, data.main.y, Filters.largeText, data.main.align, getShadowSettings(), this.top_Log);
					this.addChild(this.top_Log);
				}
				if (this.enableds[D_LOG] || this.enableds[IN_LOG])
				{
					var page:*                 = this.parent;
					var battleDamageLogPanel:* = page.getComponent(BATTLE_VIEW_ALIASES.BATTLE_DAMAGE_LOG_PANEL);
					if (battleDamageLogPanel)
					{
						if (this.enableds[D_LOG])
						{
							var topContainer:* = battleDamageLogPanel._detailsTopContainer;
							this.d_log = new TextExt(data.d_log.x + 25, data.d_log.y, null, data.d_log.align, getShadowSettings(), topContainer);
						}
						if (this.enableds[IN_LOG])
						{
							var bottomContainer:* = battleDamageLogPanel._detailsBottomContainer;
							this.in_log = new TextExt(data.in_log.x + 10, -25 + data.in_log.y, null, data.in_log.align, getShadowSettings(), bottomContainer);
						}
						battleDamageLogPanel.updateContainersPosition();
					}
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
			if (target == D_LOG && this.d_log && this.enableds[target])
			{
				this.d_log.htmlText = text;
			}
			else if (target == IN_LOG && this.in_log && this.enableds[target])
			{
				this.in_log.htmlText = text;
			}
		}
		
		override public function onResizeHandle(event:Event):void
		{
			if (this.top_Log && this.top_log_inCenter)
			{
				this.top_Log.x = Math.ceil(App.appWidth >> 1);
			}
		}
	}
}