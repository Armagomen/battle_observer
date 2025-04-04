package net.armagomen.battle_observer.battle.components
{
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class MinimapUI extends ObserverBattleDisplayable
	{
		private var oldSize:Number  = 2.0;
		private var oldScale:Number = 1.0;
		private var minimap:*       = null;
		private var page:*          = null;
		
		public function MinimapUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			this.page = parent;
			this.minimap = this.page.getComponent(BATTLE_VIEW_ALIASES.MINIMAP);
			this.page.addChild(this.minimap);
			App.graphicsOptimizationMgr.unregister(this.minimap);
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.page = null;
			this.minimap = null;
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
					var newScale:Number = (App.appHeight * 0.65) / this.minimap.currentWidth;
					this.minimap.scaleX = this.minimap.scaleY = newScale;
					this.minimap.x = (App.appWidth >> 1) - (this.minimap.currentWidth >> 1) * newScale;
					this.minimap.y = (App.appHeight >> 1) - (this.minimap.currentHeight >> 1) * newScale;
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