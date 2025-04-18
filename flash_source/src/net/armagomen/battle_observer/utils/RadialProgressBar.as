package net.armagomen.battle_observer.utils
{
	import flash.display.Shape;
	import flash.display.Sprite;
	
	public class RadialProgressBar extends Shape
	{
		private var _radius:Number    = 50;
		private var _color:uint       = 0xffa500;
		private var _thickness:Number = 5.0;
		
		public function RadialProgressBar(container:Sprite)
		{
			super();
			container.addChild(this);
		}
		
		public function updateProgressBar(_progress:Number = 1.0):void
		{
			this.graphics.clear();
			if (!_progress)
			{
				return;
			}
			this.graphics.lineStyle(this._thickness, 0, 0.25);
			this.graphics.drawCircle(0, 0, _radius);
			this.graphics.moveTo(0, -this._radius);
			this.graphics.lineStyle(this._thickness, this._color, 0.8);
			for (var i:Number = 0; i <= _progress * 360; i++)
			{
				var radians:Number = (i - 90) * (Math.PI / 180);
				this.graphics.lineTo(Math.cos(radians) * this._radius, Math.sin(radians) * this._radius);
			}
		}
		
		public function setParams(x:Number, y:Number, radius:Number, scale:Number, color:uint):void
		{
			this.x = x;
			this.y = y;
			this._radius = radius;
			this._color = color;
			this._thickness = Math.floor(5.0 * scale);
		}
	}
}