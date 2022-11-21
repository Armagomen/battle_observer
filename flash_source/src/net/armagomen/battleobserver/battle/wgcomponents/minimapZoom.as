package net.armagomen.battleobserver.battle.wgcomponents
{
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class minimapZoom
	{
		private var oldSize:Number  = 2.0;
		private var oldScale:Number = 1.0;
		private var minimap:*       = null;
		private var page:*          = null;
		
		public function minimapZoom(page:*)
		{
			super();
			this.page = page;
			this.minimap = this.page.getComponent(BATTLE_VIEW_ALIASES.MINIMAP);
			this.page.addChild(this.minimap);
			App.graphicsOptimizationMgr.unregister(this.minimap);
		}
		
		public function minimapCentered(enabled:Boolean):void
		{
			if (this.minimap)
			{
				if (enabled && !this.page.as_isComponentVisible(BATTLE_VIEW_ALIASES.FULL_STATS))
				{
					this.oldSize = this.minimap.currentSizeIndex;
					this.oldScale = this.minimap.scaleX;
					this.minimap.setAllowedSizeIndex(5.0);
					var newScale:Number = (App.appHeight * 0.7) / this.minimap.currentWidth;
					this.minimap.scaleX = this.minimap.scaleY = newScale;
					this.minimap.x = App.appWidth * 0.5 - this.minimap.currentWidth * 0.5 * newScale;
					this.minimap.y = App.appHeight * 0.5 - this.minimap.currentHeight * 0.5 * newScale;
				}
				else
				{
					this.minimap.setAllowedSizeIndex(this.oldSize);
					this.minimap.scaleX = this.minimap.scaleY = this.oldScale;
					this.minimap.x = App.appWidth - this.minimap.currentWidth;
					this.minimap.y = App.appHeight - this.minimap.currentHeight;
				}
				this.page.showComponent(BATTLE_VIEW_ALIASES.PLAYER_MESSAGES, !enabled);
			}
			else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] minimapCentered - minimap is Null !!!");
		}
	}
}