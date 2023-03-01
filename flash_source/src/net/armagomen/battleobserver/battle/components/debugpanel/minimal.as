package net.armagomen.battleobserver.battle.components.debugpanel
{
	import flash.display.Sprite;
	import flash.text.TextFieldAutoSize;
	import flash.text.TextFormat;
	import mx.utils.StringUtil;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class minimal extends Sprite
	{
		private var debugText:TextExt = null;
		private const template:String = "FPS: <font color='{0}'><b>{1}</b></font>\tPING: <font color='{2}'><b>{3}</b></font>";
		private var fpsColor:String   = "#B3FE95";
		private var pingColor:String  = "#B3FE95";
		private var lagColor:String   = "#FD9675";
		
		public function minimal(shadow_settings:Object, colors:Object)
		{
			super();
			var largeText:TextFormat = Filters.largeText;
			largeText.tabStops = [80];
			this.debugText = new TextExt(5, 0, largeText, TextFieldAutoSize.LEFT, shadow_settings, this);
			this.fpsColor = colors.fpsColor;
			this.pingColor = colors.pingColor;
			this.lagColor = colors.pingLagColor;
		}
		
		public function update(ping:int, fps:int, lag:Boolean):void
		{
			this.debugText.htmlText = StringUtil.substitute(this.template, this.fpsColor, fps, lag ? this.lagColor : this.pingColor, ping);
		}
	}
}