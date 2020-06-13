package net.armagomen.battleobserver.battle.components.debugpanel
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.utils.Filters;
	import net.armagomen.battleobserver.battle.utils.ProgressBar;
	import net.armagomen.battleobserver.battle.utils.TextExt;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.*;

	public class ObserverDebugPanelUI extends BattleDisplayable
	{
		private var debugText:TextField;
		private var fpsBar:ProgressBar = null;
		private var pingBar:ProgressBar = null;
		private var graphEnabled:Boolean = false;
		private var fpsBarEnabled:Boolean = false;
		private var pingBarEnabled:Boolean = false;
		private var maxFps:int = 200;
		public var getShadowSettings:Function;

		public function ObserverDebugPanelUI(compName:String)
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
		}

		public function as_clearScene():void
		{
			while (this.numChildren > 0)
			{
				this.removeChildAt(0);
			}
			this.debugText = null;
			this.fpsBar = null;
			this.pingBar = null;
			var page:* = parent;
			page.unregisterComponent(this.name);
		}

		public function as_startUpdate(data:Object, vSync:Boolean, limit:int):void
		{
			this.graphEnabled = Boolean(data.debugGraphics.enabled);
			if (this.graphEnabled)
			{
				this.fpsBarEnabled = Boolean(data.debugGraphics.fpsBar.enabled);
				this.pingBarEnabled = Boolean(data.debugGraphics.pingBar.enabled);

				if (this.fpsBarEnabled)
				{
					if (vSync)
					{
						this.maxFps = limit;
					}
					var fps:Object = data.debugGraphics.fpsBar;
					var fpsfilters:Array = [Filters.handleGlowFilter(fps.glowFilter)];
					fpsBar = this.addChild(new ProgressBar(fps.x, fps.y, fps.width, fps.height, fps.alpha, fps.bgAlpha, fpsfilters, fps.color)) as ProgressBar;
					App.utils.data.cleanupDynamicObject(fps);
				}

				if (this.pingBarEnabled)
				{
					var ping:Object = data.debugGraphics.pingBar;
					var pingfilters:Array = [Filters.handleGlowFilter(ping.glowFilter)];
					pingBar = this.addChild(new ProgressBar(ping.x, ping.y, ping.width, ping.height, ping.alpha, ping.bgAlpha, pingfilters, ping.color)) as ProgressBar;
					App.utils.data.cleanupDynamicObject(ping);
				}
			}
			this.debugText = new TextExt("_debugPanel", data.debugText.x, data.debugText.y, Filters.largeText, TextFieldAutoSize.LEFT, getShadowSettings(), this);
			var battlePage:* = parent;
			if (battlePage._componentsStorage.hasOwnProperty(BATTLE_VIEW_ALIASES.DEBUG_PANEL)){
				battlePage.removeChild(battlePage.getComponent(BATTLE_VIEW_ALIASES.DEBUG_PANEL));
			}
			App.utils.data.cleanupDynamicObject(data);
		}

		public function as_fpsPing(debug:String, fps:int, ping:int):void
		{
			if (this.debugText)
			{
				this.debugText.htmlText = debug;
				if (this.graphEnabled)
				{
					if (this.fpsBarEnabled)
					{
						fpsBar.bar.scaleX = Math.min(1.0, fps / this.maxFps);
					}
					if (this.pingBarEnabled)
					{
						pingBar.bar.scaleX = Math.max(0.0, 1.0 - ping / 200);
					}
				}
			}
		}
	}
}