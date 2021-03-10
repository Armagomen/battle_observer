package net.armagomen.battleobserver.battle.components
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.*;
	import DebugUtils;

	public class DamageLogsUI extends BattleDisplayable
	{
		private var top_Log:Sprite = null;
		private var top_log_inCenter:Boolean = true;
		private var enableds:Object = null;
		private var d_log:TextField = null;
		private var in_log:TextField = null;
		private var mainlog:TextField = null;
		public var getShadowSettings:Function;
		
		private const IN_LOG:String = "in_log";
		private const D_LOG:String = "d_log";

		public function DamageLogsUI(compName:String)
		{
			super();
			this.name = compName;
		}

		override protected function configUI():void
		{
			super.configUI();
			this.tabEnabled = false;
			this.tabChildren = false;
			this.mouseEnabled = false;
			this.mouseChildren = false;
			this.buttonMode = false;
			this.addEventListener(Event.RESIZE, this._onResizeHandle);
		}

		override protected function onDispose():void
		{
			this.removeEventListener(Event.RESIZE, this._onResizeHandle);
			super.onDispose();
		}

		public function as_startUpdate(data:Object, turned:Object):void
		{
			this.enableds = turned;
			var shadowSettings:Object = getShadowSettings();
			if (this.enableds.main){
				this.top_log_inCenter = data.main.inCenter;
				this.top_Log = new Sprite();
				this.top_Log.x = !this.top_log_inCenter ? 0 : Math.ceil((App.appWidth >> 1));
				this.mainlog = new TextExt("damage", data.main.x, data.main.y, Filters.largeText, data.main.align, shadowSettings, this.top_Log);
				this.addChild(this.top_Log);
			}
			if (this.enableds[D_LOG] || this.enableds[IN_LOG]){
				var page:* = this.parent;
				var battleDamageLogPanel:* = page.getComponent(BATTLE_VIEW_ALIASES.BATTLE_DAMAGE_LOG_PANEL);
				if (battleDamageLogPanel){
					if (this.enableds[D_LOG]){
						var topContainer:* = battleDamageLogPanel._detailsTopContainer;
						this.d_log = new TextExt(D_LOG, data.d_log.x + 25, data.d_log.y, Filters.normalText, data.d_log.align, shadowSettings, topContainer);
					}
					if (this.enableds[IN_LOG]){
						var bottomContainer:* = battleDamageLogPanel._detailsBottomContainer;
						this.in_log = new TextExt(IN_LOG, data.in_log.x + 10, -25 + data.in_log.y, Filters.normalText, data.in_log.align, shadowSettings, bottomContainer);
					}
					battleDamageLogPanel.updateContainersPosition();
				}
			}
			App.utils.data.cleanupDynamicObject(data);
		}

		public function as_updateDamage(text:String):void
		{
			if (this.mainlog){
				this.mainlog.htmlText = text;
			}
		}

		public function as_updateLog(target:String, text:String):void
		{
			if (target == D_LOG && this.d_log && this.enableds[target]){
				this.d_log.htmlText = text;
			}
			else if (target == IN_LOG && this.in_log && this.enableds[target]){
				this.in_log.htmlText = text;
			}
		}

		private function _onResizeHandle(event:Event):void
		{
			if (this.top_Log && this.top_log_inCenter)
			{
				this.top_Log.x = Math.ceil((App.appWidth >> 1));
			}
		}
	}
}