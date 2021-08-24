package net.armagomen.battleobserver.battle.components.sixthsense
{
	import flash.display.*;
	import flash.events.Event;
	import flash.net.URLRequest;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.utils.tween.Tween;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.views.BaseBattlePage;
	
	public class SixthSenseUI extends ObserverBattleDispalaysble
	{
		private var params:Object     = null;
		private var timer:TextExt;
		private var image:Bitmap      = null;
		private var _container:Sprite = null;
		private var animate:Boolean   = false;
		private var animation:Tween   = null;
		
		public function SixthSenseUI()
		{
			super();
			this.x = App.appWidth >> 1;
			this._container = new Sprite()
			this._container.name = "image";
			this._container.visible = false;
			this.addChild(_container);
		}
		
		override protected function onPopulate():void 
		{
			super.onPopulate();
			if (this.image == null)
			{
				this.animate = this.animationEnabled();
				this.params = this.getSettings();
				this.setImage();
			}
		}
		
		private function addLoadedImageAndTimer():void
		{
			this.image.smoothing = params.image.smoothing;
			this.image.alpha = params.image.alpha;
			this.image.scaleX = this.image.scaleY = params.image.scale;
			this.image.x = params.image.x - image.width * 0.5;
			this.image.y = params.image.y;
			this._container.addChild(this.image);
			if (params.showTimer)
			{
				this.timer = new TextExt(params.timer.x, params.timer.y, Filters.largeText, TextFieldAutoSize.CENTER, getShadowSettings(), this._container);
				if (this.animate)
				{
					this.animation = new Tween(this.timer, "alpha", 1.0, 0, 1, true);
				}
				else
				{
					this.timer.alpha = params.timer.alpha;
				}
			}
		}
		
		public function as_show():void
		{
			if (!this.image)
			{
				[Embed(source = "SixthSenseIcon.png")]
				var Icon:Class;
				this.image = new Icon();
				this.addLoadedImageAndTimer();
			}
			this._container.visible = true;
		}
		
		public function as_hide():void
		{
			this._container.visible = false;
		}
		
		public function as_updateTimer(str:String):void
		{
			if (this.animate)
			{
				this.animation.start();
			}
			this.timer.htmlText = str;
		}
		
		private function imageLoaded(evt:Event):void
		{
			var loaderInfo:LoaderInfo = evt.target as LoaderInfo;
			if (loaderInfo.hasEventListener(Event.COMPLETE))
			{
				loaderInfo.removeEventListener(Event.COMPLETE, imageLoaded);
			}
			this.image = loaderInfo.content as Bitmap;
			this.addLoadedImageAndTimer();
		}
		
		private function setImage():void
		{
			var loader:Loader = new Loader();
			loader.contentLoaderInfo.addEventListener(Event.COMPLETE, imageLoaded);
			loader.load(new URLRequest('../../../' + params.image.img));
		}
		
		override public function onResizeHandle(event:Event):void
		{
			this.x = App.appWidth >> 1;
		}
	}
}