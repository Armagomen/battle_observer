package net.armagomen.battleobserver.battle.components
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class ObserverDateTimesUI extends ObserverBattleDispalaysble
	{
		private var dateTime:TextField;
		private var config:Object;
		public var getShadowSettings:Function;
		private var loaded:Boolean = false;
		
		public function ObserverDateTimesUI()
		{
			super();
		}
		
		public function as_startUpdate(settings:Object):void
		{
			if (!this.loaded)
			{
				this.config = settings;
				var x:int = settings.x;
				if (x < 0)
				{
					x = App.appWidth + x;
				}
				var y:int = settings.y;
				if (y < 0)
				{
					y = App.appHeight + y;
				}
				dateTime = new TextExt("time", x, y, Filters.largeText, TextFieldAutoSize.LEFT, getShadowSettings(), this);
				this.loaded = true;
			}
		}
		
		public function as_setDateTime(text:String):void
		{
			if (dateTime)
			{
				dateTime.htmlText = text;
			}
		}
		
		override public function onResizeHandle(event:Event):void
		{
			var x:int = config.x;
			if (x < 0)
			{
				x = App.appWidth + x;
			}
			var y:int = config.y;
			if (y < 0)
			{
				y = App.appHeight + y;
			}
			dateTime.x = x;
			dateTime.y = y;
		}
	}

}