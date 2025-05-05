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
		private var statical:TextExt       = null;
		private var icons:Vector.<Bitmap>  = null;
		private var lastVisibleIcon:Bitmap = null;
		private var lag_icons:LagIcons     = new LagIcons()
		
		public function Modern(settings:Object)
		{
			super();
			this.icons = new <Bitmap>[new _10(), new _9(), new _8(), new _7(), new _6(), new _5(), new _4(), new _3(), new _2(), new _1()];
			this.icons.fixed = true;
			this.lag_icons.lag.x = 175;
			this.lag_icons.lag.y = 4;
			this.lag_icons.lag.visible = false;
			this.lag_icons.lag.width = 20;
			this.lag_icons.lag.height = 20;
			this.lag_icons.lag.smoothing = true;
			this.lag_icons.no_lag.x = 175;
			this.lag_icons.no_lag.y = 4;
			this.lag_icons.no_lag.width = 20;
			this.lag_icons.no_lag.height = 20;
			this.lag_icons.no_lag.smoothing = true;
			this.statical = new TextExt(15, 0, Constants.middleText, TextFieldAutoSize.LEFT, this);
			this.statical.htmlText = "<textformat tabstops='[75]'>FPS:\tPING:</textformat>";
			this.fps = new TextExt(53, 0, Constants.middleText, TextFieldAutoSize.LEFT, this);
			this.ping = new TextExt(137, 0, Constants.middleText, TextFieldAutoSize.LEFT, this);
			this.fps.textColor = Utils.colorConvert(settings.fpsColor);
			this.ping.textColor = Utils.colorConvert(settings.pingColor);
			this.updateIconsProperty();
			this.addChild(lag_icons.no_lag);
			this.addChild(lag_icons.lag);
		}
		
		private function updateIconsProperty():void
		{
			for each (var icon:Bitmap in this.icons)
			{
				icon.visible = false;
				icon.x = 10;
				icon.y = 25;
				icon.width = 190;
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
			if (this.lag_icons.lag.visible != _lag)
			{
				this.lag_icons.lag.visible = _lag;
			}
			this.updatePingIcon(_ping);
		}
		
		private function updatePingIcon(_ping:int):void
		{
			var index:int =
				(_ping < 15) ? 0 :
				(_ping < 30) ? 1 :
				(_ping < 40) ? 2 :
				(_ping < 60) ? 3 :
				(_ping < 80) ? 4 :
				(_ping < 100) ? 5 :
				(_ping < 150) ? 6 :
				(_ping < 200) ? 7 :
				(_ping < 300) ? 8 : 9;
			
			if (this.lastVisibleIcon !== this.icons[index])
			{
				this.lastVisibleIcon.visible = false;
				this.lastVisibleIcon = this.icons[index];
				this.lastVisibleIcon.visible = true;
			}
		}
	}
}