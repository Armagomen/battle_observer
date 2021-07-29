package net.armagomen.battleobserver.battle.components.debugpanel
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.ProgressBar;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.data.constants.Time;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.*;
	
	public class ObserverDebugPanelUI extends BattleDisplayable
	{
		private var debugText:TextExt      = null;
		private var fpsBar:ProgressBar     = null;
		private var pingBar:ProgressBar    = null;
		private var graphEnabled:Boolean   = false;
		private var fpsBarEnabled:Boolean  = false;
		private var pingBarEnabled:Boolean = false;
		private var maxFps:Number          = 0.02;
		public var getShadowSettings:Function;
		public var animationEnabled:Function;
		private var loaded:Boolean         = false;
		
		public function ObserverDebugPanelUI()
		{
			super();
		}
		
		override protected function onDispose():void
		{
			this.fpsBar = null;
			this.pingBar = null;
			super.onDispose();
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
		
		public function as_startUpdate(data:Object, vSync:Boolean, limit:int):void
		{
			if (!this.loaded)
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
							this.maxFps = limit * 0.01;
						}
						var fps:Object       = data.debugGraphics.fpsBar;
						var fpsfilters:Array = [Filters.handleGlowFilter(fps.glowFilter)];
						fpsBar = this.addChild(new ProgressBar(animationEnabled(), fps.x, fps.y, fps.width, fps.height, fps.alpha, fps.bgAlpha, fpsfilters, fps.color, null, 0.3)) as ProgressBar;
						App.utils.data.cleanupDynamicObject(fps);
					}
					
					if (this.pingBarEnabled)
					{
						var ping:Object       = data.debugGraphics.pingBar;
						var pingfilters:Array = [Filters.handleGlowFilter(ping.glowFilter)];
						pingBar = this.addChild(new ProgressBar(animationEnabled(), ping.x, ping.y, ping.width, ping.height, ping.alpha, ping.bgAlpha, pingfilters, ping.color, null, 0.3)) as ProgressBar;
						App.utils.data.cleanupDynamicObject(ping);
					}
				}
				this.debugText = new TextExt("_debugPanel", data.debugText.x, data.debugText.y, Filters.largeText, TextFieldAutoSize.LEFT, getShadowSettings(), this);
				var battlePage:* = parent;
				var debugPanel:* = battlePage.getComponent(BATTLE_VIEW_ALIASES.DEBUG_PANEL);
				if (debugPanel)
				{
					battlePage.removeChild(debugPanel);
				}
				App.utils.data.cleanupDynamicObject(data);
				this.loaded = true;
				y
			}
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
						fpsBar.setNewScale(Math.min(1.0, fps * this.maxFps));
					}
					if (this.pingBarEnabled)
					{
						pingBar.setNewScale(Math.max(0.0, 1.0 - ping * 0.02));
					}
				}
			}
		}
	}
}