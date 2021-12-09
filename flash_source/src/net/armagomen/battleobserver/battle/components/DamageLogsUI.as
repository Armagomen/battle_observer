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
		private var top_Log:Sprite           = null;
		private var top_log_inCenter:Boolean = true;
		private var enableds:Object          = null;
		private var d_log:TextExt            = null;
		private var in_log:TextExt           = null;
		private var mainlog:TextExt          = null;
		private var damageLogPanel:*         = null;
		private const IN_LOG:String          = "in_log";
		private const D_LOG:String           = "d_log";
		
		public function DamageLogsUI(logsPanel:*)
		{
			super();
			this.damageLogPanel = logsPanel;
		}
		
		override protected function onBeforeDispose():void 
		{
			super.onBeforeDispose();
			if (this.top_Log)
			{
				this.top_Log.removeChildren();
				this.top_Log = null;
			}
			App.utils.data.cleanupDynamicObject(this.enableds);
			this.d_log = null;
			this.in_log = null;
			this.mainlog = null;
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
					if (this.damageLogPanel)
					{
						if (this.enableds[D_LOG])
						{
							var topContainer:* = this.damageLogPanel._detailsTopContainer;
							this.d_log = new TextExt(data.d_log.x + 25, data.d_log.y, null, data.d_log.align, getShadowSettings(), topContainer);
						}
						if (this.enableds[IN_LOG])
						{
							var bottomContainer:* = this.damageLogPanel._detailsBottomContainer;
							this.in_log = new TextExt(data.in_log.x + 10, -25 + data.in_log.y, null, data.in_log.align, getShadowSettings(), bottomContainer);
						}
						this.damageLogPanel.updateContainersPosition();
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