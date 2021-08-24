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
		
		override protected function onPopulate():void 
		{
			super.onPopulate();
			if (this.dateTime == null)
			{
				this.settings = this.getSettings().battle;
				var x:Number = this.settings.x < 0 ? App.appWidth + this.settings.x : this.settings.x;
				var y:Number = this.settings.y < 0 ? App.appHeight + this.settings.y : this.settings.y;
				this.dateTime = new TextExt(x, y, Filters.largeText, TextFieldAutoSize.LEFT, getShadowSettings(), this);
			}
		}
		
		public function as_setDateTime(text:String):void
		{
			if (dateTime)
			{
				this.dateTime.htmlText = text;
			}
		}
		
		override public function onResizeHandle(event:Event):void
		{
			this.dateTime.x = this.settings.x < 0 ? App.appWidth + this.settings.x : this.settings.x;
			this.dateTime.y = this.settings.y < 0 ? App.appHeight + this.settings.y : this.settings.y;
		}
	}

}