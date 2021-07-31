package net.armagomen.battleobserver.battle.components
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.gui.battle.components.*;

	public class OwnHealthUI extends BattleDisplayable
	{
		private var own_health:TextField;
		public var getShadowSettings:Function;
		private var loaded:Boolean = false;

		public function OwnHealthUI()
		{
			super();
		}

		public function as_startUpdate(data:Object):void
		{
			if (this.loaded) return;
			own_health = new TextExt("own_health", data.x, data.y, Filters.middleText, data.align, getShadowSettings(), this);
			App.utils.data.cleanupDynamicObject(data);
			this.loaded = true;
		}

		public function as_setOwnHealth(text:String):void
		{
			own_health.htmlText = text;
		}
		
		public function as_onCrosshairPositionChanged(x:Number, y:Number):void
		{
			this.x = x;
			this.y = y;
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
	}
}