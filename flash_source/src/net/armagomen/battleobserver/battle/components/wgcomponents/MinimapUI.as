package net.armagomen.battleobserver.battle.components.wgcomponents
{
	import flash.events.*;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.views.minimap.Minimap;
	
	public class MinimapUI extends ObserverBattleDispalaysble
	{
		private var newScale:Number      = 1.0;
		private var vpos:Number          = 150.0;
		private var sizeBefore:Number    = 2.0;
		private var indexChanged:Boolean = false;
		
		public function MinimapUI()
		{
			super();
		}
		
		private function getMinimap():*
		{
			var battlePage:* = parent;
			if (battlePage._componentsStorage.hasOwnProperty(BATTLE_VIEW_ALIASES.MINIMAP))
			{
				return battlePage.getComponent(BATTLE_VIEW_ALIASES.MINIMAP);
			}
			return null;
		}
		
		public function as_startUpdate(num:Number):void
		{
			var minimap:Minimap = this.getMinimap();
			if (minimap)
			{
				App.graphicsOptimizationMgr.unregister(minimap);
			}
			else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_startUpdate - minimap is Null !!!");
			vpos = num * 2;
			newScale = Math.max((App.appHeight - vpos) / 630, 1.0);
		}
		
		public function as_MinimapCentered(enabled:Boolean):void
		{
			var minimap:Minimap = this.getMinimap();
			if (minimap)
			{
				if (!this.indexChanged)
				{
					parent.setChildIndex(minimap, parent.numChildren - 1);
					this.indexChanged = true;
				}
				if (enabled)
				{
					sizeBefore = minimap.currentSizeIndex;
					var offset:Number = 315 * newScale;
					minimap.setAllowedSizeIndex(5.0);
					minimap.scaleX = minimap.scaleY = newScale;
					minimap.x = App.appWidth * 0.5 - offset;
					minimap.y = App.appHeight * 0.5 - offset;
				}
				else
				{
					minimap.setAllowedSizeIndex(sizeBefore);
					minimap.scaleX = minimap.scaleY = 1.0;
					minimap.x = App.appWidth - minimap.currentWidth;
					minimap.y = App.appHeight - minimap.currentHeight;
				}
				var battlePage:* = parent;
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