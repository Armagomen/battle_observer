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
		public var getSettings:Function;
		
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
		
		override protected function onPopulate():void 
		{
			super.onPopulate();
			this.as_onSettingsChanged(this.getSettings());
		}
		
		public function as_clearScene():void
		{
			while (this.numChildren > 0)
			{
				this.removeChildAt(0);
			}
			this.dateTime = null;
		}
		
		public function as_onSettingsChanged(settings:Object):void
		{
			this.as_clearScene();
			if (settings.enabled && settings.hangar.enabled){
				this.x = settings.hangar.x < 0 ? parent.width + settings.hangar.x : settings.hangar.x
				this.y = settings.hangar.y < 0 ? parent.height + settings.hangar.y : settings.hangar.y
				this.dateTime = new TextExt(0, 0, Filters.largeText, TextFieldAutoSize.LEFT, this);
			}
			App.utils.data.cleanupDynamicObject(settings);
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
			var settings:Object = this.getSettings().hangar;
			this.x = settings.x < 0 ? parent.width + settings.x : settings.x
			this.y = settings.y < 0 ? parent.height + settings.y : settings.y
			App.utils.data.cleanupDynamicObject(settings);
		}
	}

}