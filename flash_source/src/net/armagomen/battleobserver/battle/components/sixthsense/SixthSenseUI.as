package net.armagomen.battleobserver.battle.components.sixthsense
{
	import flash.display.*;
	import flash.events.*;
	import flash.net.URLRequest;
	import flash.text.*;
	import flash.text.TextField;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.gui.battle.components.*;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;

	public class SixthSenseUI extends BattleDisplayable
	{
		private var params:Object = null;
		private var timer:TextField;
		private var image:Bitmap = null;
		private var _container:Sprite = null;
		public var getShadowSettings:Function;

		public function SixthSenseUI(compName:String)
		{
			super();
			this.name = compName;
			this.x = App.appWidth >> 1;
		}

		public function as_startUpdate(settings:Object):void
		{
			var battlePage: * = parent;
			if (battlePage._componentsStorage.hasOwnProperty(BATTLE_VIEW_ALIASES.SIXTH_SENSE)) {
				var sixthSense: * = battlePage.getComponent(BATTLE_VIEW_ALIASES.SIXTH_SENSE);
				if (sixthSense) {
					battlePage.removeChild(sixthSense);
				}
			}
			params = App.utils.data.cloneObject(settings);
			this.setImage();
			App.utils.data.cleanupDynamicObject(settings);
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

		override protected function onPopulate():void
		{
			super.onPopulate();
			this._container = new Sprite()
			this._container.name = "image";
			this._container.visible = false;
			this.addChild(_container);
		}

		override protected function onDispose():void
		{
			this._container = null;
			this.removeEventListener(Event.RESIZE, this._onResizeHandle);
			super.onDispose();
		}

		public function as_show():void
		{
			if (!this.image)
			{
				[Embed(source = "SixthSenseIcon.png")]
				var Icon:Class;
				this.image = new Icon();
				this.image.smoothing = params.image.smoothing;
				this.image.alpha = params.image.alpha;
				this.image.scaleX = this.image.scaleY = params.image.scale;
				this.image.x = params.image.x - image.width >> 1;
				this.image.y = params.image.y;
				this._container.addChild(this.image);
				if (params.showTimer)
				{
					timer = new TextExt("timer", params.timer.x, params.timer.y, Filters.largeText, TextFieldAutoSize.CENTER, getShadowSettings(), this._container);
					timer.alpha = params.timer.alpha;
				}
			}
			this._container.visible = true;
		}
		
		public function as_hide():void
		{
			this._container.visible = false;
		}
		
		public function as_updateTimer(str:String):void
		{
			timer.htmlText = str;
		}

		private function imageLoaded(evt:Event):void
		{
			var loaderInfo:LoaderInfo = evt.target as LoaderInfo;
			if (loaderInfo.hasEventListener(Event.COMPLETE))
			{
				loaderInfo.removeEventListener(Event.COMPLETE, imageLoaded);
			}
			this.image = loaderInfo.content as Bitmap;
			this.image.smoothing = params.image.smoothing;
			this.image.alpha = params.image.alpha;
			this.image.scaleX = this.image.scaleY = params.image.scale;
			this.image.x = params.image.x - image.width >> 1;
			this.image.y = params.image.y;
			this._container.addChild(this.image);
			if (params.showTimer)
			{
				timer = new TextExt("timer", params.timer.x, params.timer.y, Filters.largeText, TextFieldAutoSize.CENTER, getShadowSettings(), this._container);
				timer.alpha = params.timer.alpha;
			}
		}

		private function setImage():void
		{
			var loader:Loader = new Loader();
			loader.contentLoaderInfo.addEventListener(Event.COMPLETE, imageLoaded);
			loader.load(new URLRequest('../../../'+params.image.img));
		}

		private function _onResizeHandle(event:Event):void
		{
			this.x = App.appWidth >> 1;
		}
	}
}