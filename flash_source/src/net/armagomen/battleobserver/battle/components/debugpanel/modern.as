package net.armagomen.battleobserver.battle.components.debugpanel
{
	import flash.display.Bitmap;
	import flash.display.Sprite;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.utils.Utils;
	
	public class modern extends Sprite
	{
		[Embed(source = "ping_img/1.png")]
		private var _1:Class;
		[Embed(source = "ping_img/2.png")]
		private var _2:Class;
		[Embed(source = "ping_img/3.png")]
		private var _3:Class;
		[Embed(source = "ping_img/4.png")]
		private var _4:Class;
		[Embed(source = "ping_img/5.png")]
		private var _5:Class;
		[Embed(source = "ping_img/6.png")]
		private var _6:Class;
		[Embed(source = "ping_img/7.png")]
		private var _7:Class;
		[Embed(source = "ping_img/8.png")]
		private var _8:Class;
		[Embed(source = "ping_img/9.png")]
		private var _9:Class;
		[Embed(source = "ping_img/10.png")]
		private var _10:Class;
		
		private var FPS:TextExt            = null;
		private var PING:TextExt           = null;
		private var LAG:TextExt            = null;
		private var PATTERN:TextExt        = null;
		
		private var pingColor:uint         = Utils.colorConvert("#B3FE95");
		private var lagColor:uint          = Utils.colorConvert("#FD9675");
		private var icons:Vector.<Bitmap>  = null;
		private var lastVisibleIcon:Bitmap = null;
		
		public function modern(colors:Object)
		{
			super();
			this.LAG = new TextExt(185, 0, Filters.middleText, TextFieldAutoSize.LEFT, this);
			this.LAG.text = "LAG";
			this.PATTERN = new TextExt(20, 0, Filters.middleText, TextFieldAutoSize.LEFT, this);
			this.PATTERN.htmlText = "<textformat tabstops='[78]'>FPS:\tPING:</textformat>";
			
			this.FPS = new TextExt(58, 0, Filters.middleText, TextFieldAutoSize.LEFT, this);
			this.PING = new TextExt(144, 0, Filters.middleText, TextFieldAutoSize.LEFT, this);
			
			this.pingColor = Utils.colorConvert(colors.pingColor);
			this.lagColor = Utils.colorConvert(colors.pingLagColor);
			
			this.FPS.textColor = Utils.colorConvert(colors.fpsColor);
			this.PING.textColor = this.pingColor;
			this.LAG.textColor = this.pingColor;
			
			this.createBitmapVector();
		}
		
		private function createBitmapVector():void
		{
			this.icons = new <Bitmap>[new _1(), new _2(), new _3(), new _4(), new _5(), new _6(), new _7(), new _8(), new _9(), new _10()];
			this.icons.fixed = true;
			
			for each (var icon:Bitmap in this.icons)
			{
				icon.visible = false;
				icon.x = 15;
				icon.y = 25;
				icon.width = 210;
				icon.height = 7;
				icon.alpha = 0.75;
				this.addChild(icon);
			}
		}
		
		public function update(ping:int, fps:int, lag:Boolean):void
		{
			this.FPS.text = fps.toString();
			this.PING.text = ping.toString();
			var color:uint = lag ? this.lagColor : this.pingColor;
			if (this.LAG.textColor != color)
			{
				this.LAG.textColor = color;
			}
			var icon:Bitmap = null;
			if (ping < 15)
			{
				icon = this.icons[9];
			}
			else if (ping < 30)
			{
				icon = this.icons[8];
			}
			else if (ping < 40)
			{
				icon = this.icons[7];
			}
			else if (ping < 50)
			{
				icon = this.icons[6];
			}
			else if (ping < 60)
			{
				icon = this.icons[5];
			}
			else if (ping < 70)
			{
				icon = this.icons[4];
			}
			else if (ping < 100)
			{
				icon = this.icons[3];
			}
			else if (ping < 200)
			{
				icon = this.icons[2];
			}
			else if (ping < 300)
			{
				icon = this.icons[1];
			}
			else
			{
				icon = this.icons[0];
			}
			
			if (this.lastVisibleIcon !== icon)
			{
				if (this.lastVisibleIcon)
				{
					this.lastVisibleIcon.visible = false;
				}
				icon.visible = true;
				this.lastVisibleIcon = icon;
			}
		}
	}
}