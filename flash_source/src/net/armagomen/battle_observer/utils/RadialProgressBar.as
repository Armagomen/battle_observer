package net.armagomen.battle_observer.utils
{
	import flash.display.Graphics;
	import flash.display.Shape;
	import flash.display.Sprite;
	import flash.text.TextField;
	import flash.text.TextFormat;
	
	public class RadialProgressBar extends Sprite
	{
		private var progressBar:Shape;
		private var progressText:TextField;
		private var radius:Number = 50;
		
		public function RadialProgressBar()
		{
			progressBar = new Shape();
			addChild(progressBar);
			
			progressText = new TextField();
			progressText.defaultTextFormat = new TextFormat("Arial", 24, 0xFFFFFF, true);
			progressText.width = 100;
			progressText.height = 30;
			progressText.x = -50;
			progressText.y = -15;
			progressText.selectable = false;
			progressText.mouseEnabled = false;
			addChild(progressText);
		}
		
		public function updateProgressBar(_progress:Number = 1.0):void
		{
			var g:Graphics    = progressBar.graphics;
			g.clear();
			g.moveTo(0, -radius);
			g.lineStyle(5.0, 0xffa500, 0.8);
			for (var i:Number = 0; i <= _progress * 360; i++)
			{
				var radians:Number = (i - 90) * (Math.PI / 180);
				g.lineTo(Math.cos(radians) * radius, Math.sin(radians) * radius);
			}
		}
		
		public function setPosition(x:Number, y:Number, radius:Number):void
		{
			this.x = x;
			this.y = y;
			this.radius = radius;
		}
	}
}