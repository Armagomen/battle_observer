package net.armagomen.battleobserver.battle.components.debugpanel
{
	import flash.display.Sprite;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.utils.Utils;
	import net.armagomen.battleobserver.battle.interfaces.IDebugPanel;
	
	public class minimal extends Sprite implements IDebugPanel
	{
		private var pingColor:uint  = Utils.colorConvert("#B3FE95");
		private var lagColor:uint   = Utils.colorConvert("#FD9675");
		
		private var PATTERN:TextExt = null;
		private var FPS:TextExt     = null;
		private var PING:TextExt    = null;
		
		public function minimal(colors:Object)
		{
			super();
			this.PATTERN = new TextExt(5, 0, Filters.largeText, TextFieldAutoSize.LEFT, this);
			this.PATTERN.htmlText = "<textformat tabstops='[80]'>FPS:\tPING:</textformat>";
			this.FPS = new TextExt(46, 0, Filters.largeText, TextFieldAutoSize.LEFT, this);
			this.PING = new TextExt(136, 0, Filters.largeText, TextFieldAutoSize.LEFT, this);
			this.pingColor = Utils.colorConvert(colors.pingColor);
			this.lagColor = Utils.colorConvert(colors.pingLagColor);
			this.FPS.textColor = Utils.colorConvert(colors.fpsColor);
			this.PING.textColor = this.pingColor;
		}
		
		public function update(ping:int, fps:int, lag:Boolean):void
		{
			this.PING.text = ping.toString();
			this.FPS.text = fps.toString();
			
			var color:uint = lag ? this.lagColor : this.pingColor;
			
			if (this.PING.textColor != color)
			{
				this.PING.textColor = color
			}
		}
	}
}