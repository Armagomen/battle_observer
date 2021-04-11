package net.armagomen.battleobserver.utils
{
	
	import flash.display.*;
	import flash.text.*;
	import flash.geom.ColorTransform;
	import net.armagomen.battleobserver.data.Constants;
	import fl.transitions.Tween;
	
	/**
	 * ...
	 * @author Armagomen
	 */
	public class ProgressBar extends Sprite
	{
		private var bar:Shape           = new Shape();
		private var backGround:Shape    = new Shape();
		private var outline:Shape       = new Shape();
		private var uiText:TextExt      = null;
		private var animation:Tween     = null;
		private var WIDTH:Number        = 0;
		private var HEIGHT:Number       = 0;
		private var COLOR:uint          = 0;
		private var costumColor:Boolean = false;
		private var animationEnabled:Boolean = false;
		private var animationTime:Number = 1.0;
		
		public function ProgressBar(animate:Boolean, x:Number, y:Number, width:Number, height:Number, alpha:Number,
									bgAlpha:Number, filters:Array, color:String, bgColor:String = "#000000", barName:String = "bar", time:Number = 1.0)
		{
			super();
			if (bgColor == null){
				bgColor = "#000000";
			}
			if (barName == null){
				barName = "bar";
			}
			
			this.animationEnabled = animate;
			this.animationTime = time;
			this.x = x;
			this.y = y;
			this.name = barName;
			this.WIDTH = width;
			this.HEIGHT = height;
			this.COLOR = Utils.colorConvert(color);
			if (bgAlpha > 0){
				this.backGround.graphics.beginFill(Utils.colorConvert(bgColor), bgAlpha);
				this.backGround.graphics.drawRect(0, 0, this.WIDTH, this.HEIGHT);
				this.backGround.graphics.endFill();
				this.addChild(backGround);
			}
			this.bar.name = barName;
			this.bar.graphics.beginFill(this.COLOR, alpha);
			this.bar.graphics.drawRect(0, 0, this.WIDTH, this.HEIGHT);
			this.bar.graphics.endFill();
			if (filters != null)
			{
				bar.filters = filters;
			}
			
			this.addChild(bar);
			if (this.animationEnabled)
			{
				this.animation = new Tween(this.bar, "scaleX", null, this.bar.scaleX, 1.0, animationTime, true);
				this.animation.FPS = 30;
			}
		}
		
		public function setNewScale(newScale:Number):void
		{
			if (this.bar.scaleX != newScale)
			{
				if (this.visible && this.animationEnabled)
				{
					this.animation.continueTo(newScale, animationTime);
				}
				else
				{
					this.bar.scaleX = newScale;
				}
			}
		}
		
		public function setText(text:String):void
		{
			this.uiText.htmlText = text;
		}
		
		public function addTextField(x:Number, y:Number, align:String, format:TextFormat, shdowSettings:Object):void
		{
			this.uiText = new TextExt("text", x, y, format, align, shdowSettings, this);
		}
		
		public function setOutline(customColor:Boolean = false, color:String = "#000000", alpha:Number = 1.0):void
		{
			this.costumColor = customColor;
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
		
		public function updateColor(hpColor:String):void
		{
			Utils.updateColor(this.bar, hpColor);
			if (!this.costumColor)
			{
				Utils.updateColor(this.outline, hpColor);
			}
		}
	}
}