package net.armagomen.battleobserver.battle.wgcomponents
{
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.KeyboardEvent;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.views.BaseBattlePage;
	import net.wg.gui.battle.views.minimap.Minimap;
	import flash.ui.Keyboard;
	
	public class MinimapUI extends Sprite
	{
		private var sizeBefore:Number = 2.0;
		private var minimap:Minimap   = null;
		private var page:*            = null;
		private var isKeyDown:Boolean = false;
		
		public function MinimapUI(page:*)
		{
			super();
			this.page = page;
			this.minimap = this.page.getComponent(BATTLE_VIEW_ALIASES.MINIMAP);
			this.page.addChild(this.minimap);
			App.graphicsOptimizationMgr.unregister(this.minimap);
			App.stage.addEventListener(KeyboardEvent.KEY_DOWN, this.keyDownHandler, false, 1, true);
			App.stage.addEventListener(KeyboardEvent.KEY_UP, this.keyUpHandler, false, 1, true);
		}
		
		private function keyDownHandler(event:KeyboardEvent):void
		{
			DebugUtils.LOG_WARNING("keyDownHandler " + event.keyCode);
			if (event.keyCode == Keyboard.CONTROL && !this.isKeyDown)
			{
				this.isKeyDown = true;
				this.minimapCentered(this.isKeyDown);
			}
		}
		
		private function keyUpHandler(event:KeyboardEvent):void
		{
			if (event.keyCode == Keyboard.CONTROL && this.isKeyDown)
			{
				this.isKeyDown = false;
				this.minimapCentered(this.isKeyDown);
			}
		}
		
		private function minimapCentered(enabled:Boolean):void
		{
			if (this.minimap)
			{
				if (enabled)
				{
					var newScale:Number = Math.max((App.appHeight - App.appHeight / 8) / 630, 1.0);
					this.sizeBefore = this.minimap.currentSizeIndex;
					this.minimap.setAllowedSizeIndex(5);
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
				this.page.showComponent(BATTLE_VIEW_ALIASES.PLAYER_MESSAGES, !enabled);
			}
			else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] minimapCentered - minimap is Null !!!");
		}
	}
}