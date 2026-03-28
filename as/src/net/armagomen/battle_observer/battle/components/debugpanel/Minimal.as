package net.armagomen.battle_observer.battle.components.debugpanel
{
	import flash.display.Sprite;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battle_observer.battle.components.debugpanel.lag.LagIcons;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	import net.armagomen.battle_observer.utils.Utils;
	
	public class Minimal extends Sprite
	{
		private var lag_icons:LagIcons = new LagIcons()
		private var statical:TextExt   = null;
		private var fps:TextExt        = null;
		private var ping:TextExt       = null;
		
		public function Minimal(settings:Object)
		{
			super();
			this.lag_icons.lag.x = 175;
			this.lag_icons.lag.y = 4;
			this.lag_icons.lag.visible = false;
			this.lag_icons.lag.width = 22;
			this.lag_icons.lag.height = 22;
			this.lag_icons.lag.smoothing = true;
			this.lag_icons.no_lag.x = 175;
			this.lag_icons.no_lag.y = 4;
			this.lag_icons.no_lag.visible = true;
			this.lag_icons.no_lag.width = 22;
			this.lag_icons.no_lag.height = 22;
			this.lag_icons.no_lag.smoothing = true;
			this.statical = new TextExt(5, 0, Constants.largeText, TextFieldAutoSize.LEFT, this);
			this.statical.htmlText = "<textformat tabstops='[80]'>FPS:\tPING:</textformat>";
			this.fps = new TextExt(46, 0, Constants.largeText, TextFieldAutoSize.LEFT, this);
			this.fps.textColor = Utils.colorConvert(settings.fpsColor);
			this.ping = new TextExt(136, 0, Constants.largeText, TextFieldAutoSize.LEFT, this);
			this.ping.textColor = Utils.colorConvert(settings.pingColor);
			this.addChild(this.lag_icons.no_lag);
			this.addChild(this.lag_icons.lag);
		}
		
		public function update(_ping:int, _fps:int, _lag:Boolean):void
		{
			this.ping.text = _ping.toString();
			this.fps.text = _fps.toString();
			if (this.lag_icons.lag.visible != _lag)
			{
				this.lag_icons.lag.visible = _lag;
			}
		}
	}
}