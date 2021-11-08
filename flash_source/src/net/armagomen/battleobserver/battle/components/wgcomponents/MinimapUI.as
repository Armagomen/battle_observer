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
		private var offset:Number     = 315.0;
		
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
				this.parent.addChild(this.minimap);
			}
			else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_startUpdate - minimap is Null !!!");
			this.vpos = num * 2;
			this.newScale = Math.max((App.appHeight - vpos) / 630, 1.0);
			this.offset = 315 * newScale;
		}
		
		public function as_MinimapCentered(enabled:Boolean):void
		{
			if (this.minimap)
			{
				if (enabled)
				{
					this.sizeBefore = this.minimap.currentSizeIndex;
					this.minimap.setAllowedSizeIndex(5.0);
					this.minimap.scaleX = this.minimap.scaleY = this.newScale;
					this.minimap.x = App.appWidth * 0.5 - this.offset;
					this.minimap.y = App.appHeight * 0.5 - this.offset;
				}
				else
				{
					this.minimap.setAllowedSizeIndex(this.sizeBefore);
					this.minimap.scaleX = this.minimap.scaleY = 1.0;
					this.minimap.x = App.appWidth - this.minimap.currentWidth;
					this.minimap.y = App.appHeight - this.minimap.currentHeight;
				}
				var battlePage:* = this.parent;
				battlePage.showComponent(BATTLE_VIEW_ALIASES.PLAYER_MESSAGES, !enabled);
			}
			else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_MinimapCentered - minimap is Null !!!");
		}
		
		override public function onResizeHandle(event:Event):void
		{
			newScale = Math.max((App.appHeight - this.vpos) / 630, 1.0);
		}
	}
}