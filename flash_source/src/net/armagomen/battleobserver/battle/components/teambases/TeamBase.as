package net.armagomen.battleobserver.battle.components.teambases
{
	import net.armagomen.battleobserver.utils.tween.Tween;
	import flash.display.*;
	import flash.text.*;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.utils.Utils;
	import Math;
	
	/**
	 * ...
	 * @author Armagomen
	 */
	public dynamic class TeamBase extends Sprite
	{
		private var progressBar:Shape      = new Shape();
		private var status:TextExt;
		private var timer:TextExt;
		private var invaders:TextExt;
		private var basesFormat:TextFormat = new TextFormat("$TitleFont", 16, 0xFAFAFA);
		private var animation:Tween        = null;
		[Embed(source = "players.png")]
		private var Players:Class;
		[Embed(source = "timer.png")]
		private var Time:Class;
		
		private var colorBlind:Boolean     = false;
		
		public function TeamBase(colorBlind:Boolean)
		{
			super();
			this.colorBlind = colorBlind;
		}
		
		public function updateBase(newScale:int, invadersCnt:int, time:String, text:String):void
		{
			var scale:Number = Math.min(1.0, (newScale + invadersCnt) * 0.01);
			this.animation.continueTo(scale, scale > this.progressBar.scaleX ? 1.0 : 0.01);
			this.status.htmlText = text;
			this.timer.text = time;
			this.invaders.text = invadersCnt.toString();
		}
		
		public function updateCaptureText(captureText:String):void
		{
			this.status.htmlText = captureText;
		}
		
		public function create(bases:Object, shadowSettings:Object, colors:Object, team:String):void
		{
			this.basesFormat = new TextFormat(bases.text_settings.font, bases.text_settings.size, Utils.colorConvert(bases.text_settings.color), bases.text_settings.bold, bases.text_settings.italic, bases.text_settings.underline);
			this.createBase(bases, shadowSettings, colors, team);
		}
		
		public function remove():void
		{
			this.animation.stop();
			this.removeChildren();
			this.progressBar = null;
			this.status = null;
			this.timer = null;
			this.invaders = null;
			this.basesFormat = null;
			this.animation = null;
			this.colorBlind = false;
			this.animate = false;
		}
		
		private function PlayersIcon(width:Number):Bitmap
		{
			var icon:Bitmap = new Players();
			icon.width = icon.height = width;
			icon.y = -1;
			icon.smoothing = true;
			icon.alpha = 0.9;
			return icon;
		}
		
		private function TimeIcon(width:Number, panelWidth:Number):Bitmap
		{
			var icon:Bitmap = new Time();
			icon.width = icon.height = width;
			icon.x = panelWidth - icon.width;
			icon.y = -1;
			icon.smoothing = true;
			icon.alpha = 0.9;
			return icon;
		}
		
		private function createBase(settings:Object, shadowSettings:Object, colors:Object, team:String):void
		{
			var progressBarColor:uint = Utils.colorConvert(team == "green" ? colors.ally : this.colorBlind ? colors.enemyColorBlind : colors.enemy);
			
			var baseMain:Sprite       = new Sprite()
			this.addChild(baseMain)
			var iconWidth:Number = settings.height + 2;
			
			baseMain.y = 1;
			baseMain.graphics.beginFill(Utils.colorConvert(colors.bgColor), Math.max(0.05, colors.bgAlpha));
			baseMain.graphics.drawRect(0, 0, settings.width, settings.height);
			baseMain.graphics.endFill();
			
			if (settings.outline.enabled)
			{
				baseMain.graphics.lineStyle(1, Utils.colorConvert(settings.outline.color), Math.max(0.05, colors.bgAlpha), true, LineScaleMode.NONE);
				baseMain.graphics.drawRect(-1, -1, settings.width + 1, settings.height + 1);
			}
			
			this.progressBar.name = this.name;
			this.progressBar.graphics.beginFill(progressBarColor, Math.max(0.05, colors.alpha));
			this.progressBar.graphics.drawRect(0, 0, settings.width, settings.height);
			this.progressBar.graphics.endFill();
			this.progressBar.scaleX = 0;
			baseMain.addChild(this.progressBar);
			baseMain.addChild(PlayersIcon(iconWidth));
			baseMain.addChild(TimeIcon(iconWidth, settings.width));
			
			this.status = new TextExt(settings.width * 0.5, settings.text_settings.y, this.basesFormat, TextFieldAutoSize.CENTER, shadowSettings, baseMain);
			this.timer = new TextExt(settings.width - iconWidth, settings.text_settings.y, this.basesFormat, TextFieldAutoSize.RIGHT, shadowSettings, baseMain);
			this.invaders = new TextExt(iconWidth, settings.text_settings.y, this.basesFormat, TextFieldAutoSize.LEFT, shadowSettings, baseMain);
			
			this.x = App.appWidth * 0.5 - baseMain.width * 0.5;
			this.y = settings.y >= 0 ? settings.y : App.appHeight + settings.y;
			
			this.animation = new Tween(this.progressBar, "scaleX", this.progressBar.scaleX, 1.0, 1.0, true);
		}
	
	}
}