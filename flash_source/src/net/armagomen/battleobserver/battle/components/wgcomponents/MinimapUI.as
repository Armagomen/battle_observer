package net.armagomen.battleobserver.battle.components.wgcomponents
{
	import flash.events.Event;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.views.minimap.Minimap;
	
	public class MinimapUI extends ObserverBattleDisplayable
	{
		private var sizeBefore:Number = 2.0;
		private var minimap:Minimap   = null;
		public var getIndent:Function
		
		public function MinimapUI(minimap:Minimap)
		{
			this.minimap = minimap;
			super();
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.minimap = null;
		}
		
		public function as_MinimapCentered(enabled:Boolean):void
		{
			if (this.minimap)
			{
				if (enabled)
				{
					var newScale:Number = Math.max((App.appHeight - this.getIndent() * 2) / 630, 1.0);
					this.sizeBefore = this.minimap.currentSizeIndex;
					this.minimap.setAllowedSizeIndex(5.0);
					this.minimap.scaleX = this.minimap.scaleY = newScale;
					this.minimap.x = App.appWidth * 0.5 - 315 * newScale;
					this.minimap.y = App.appHeight * 0.5 - 315 * newScale;
				}
				else
				{
					this.minimap.setAllowedSizeIndex(this.sizeBefore);
					this.minimap.scaleX = this.minimap.scaleY = 1.0;
					this.minimap.x = App.appWidth - this.minimap.currentWidth;
					this.minimap.y = App.appHeight - this.minimap.currentHeight;
				}
				var page:* = this.minimap.parent;
				page.showComponent(BATTLE_VIEW_ALIASES.PLAYER_MESSAGES, !enabled);
			}
			else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_MinimapCentered - minimap is Null !!!");
		}
	}
}