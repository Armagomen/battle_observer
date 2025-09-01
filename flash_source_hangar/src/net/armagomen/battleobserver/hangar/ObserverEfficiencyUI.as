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
		public var getSettings:Function;
		public var getData:Function;
		
		public function ObserverEfficiencyUI()
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
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			this.as_onSettingsChanged(this.getSettings());
		}
		
		public function as_clearScene():void
		{
			this.removeChildren();
			this.text = null;
		}
		
		public function as_onSettingsChanged(settings:Object):void
		{
			this.as_clearScene();
			if (settings.enabled)
			{
				this.scaleX = this.scaleY = App.appHeight / 1080;
				this.x = App.appWidth >> 1;
				this.y = Math.ceil(App.appHeight / 5.5);
				this.text = new TextExt(0, 0, Filters.mediumText, TextFieldAutoSize.CENTER, this);
				this.text.htmlText = this.getData();
			}
			App.utils.data.cleanupDynamicObject(settings);
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
			this.scaleX = this.scaleY = App.appHeight / 1080;
			this.x = App.appWidth >> 1;
			this.y = Math.ceil(App.appHeight / 5.5);
			
		}
		
		public function as_setVisible(vis:Boolean):void
		{
			this.visible = vis;
		}
	}
}