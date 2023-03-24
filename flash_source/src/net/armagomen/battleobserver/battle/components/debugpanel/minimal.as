package net.armagomen.battleobserver.battle.components.debugpanel
{
	import flash.display.Sprite;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.utils.Utils;
	import net.armagomen.battleobserver.battle.interfaces.IDebugPanel;
	
	public class Minimal extends Sprite implements IDebugPanel
	{
		private var pingColor:uint   = Utils.colorConvert("#B3FE95");
		private var lagColor:uint    = Utils.colorConvert("#FD9675");
		
		private var statical:TextExt = null;
		private var fps:TextExt      = null;
		private var ping:TextExt     = null;
		
		public function Minimal(settings:Object)
		{
			super();
			this.pingColor = Utils.colorConvert(settings.pingColor);
			this.lagColor = Utils.colorConvert(settings.pingLagColor);
			this.statical = new TextExt(5, 0, Filters.largeText, TextFieldAutoSize.LEFT, this);
			this.statical.htmlText = "<textformat tabstops='[80]'>FPS:\tPING:</textformat>";
			this.fps = new TextExt(46, 0, Filters.largeText, TextFieldAutoSize.LEFT, this);
			this.fps.textColor = Utils.colorConvert(settings.fpsColor);
			this.ping = new TextExt(136, 0, Filters.largeText, TextFieldAutoSize.LEFT, this);
			this.ping.textColor = this.pingColor;
		}
		
		public function update(ping:int, fps:int, lag:Boolean):void
		{
			this.ping.text = ping.toString();
			this.fps.text = fps.toString();
			
			var color:uint = lag ? this.lagColor : this.pingColor;
			
			if (this.ping.textColor != color)
			{
				this.ping.textColor = color
			}
		}
	}
}