package net.armagomen.battleobserver.hangar
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.hangar.utils.TextExt;
	import net.armagomen.battleobserver.hangar.utils.Filters;
	import net.wg.infrastructure.base.BaseDAAPIComponent;
	
	public class ObserverEfficiencyUI extends BaseDAAPIComponent
	{
		private var text:TextExt;
		
		public function ObserverEfficiencyUI()
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
		
		public function as_clearScene():void
		{
			this.removeChildren();
			this.text = null;
		}
		
		public function as_addToStage():void
		{
			var scale:Number = Math.min(App.appHeight / 1080, 1.0);
			this.scaleX = this.scaleY = scale;
			this.x = App.appWidth >> 1;
			this.y = Math.ceil(App.appHeight / 5.5);
			this.text = new TextExt(0, 0, Filters.mediumText, TextFieldAutoSize.CENTER, this);
		}
		
		public function as_updateValue(value:String):void
		{
			if (this.text)
			{
				this.text.htmlText = value;
			}
		}
		
		private function _onResizeHandle(event:Event):void
		{
			var scale:Number = Math.min(App.appHeight / 1080, 1.0);
			this.scaleX = this.scaleY = scale;
			this.x = App.appWidth >> 1;
			this.y = Math.ceil(App.appHeight / 5.5);
		}
	}
}