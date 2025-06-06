﻿package net.armagomen.battle_observer.utils
{
	
	import flash.display.*;
	import flash.text.*;
	import net.armagomen.battle_observer.utils.tween.Tween;
	
	/**
	 * ...
	 * @author Armagomen
	 */
	public class ProgressBar extends Sprite
	{
		private var bar:Shape            = new Shape();
		private var outline:Shape        = new Shape();
		private var uiText:TextExt       = null;
		private var animation:Tween      = null;
		private var barColor:uint        = 0;
		private var animationTime:Number = 1.0;
		
		public function ProgressBar(x:Number, y:Number, width:Number, height:Number, color:String, bgColor:String = "#000000", time:Number = 1.0)
		{
			super();
			if (bgColor == null)
			{
				bgColor = "#000000";
			}
			this.animationTime = time;
			this.x = x;
			this.y = y;
			this.barColor = Utils.colorConvert(color);
			this.graphics.beginFill(Utils.colorConvert(bgColor), Constants.BG_ALPHA);
			this.graphics.drawRect(0, 0, width, height);
			this.graphics.endFill();
			this.bar.graphics.beginFill(this.barColor, Constants.ALPHA);
			this.bar.graphics.drawRect(0, 0, width, height);
			this.bar.graphics.endFill();
			this.addChild(this.bar);
			if (this.animationTime > 0)
			{
				this.animation = new Tween(this.bar, "scaleX", 1.0, 0, this.animationTime);
			}
		}
		
		public function setNewScale(newScale:Number):void
		{
			var scale:Number = Math.max(0, newScale);
			if (this.animationTime > 0 && this.visible)
			{
				this.animation.continueTo(scale, this.animationTime);
			}
			else
			{
				this.bar.scaleX = scale;
			}
		}
		
		public function setText(text:String):void
		{
			this.uiText.htmlText = text;
		}
		
		public function addTextField(x:Number, y:Number, align:String, format:TextFormat):void
		{
			this.uiText = new TextExt(x, y, format, align, this);
		}
		
		public function setOutline(width:Number = 0, height:Number = 0):void
		{
			
			this.outline.graphics.lineStyle(1, this.barColor, Constants.ALPHA, true, LineScaleMode.NONE);
			this.outline.graphics.drawRect(-1, -1, width + 1, height + 1);
			this.addChild(this.outline);
		}
		
		public function setVisible(vis:Boolean):void
		{
			var active:Boolean = vis && this.bar.scaleX > 0;
			if (this.visible != active)
			{
				this.visible = active;
			}
		}
		
		public function updateColor(color:String):void
		{
			Utils.updateColor(this.bar, color);
			if (this.outline)
			{
				Utils.updateColor(this.outline, color);
			}
		}

		public function remove():void
		{
			this.removeChildren();
			this.bar = null;
			this.outline = null;
			this.uiText = null;
			if (this.animation)
			{
				this.animation.stop();
				this.animation = null;
			}
		}
	}
}