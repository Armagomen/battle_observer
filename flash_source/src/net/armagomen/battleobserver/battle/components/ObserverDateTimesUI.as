﻿package net.armagomen.battleobserver.battle.components
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.utils.Filters;
	import net.armagomen.battleobserver.battle.utils.TextExt;
	import net.wg.gui.battle.components.*;

	public class ObserverDateTimesUI extends BattleDisplayable
	{
		private var dateTime:TextField;
		private var config:Object;
		public var getShadowSettings:Function;

		public function ObserverDateTimesUI(compName:String)
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

		public function as_clearScene():void
		{
			while (this.numChildren > 0){
				this.removeChildAt(0);
			}
			this.dateTime = null;
			var page:* = parent;
			page.unregisterComponent(this.name);
		}

		public function as_startUpdate(settings:Object):void
		{
			this.config = settings;
			var x:int = settings.x;
			if (x < 0){
				x = App.appWidth + x;
			}
			var y:int = settings.y;
			if (y < 0){
				y = App.appHeight + y;
			}
			dateTime = new TextExt("time", x, y, Filters.largeText, TextFieldAutoSize.LEFT, getShadowSettings(), this);
		}

		public function as_setDateTime(text:String):void
		{
			if (dateTime)
			{
				dateTime.htmlText = text;
			}
		}

		public function _onResizeHandle(event:Event):void
		{
			var x:int = config.x;
			if (x < 0){
				x = App.appWidth + x;
			}
			var y:int = config.y;
			if (y < 0){
				y = App.appHeight + y;
			}
			dateTime.x = x;
			dateTime.y = y;
		}
	}

}