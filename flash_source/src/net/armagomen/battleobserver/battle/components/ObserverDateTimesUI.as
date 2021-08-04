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
				var x:Number = settings.x < 0 ? App.appWidth + settings.x : settings.x;
				var y:Number = settings.y < 0 ? App.appHeight + settings.y : settings.y;
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
			dateTime.x = config.x < 0 ? App.appWidth + config.x : config.x;
			dateTime.y = config.y < 0 ? App.appHeight + config.y : config.y;
		}
	}

}