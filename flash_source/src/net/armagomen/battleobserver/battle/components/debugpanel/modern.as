package net.armagomen.battleobserver.battle.components.debugpanel
{
	import flash.display.Bitmap;
	import flash.display.Sprite;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.utils.Utils;
	import net.armagomen.battleobserver.battle.interfaces.IDebugPanel;
	
	public class Modern extends Sprite implements IDebugPanel
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
		
		private var fps:TextExt            = null;
		private var ping:TextExt           = null;
		private var lag:TextExt            = null;
		private var statical:TextExt       = null;
		
		private var pingColor:uint         = Utils.colorConvert("#B3FE95");
		private var lagColor:uint          = Utils.colorConvert("#FD9675");
		private var icons:Vector.<Bitmap>  = null;
		private var lastVisibleIcon:Bitmap = null;
		
		public function Modern(settings:Object)
		{
			super();
			this.lag = new TextExt(185, 0, Filters.middleText, TextFieldAutoSize.LEFT, this);
			this.lag.text = "LAG";
			this.statical = new TextExt(20, 0, Filters.middleText, TextFieldAutoSize.LEFT, this);
			this.statical.htmlText = "<textformat tabstops='[78]'>FPS:\tPING:</textformat>";
			
			this.fps = new TextExt(58, 0, Filters.middleText, TextFieldAutoSize.LEFT, this);
			this.ping = new TextExt(144, 0, Filters.middleText, TextFieldAutoSize.LEFT, this);
			
			this.pingColor = Utils.colorConvert(settings.pingColor);
			this.lagColor = Utils.colorConvert(settings.pingLagColor);
			
			this.fps.textColor = Utils.colorConvert(settings.fpsColor);
			this.ping.textColor = this.pingColor;
			this.lag.textColor = this.pingColor;
			
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
			this.fps.text = fps.toString();
			this.ping.text = ping.toString();
			var color:uint = lag ? this.lagColor : this.pingColor;
			if (this.lag.textColor != color)
			{
				this.lag.textColor = color;
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