package net.armagomen.battleobserver.battle.utils
{

	import flash.display.*;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.data.Constants;
	import fl.transitions.Tween;
	
	/**
	 * ...
	 * @author Armagomen
	 */
	public class ProgressBar extends Sprite
	{
		public var bar:Shape = new Shape();
		public var uiText:TextExt = null;
		private var animation:Tween = null;
		private var WIDTH:Number = 0;
		private var HEIGHT:Number = 0;
		private var COLOR:uint = 0;

		public function ProgressBar(x:Number, y:Number, width:Number, height:Number, alpha:Number, bgAlpha:Number, filters:Array, 
									color:String, bgColor:String="#000000", barName:String="bar")
		{
			super();
			var backGround:Shape = new Shape();
			this.x = x;
			this.y = y;
			this.name = barName;
			this.WIDTH = width;
			this.HEIGHT = height;
			this.COLOR = Utils.colorConvert(color);
			backGround.graphics.beginFill(Utils.colorConvert(bgColor), bgAlpha);
			backGround.graphics.drawRect(0, 0, this.WIDTH, this.HEIGHT);
			backGround.graphics.endFill();
			bar.name = barName;
			bar.graphics.beginFill(this.COLOR, alpha);
			bar.graphics.drawRect(0, 0, this.WIDTH, this.HEIGHT);
			bar.graphics.endFill();
			if (filters != null)
			{
				bar.filters = filters;
			}
			this.addChild(backGround);
			this.addChild(bar);
			this.animation = new Tween(this.bar, "scaleX", null, this.bar.scaleX, 1.0, 1, true);
			this.animation.FPS = 30;

		}

		public function animateBar(newScale:Number):void
		{
			this.animation.continueTo(newScale, 1);
		}
		
		public function stopAndClearAnimate():void{
			if (this.animation.isPlaying){
				this.animation.stop();
				this.animation = null;
			}
		}

		public function addTextField(x:Number, y:Number, align:String, format:TextFormat, shdowSettings:Object):void
		{
			uiText = new TextExt("text", x, y, format, align, shdowSettings, this);
		}

		public function setOutline(customColor:Boolean=false, color:String="#000000", alpha:Number=1.0):void
		{
			var outline:Shape = new Shape();
			outline.graphics.lineStyle(1, customColor ? Utils.colorConvert(color) : this.COLOR, Math.max(0.05, alpha), true, LineScaleMode.NONE);
			outline.graphics.drawRect(0, 0, this.WIDTH, this.HEIGHT);
			this.addChild(outline);
		}

		public function setVisible(vis:Boolean):void
		{
			if (this.visible != vis)
			{
				this.visible = vis;
			}
		}
	}
}