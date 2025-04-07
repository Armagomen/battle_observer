package net.armagomen.battle_observer.utils
{
	import flash.display.Shape;
	
	public class RadialProgressBar extends Shape
	{
		private var _radius:Number = 50;
		
		public function RadialProgressBar()
		{
			super();
		}
		
		public function updateProgressBar(_progress:Number = 1.0):void
		{
			this.graphics.clear();
			this.graphics.moveTo(0, -_radius);
			this.graphics.lineStyle(5.0, 0xffa500, 0.8);
			for (var i:Number = 0; i <= _progress * 360; i++)
			{
				var radians:Number = (i - 90) * (Math.PI / 180);
				this.graphics.lineTo(Math.cos(radians) * _radius, Math.sin(radians) * _radius);
			}
		}
		
		public function setPosition(x:Number, y:Number, radius:Number):void
		{
			this.x = x;
			this.y = y;
			this._radius = radius;
		}
	}
}