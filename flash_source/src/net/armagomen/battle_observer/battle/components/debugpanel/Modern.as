package net.armagomen.battle_observer.battle.components.debugpanel
{
	import flash.display.Bitmap;
	import flash.display.Sprite;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	import net.armagomen.battle_observer.utils.Utils;
	
	public class Modern extends Sprite
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
		
		private var lags:Boolean           = false;
		
		public function Modern(settings:Object, panel:*)
		{
			super();
			this.lag = new TextExt(185, 0, Constants.middleText, TextFieldAutoSize.LEFT, this);
			this.lag.text = "LAG";
			this.statical = new TextExt(20, 0, Constants.middleText, TextFieldAutoSize.LEFT, this);
			this.statical.htmlText = "<textformat tabstops='[78]'>FPS:\tPING:</textformat>";
			
			this.fps = new TextExt(58, 0, Constants.middleText, TextFieldAutoSize.LEFT, this);
			this.ping = new TextExt(144, 0, Constants.middleText, TextFieldAutoSize.LEFT, this);
			
			this.pingColor = Utils.colorConvert(settings.pingColor);
			this.lagColor = Utils.colorConvert(settings.pingLagColor);
			
			this.fps.textColor = Utils.colorConvert(settings.fpsColor);
			this.ping.textColor = this.pingColor;
			this.lag.textColor = this.pingColor;
			
			this.createBitmapVector();
			panel.addChild(this);
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
			
			this.lastVisibleIcon = this.icons[0];
			this.lastVisibleIcon.visible = true;
		}
		
		public function update(_ping:int, _fps:int, _lag:Boolean):void
		{
			this.fps.text = _fps.toString();
			this.ping.text = _ping.toString();
			if (this.lags != _lag)
			{
				this.lags = _lag;
				this.lag.textColor = _lag ? this.lagColor : this.pingColor;
			}
			this.lastVisibleIcon.visible = false;
			if (_ping < 15)
			{
				this.lastVisibleIcon = this.icons[9];
			}
			else if (_ping < 30)
			{
				this.lastVisibleIcon = this.icons[8];
			}
			else if (_ping < 40)
			{
				this.lastVisibleIcon = this.icons[7];
			}
			else if (_ping < 60)
			{
				this.lastVisibleIcon = this.icons[6];
			}
			else if (_ping < 80)
			{
				this.lastVisibleIcon = this.icons[5];
			}
			else if (_ping < 100)
			{
				this.lastVisibleIcon = this.icons[4];
			}
			else if (_ping < 150)
			{
				this.lastVisibleIcon = this.icons[3];
			}
			else if (_ping < 200)
			{
				this.lastVisibleIcon = this.icons[2];
			}
			else if (_ping < 300)
			{
				this.lastVisibleIcon = this.icons[1];
			}
			else
			{
				this.lastVisibleIcon = this.icons[0];
			}
			this.lastVisibleIcon.visible = true;
		}
	}
}