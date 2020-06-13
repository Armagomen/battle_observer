package net.armagomen.battleobserver.battle.components.sixthsense
{
	import flash.display.*;
	import flash.events.*;
	import flash.net.URLRequest;
	import flash.text.*;
	import flash.text.TextField;
	import net.armagomen.battleobserver.battle.utils.Filters;
	import net.armagomen.battleobserver.battle.utils.TextExt;
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
			this.removeEventListener(Event.RESIZE, this._onResizeHandle);
			super.onDispose();
		}

		public function as_clearScene():void
		{
			while (this.numChildren > 0){
				this.removeChildAt(0);
			}
			if (this.params)
			{
				App.utils.data.cleanupDynamicObject(this.params);
				this.params = null;
			}
			this.timer = null;
			this.image = null;
			this._container = null;
			var page:* = parent;
			page.unregisterComponent(this.name);
		}

		public function as_sixthSense(show:Boolean, str:String):void
		{
			if (params.enabled)
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
				if (params.showTimer)
				{
					timer.htmlText = str;
				}
				if (this._container.visible != show)
				{
					this._container.visible = show;
				}
			}
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
			if (params.enabled)
			{
				var loader:Loader = new Loader();
				loader.contentLoaderInfo.addEventListener(Event.COMPLETE, imageLoaded);
				loader.load(new URLRequest('../../../'+params.image.img));
			}
		}

		private function _onResizeHandle(event:Event):void
		{
			this.x = App.appWidth >> 1;
		}
	}
}