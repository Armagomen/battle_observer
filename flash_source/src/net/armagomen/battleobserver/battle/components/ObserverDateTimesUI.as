package net.armagomen.battleobserver.battle.components
{
	import flash.events.Event;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class ObserverDateTimesUI extends ObserverBattleDispalaysble
	{
		private var dateTime:TextExt;
		private var settings:Object;
		
		public function ObserverDateTimesUI()
		{
			super();
		}
		
		public function as_startUpdate(settings:Object):void
		{
			if (this.dateTime == null)
			{
				this.settings = settings;
				var x:Number = settings.x < 0 ? App.appWidth + settings.x : settings.x;
				var y:Number = settings.y < 0 ? App.appHeight + settings.y : settings.y;
				dateTime = new TextExt("time", x, y, Filters.largeText, TextFieldAutoSize.LEFT, getShadowSettings(), this);
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
			dateTime.x = settings.x < 0 ? App.appWidth + settings.x : settings.x;
			dateTime.y = settings.y < 0 ? App.appHeight + settings.y : settings.y;
		}
	}

}