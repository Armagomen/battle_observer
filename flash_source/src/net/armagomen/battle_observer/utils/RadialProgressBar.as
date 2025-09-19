package net.armagomen.battle_observer.utils
{
	import flash.display.Sprite;
	import flash.display.Shape;
	import flash.filters.GlowFilter;
	
	public class RadialProgressBar extends Sprite
	{
		
		private var _radius:Number    = 50;
		private var _color:uint       = 0xffa500;
		private var _thickness:Number = 4.0;
		
		private var baseCircle:Shape  = new Shape();
		private var progressArc:Shape = new Shape();
		
		public function RadialProgressBar(container:Sprite)
		{
			super();
			container.addChild(this);
			this.addChild(this.baseCircle);
			this.addChild(this.progressArc);
			this.baseCircle.cacheAsBitmap = true;
			this.progressArc.cacheAsBitmap = true;
		}
		
		private function createBaseCircle():void
		{
			this.baseCircle.graphics.lineStyle(this._thickness, 0, 0.25);
			this.baseCircle.graphics.drawCircle(0, 0, this._radius);
			this.baseCircle.visible = false;
		}
		
		public function updateProgressBar(_progress:Number = 1.0):void
		{
			this.progressArc.graphics.clear();
			
			if (!_progress)
			{
				this.baseCircle.visible = false;
				return;
			}
			this.baseCircle.visible = true;
			this.progressArc.graphics.lineStyle(this._thickness, this._color);
			this.progressArc.graphics.moveTo(0, -this._radius);
			for (var i:Number = 0; i <= _progress * 360; i++)
			{
				var radians:Number = (i - 90) * (Math.PI / 180);
				this.progressArc.graphics.lineTo(Math.cos(radians) * this._radius, Math.sin(radians) * this._radius);
			}
		}
		
		public function setParams(x:Number, y:Number, radius:Number, scale:Number, color:uint):void
		{
			this.x = x;
			this.y = y;
			this._radius = radius;
			this._color = color;
			this._thickness = Math.floor(4.0 * scale);
			this.baseCircle.filters = [new GlowFilter(0, 1.0, 8, 8, 2, 1)];
			this.progressArc.filters = [new GlowFilter(this._color, 1.0, 8, 8, 2, 1)];
			this.createBaseCircle();
		}
	}
}