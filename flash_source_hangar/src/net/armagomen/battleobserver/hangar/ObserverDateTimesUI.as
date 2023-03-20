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
		private var config:Object;
		
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
		
		public function as_clearScene():void
		{
			while (this.numChildren > 0)
			{
				this.removeChildAt(0);
			}
			this.dateTime = null;
			App.utils.data.cleanupDynamicObject(this.config);
		}
		
		public function as_startUpdate(settings:Object):void
		{
			this.as_clearScene();
			if (settings.enabled){
				this.config = settings;
				this.x = settings.x < 0 ? parent.width + settings.x : settings.x
				this.y = settings.y < 0 ? parent.height + settings.y : settings.y
				this.dateTime = new TextExt("time", 0, 0, Filters.largeText, TextFieldAutoSize.LEFT, this);
			}
		}
		
		public function as_setDateTime(text:String):void
		{
			if (this.dateTime)
			{
				this.dateTime.htmlText = text;
			}
		}
		
		public function _onResizeHandle(event:Event):void
		{
			this.x = this.config.x < 0 ? parent.width + this.config.x : this.config.x
			this.y = this.config.y < 0 ? parent.height + this.config.y : this.config.y
		}
	}

}