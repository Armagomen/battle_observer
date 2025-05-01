package net.armagomen.battle_observer.battle.components.debugpanel
{
	import flash.display.Sprite;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	import net.armagomen.battle_observer.utils.Utils;
	
	public class Minimal extends Sprite
	{
		private var pingColor:uint   = Utils.colorConvert("#B3FE95");
		private var lagColor:uint    = Utils.colorConvert("#FD9675");
		
		private var statical:TextExt = null;
		private var fps:TextExt      = null;
		private var ping:TextExt     = null;
		private var lags:Boolean     = false;
		
		public function Minimal(settings:Object, panel:*)
		{
			super();
			this.pingColor = Utils.colorConvert(settings.pingColor);
			this.lagColor = Utils.colorConvert(settings.pingLagColor);
			this.statical = new TextExt(5, 0, Constants.largeText, TextFieldAutoSize.LEFT, this);
			this.statical.htmlText = "<textformat tabstops='[80]'>FPS:\tPING:</textformat>";
			this.fps = new TextExt(46, 0, Constants.largeText, TextFieldAutoSize.LEFT, this);
			this.fps.textColor = Utils.colorConvert(settings.fpsColor);
			this.ping = new TextExt(136, 0, Constants.largeText, TextFieldAutoSize.LEFT, this);
			this.ping.textColor = this.pingColor;
			panel.addChild(this);
		}
		
		public function update(_ping:int, _fps:int, _lag:Boolean):void
		{
			this.ping.text = _ping.toString();
			this.fps.text = _fps.toString();
			if (this.lags != _lag)
			{
				this.lags = _lag;
				this.ping.textColor = _lag ? this.lagColor : this.pingColor;
			}
		}
	}
}