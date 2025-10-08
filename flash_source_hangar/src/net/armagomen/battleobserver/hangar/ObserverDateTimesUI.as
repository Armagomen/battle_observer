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
			this.visible = false;
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
			var scale_x:Number = Math.min(App.appWidth / 1920, 1.0);
			var scale_y:Number = Math.min(App.appHeight / 1080, 1.0);
			this.scaleX = this.scaleY = Math.min(scale_x, scale_y);
			this.x = Math.ceil(50 * scale_x);
			this.y = Math.ceil(80 * scale_y);
			this.dateTime = new TextExt(0, 0, Filters.largeText, TextFieldAutoSize.LEFT, this);
			this.dateTime.alpha = 0.8;
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
			var scale_x:Number = Math.min(App.appWidth / 1920, 1.0);
			var scale_y:Number = Math.min(App.appHeight / 1080, 1.0);
			this.scaleX = this.scaleY = Math.min(scale_x, scale_y);
			this.x = Math.ceil(50 * scale_x);
			this.y = Math.ceil(80 * scale_y);
		}
	}
}