package net.armagomen.battleobserver.hangar
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.hangar.utils.Filters;
	import net.armagomen.battleobserver.hangar.utils.TextExt;
	import net.wg.infrastructure.base.BaseDAAPIComponent;
	
	public class ObserverDateTimesUI extends BaseDAAPIComponent
	{
		private var dateTime:TextExt;
		
		public function ObserverDateTimesUI()
		{
			super();
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
			this.as_clearScene();
			super.onDispose();
		}
		
		public function as_addToStage():void
		{
			this.scaleX = this.scaleY = App.appHeight / 1080;
			this.x = Math.ceil(App.appWidth / 64);
			this.y = Math.ceil(App.appHeight / 16);
			this.dateTime = new TextExt(0, 0, Filters.largeText, TextFieldAutoSize.LEFT, this);
		}
		
		public function as_clearScene():void
		{
			this.removeChildren();
			this.dateTime = null;
		}
		
		public function as_updateTime(text:String):void
		{
			if (this.dateTime)
			{
				this.dateTime.htmlText = text;
			}
		}
		
		public function _onResizeHandle(event:Event):void
		{
			this.scaleX = this.scaleY = App.appHeight / 1080;
			this.x = Math.ceil(App.appWidth / 64);
			this.y = Math.ceil(App.appHeight / 16);
		}
	}
}