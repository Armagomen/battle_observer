package net.armagomen.battleobserver.battle.components.wgcomponents
{
	import flash.events.Event;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.views.minimap.Minimap;
	
	public class MinimapUI extends ObserverBattleDisplayable
	{
		private var newScale:Number   = 1.0;
		private var vpos:Number       = 150.0;
		private var sizeBefore:Number = 2.0;
		private var minimap:Minimap   = null;
		
		public function MinimapUI(minimap:Minimap)
		{
			this.minimap = minimap;
			super();
		}
		
		public function as_startUpdate(num:Number):void
		{
			if (this.minimap)
			{
				App.graphicsOptimizationMgr.unregister(this.minimap);
			}
			else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_startUpdate - minimap is Null !!!");
			vpos = num * 2;
			newScale = Math.max((App.appHeight - vpos) / 630, 1.0);
		}
		
		public function as_MinimapCentered(enabled:Boolean):void
		{
			if (this.minimap)
			{
				if (enabled)
				{
					sizeBefore = this.minimap.currentSizeIndex;
					var offset:Number = 315 * newScale;
					this.minimap.setAllowedSizeIndex(5.0);
					this.minimap.scaleX = this.minimap.scaleY = newScale;
					this.minimap.x = App.appWidth * 0.5 - offset;
					this.minimap.y = App.appHeight * 0.5 - offset;
				}
				else
				{
					this.minimap.setAllowedSizeIndex(sizeBefore);
					this.minimap.scaleX = this.minimap.scaleY = 1.0;
					this.minimap.x = App.appWidth - this.minimap.currentWidth;
					this.minimap.y = App.appHeight - this.minimap.currentHeight;
				}
				var battlePage:* = this.minimap.parent;
				battlePage.showComponent(BATTLE_VIEW_ALIASES.PLAYER_MESSAGES, !enabled);
			}
			else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_MinimapCentered - minimap is Null !!!");
		}
		
		override public function onResizeHandle(event:Event):void
		{
			newScale = Math.max((App.appHeight - vpos) / 630, 1.0);
		}
	}
}