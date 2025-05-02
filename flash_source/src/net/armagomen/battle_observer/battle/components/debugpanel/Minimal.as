package net.armagomen.battle_observer.battle.components.debugpanel
{
	import flash.display.Sprite;
	import flash.display.Bitmap;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	import net.armagomen.battle_observer.utils.Utils;
	
	public class Minimal extends Sprite
	{
		
		[Embed(source = "ping_img/good.png")]
		private var good:Class;
		[Embed(source = "ping_img/bad.png")]
		private var bad:Class;
		[Embed(source = "ping_img/bad_cb.png")]
		private var bad_cb:Class;
		
		private var lag:Bitmap             = App.colorSchemeMgr.getIsColorBlindS() ? new bad_cb() : new bad();
		private var no_lag:Bitmap          = new good();
		
		private var statical:TextExt = null;
		private var fps:TextExt      = null;
		private var ping:TextExt     = null;
		private var lags:Boolean     = false;
		
		public function Minimal(settings:Object, panel:*)
		{
			super();
			lag.x = 175;
			lag.y = 4;
			lag.visible = false;
			lag.width = 22;
			lag.height = 22;
			lag.smoothing = true;
			no_lag.x = 175;
			no_lag.y = 4;
			no_lag.visible = true;
			no_lag.width = 22;
			no_lag.height = 22;
			no_lag.smoothing = true;
			this.statical = new TextExt(5, 0, Constants.largeText, TextFieldAutoSize.LEFT, this);
			this.statical.htmlText = "<textformat tabstops='[80]'>FPS:\tPING:</textformat>";
			this.fps = new TextExt(46, 0, Constants.largeText, TextFieldAutoSize.LEFT, this);
			this.fps.textColor = Utils.colorConvert(settings.fpsColor);
			this.ping = new TextExt(136, 0, Constants.largeText, TextFieldAutoSize.LEFT, this);
			this.ping.textColor = Utils.colorConvert(settings.pingColor);
			this.addChild(this.no_lag);
			this.addChild(this.lag);
			panel.addChild(this);
		}
		
		public function update(_ping:int, _fps:int, _lag:Boolean):void
		{
			this.ping.text = _ping.toString();
			this.fps.text = _fps.toString();
			if (this.lags != _lag)
			{
				this.lags = _lag;
				this.lag.visible = _lag;
			}
		}
	}
}