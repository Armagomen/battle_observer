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
		
		private function updateProgressBar(_progress:Number = 1.0):void
		{
			var radius:Number = 50;
			var g:Graphics    = progressBar.graphics;
			g.clear();
			g.beginFill(0xFF0000);
			g.moveTo(0, 0);
			g.lineTo(radius, 0);
			g.lineStyle(3.0);
			for (var i:Number = 0; i <= _progress * 360; i++)
			{
				var radians:Number = (i - 90) * (Math.PI / 180);
				g.lineTo(Math.cos(radians) * radius, Math.sin(radians) * radius);
			}
			g.lineTo(0, 0);
			g.endFill();
			
			progressText.text = Math.round(_progress * 100) + "%";
		}
	}
}