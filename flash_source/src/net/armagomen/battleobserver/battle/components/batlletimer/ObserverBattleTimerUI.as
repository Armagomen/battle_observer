package net.armagomen.battleobserver.battle.components.batlletimer
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.utils.Filters;
	import net.armagomen.battleobserver.battle.utils.TextExt;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.*;

	public class ObserverBattleTimerUI extends BattleDisplayable
	{
		private var battleTimer:TextField;
		public var getShadowSettings:Function;

		public function ObserverBattleTimerUI(compName:String)
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
			this.addEventListener(Event.RESIZE, this._onResizeHandle);
		}

		override protected function onDispose():void
		{
			this.removeEventListener(Event.RESIZE, this._onResizeHandle);
			super.onDispose();
		}

		public function as_startUpdate():void
		{
			this.x = App.appWidth;
			this.battleTimer = new TextExt("_timer", -8, 0, Filters.largeText, TextFieldAutoSize.RIGHT, getShadowSettings(), this);
			var battlaPage:* = parent;
			var component:* = battlaPage._componentsStorage.hasOwnProperty(BATTLE_VIEW_ALIASES.BATTLE_TIMER) ? battlaPage.getComponent(BATTLE_VIEW_ALIASES.BATTLE_TIMER) : null;
			if (component)
			{
				parent.removeChild(component);
			}
		}

		public function as_timer(timer:String):void
		{
			if (this.battleTimer)
			{
				this.battleTimer.htmlText = timer;
			}
		}

		public function _onResizeHandle(event:Event):void
		{
			this.x = App.appWidth;
		}
	}

}