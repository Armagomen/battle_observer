﻿package net.armagomen.battle_observer.battle.components
{
	import flash.events.Event;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	
	public class ObserverDateTimesUI extends ObserverBattleDisplayable
	{
		private var dateTime:TextExt;
		private var settings:Object;
		
		public function ObserverDateTimesUI()
		{
			super();
		}
		
		override protected function onPopulate():void 
		{
			
			if (not_initialized)
			{
				super.onPopulate();
				this.settings = this.getSettings().battle;
				var x:Number = this.settings.x < 0 ? App.appWidth + this.settings.x : this.settings.x;
				var y:Number = this.settings.y < 0 ? App.appHeight + this.settings.y : this.settings.y;
				this.dateTime = new TextExt(x, y, Constants.largeText, TextFieldAutoSize.LEFT, this);
			}
			else
			{
				super.onPopulate();
			}
		}
		
		override protected function onBeforeDispose():void 
		{
			super.onBeforeDispose();
			this.dateTime = null;
			App.utils.data.cleanupDynamicObject(this.settings);
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