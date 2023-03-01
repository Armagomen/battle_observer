package net.armagomen.battleobserver.battle.components.debugpanel
{
	import flash.display.Bitmap;
	import flash.display.Sprite;
	import flash.text.TextFieldAutoSize;
	import mx.utils.StringUtil;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class modern extends Sprite
	{
		[Embed(source = "ping_img/1.png")]
		private var one:Class;
		[Embed(source = "ping_img/2.png")]
		private var two:Class;
		[Embed(source = "ping_img/3.png")]
		private var three:Class;
		[Embed(source = "ping_img/4.png")]
		private var four:Class;
		[Embed(source = "ping_img/5.png")]
		private var five:Class;
		[Embed(source = "ping_img/6.png")]
		private var sixth:Class;
		[Embed(source = "ping_img/7.png")]
		private var seven:Class;
		[Embed(source = "ping_img/8.png")]
		private var eight:Class;
		[Embed(source = "ping_img/9.png")]
		private var nine:Class;
		[Embed(source = "ping_img/10.png")]
		private var ten:Class;
		
		private var debugText:TextExt      = null;
		private const template:String      = "<textformat tabstops='[76, 160]'>FPS: <font color='{0}'>{1}</font><tab>PING: <font color='{2}'>{3}</font><tab><font color='{4}'>LAG</font></textformat>";
		
		private var fpsColor:String        = "#B3FE95";
		private var pingColor:String       = "#B3FE95";
		private var lagColor:String        = "#FD9675";
		private var icons:Vector.<Bitmap>  = null;
		private var lastVisibleIcon:Bitmap = null;
		
		public function modern(shadow_settings:Object, colors:Object)
		{
			super();
			this.debugText = new TextExt(20, 0, Filters.middleText, TextFieldAutoSize.LEFT, shadow_settings, this);
			this.fpsColor = colors.fpsColor;
			this.pingColor = colors.pingColor;
			this.lagColor = colors.pingLagColor;
			this.createBitmapVector();
		}
		
		private function createBitmapVector():void
		{
			this.icons = new Vector.<Bitmap>(10, true);
			
			var icon1:Bitmap = new one();
			this.icons[0] = icon1;
			
			var icon2:Bitmap = new two();
			this.icons[1] = icon2;
			
			var icon3:Bitmap = new three();
			this.icons[2] = icon3;
			
			var icon4:Bitmap = new four();
			this.icons[3] = icon4;
			
			var icon5:Bitmap = new five();
			this.icons[4] = icon5;
			
			var icon6:Bitmap = new sixth();
			this.icons[5] = icon6;
			
			var icon7:Bitmap = new seven();
			this.icons[6] = icon7;
			
			var icon8:Bitmap = new eight();
			this.icons[7] = icon8;
			
			var icon9:Bitmap = new nine();
			this.icons[8] = icon9;
			
			var icon10:Bitmap = new ten();
			this.icons[9] = icon10;
			
			for each (var icon:Bitmap in this.icons)
			{
				icon.visible = false;
				icon.x = 15;
				icon.y = 25;
				icon.width = 210;
				icon.height = 7;
				icon.smoothing = true;
				this.addChild(icon);
			}
		}
		
		public function update(ping:int, fps:int, lag:Boolean):void
		{
			this.debugText.htmlText = StringUtil.substitute(this.template, this.fpsColor, fps, this.pingColor, ping, lag ? this.lagColor : this.pingColor);
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
			else if (ping < 60)
			{
				icon = this.icons[6];
			}
			else if (ping < 80)
			{
				icon = this.icons[5];
			}
			else if (ping < 100)
			{
				icon = this.icons[4];
			}
			else if (ping < 200)
			{
				icon = this.icons[3];
			}
			else if (ping < 400)
			{
				icon = this.icons[2];
			}
			else if (ping < 800)
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