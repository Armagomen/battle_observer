package net.armagomen.battleobserver.battle.components.debugpanel
{
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.ProgressBar;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class ObserverDebugPanelUI extends ObserverBattleDisplayable
	{
		private var debugText:TextExt      = null;
		private var fpsBar:ProgressBar     = null;
		private var pingBar:ProgressBar    = null;
		private var graphEnabled:Boolean   = false;
		private var fpsBarEnabled:Boolean  = false;
		private var pingBarEnabled:Boolean = false;
		private var maxFps:int             = 200;
		
		public var isVerticalSync:Function;
		public var getRefreshRate:Function;
		
		public function ObserverDebugPanelUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			if (this.debugText == null)
			{
				var settings:Object = this.getSettings();
				this.graphEnabled = Boolean(settings.debugGraphics.enabled);
				if (this.graphEnabled)
				{
					this.fpsBarEnabled = Boolean(settings.debugGraphics.fpsBar.enabled);
					this.pingBarEnabled = Boolean(settings.debugGraphics.pingBar.enabled);
					
					if (this.fpsBarEnabled)
					{
						if (this.isVerticalSync())
						{
							this.maxFps = this.getRefreshRate();
						}
						var fps:Object       = settings.debugGraphics.fpsBar;
						var fpsfilters:Array = [Filters.handleGlowFilter(fps.glowFilter)];
						this.fpsBar = new ProgressBar(fps.x, fps.y, fps.width, fps.height, fps.alpha, fps.bgAlpha, fpsfilters, fps.color, null, 0);
						this.addChild(this.fpsBar);
					}
					
					if (this.pingBarEnabled)
					{
						var ping:Object       = settings.debugGraphics.pingBar;
						var pingfilters:Array = [Filters.handleGlowFilter(ping.glowFilter)];
						this.pingBar = new ProgressBar(ping.x, ping.y, ping.width, ping.height, ping.alpha, ping.bgAlpha, pingfilters, ping.color, null, 0);
						this.addChild(this.pingBar);
					}
				}
				this.debugText = new TextExt(settings.debugText.x, settings.debugText.y, Filters.largeText, TextFieldAutoSize.LEFT, this.getShadowSettings(), this);
			}
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			if (this.graphEnabled)
			{
				if (this.fpsBarEnabled)
				{
					this.fpsBar.remove();
					this.fpsBar = null;
				}
				if (this.pingBarEnabled)
				{
					this.pingBar.remove();
					this.pingBar = null;
				}
			}
			this.debugText = null;
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
						fpsBar.setNewScale(fps / this.maxFps);
					}
					if (this.pingBarEnabled)
					{
						pingBar.setNewScale(1.0 - ping / 200);
					}
				}
			}
		}
	}
}