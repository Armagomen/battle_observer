package net.armagomen.battleobserver.battle.components.teambases
{
	import fl.transitions.Tween;
	import flash.display.*;
	import flash.text.*;
	import net.armagomen.battleobserver.utils.Params;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.utils.Utils;
	
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
		
		public function TeamBase(team:String, colorBlind:Boolean)
		{
			super();
			this.name = team;
			this.colorBlind = colorBlind;
		}
		
		public function updateBase(newScale:Number, invadersCnt:String, time:String, text:String):void
		{
			if (Params.AnimationEnabled)
			{
				if (newScale > this.progressBar.scaleX) {
					this.animation.continueTo(newScale, 1);
				} else if (this.animation.isPlaying) {
					this.animation.stop();
					this.progressBar.scaleX = newScale;
				}
			}
			else
			{
				this.progressBar.scaleX = newScale;
			}
			this.status.htmlText = text;
			this.timer.text = time;
			this.invaders.text = invadersCnt;
		}
		
		public function updateCaptureText(captureText:String):void
		{
			this.status.htmlText = captureText;
		}
		
		public function create(bases:Object, shadowSettings:Object, colors:Object):void
		{
			this.basesFormat = new TextFormat(bases.text_settings.font, bases.text_settings.size, Utils.colorConvert(bases.text_settings.color), bases.text_settings.bold, bases.text_settings.italic, bases.text_settings.underline);
			createBase(bases, shadowSettings, colors);
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
		
		private function createBase(settings:Object, shadowSettings:Object, colors:Object):void
		{
			var progressBarColor:uint = Utils.colorConvert(this.name == "green" ? colors.ally : this.colorBlind ? colors.enemyColorBlind : colors.enemy);
			
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
			this.progressBar.scaleX = 0.01;
			baseMain.addChild(this.progressBar);
			baseMain.addChild(PlayersIcon(iconWidth));
			baseMain.addChild(TimeIcon(iconWidth, settings.width));
			
			this.status = new TextExt("status", settings.width >> 1, settings.text_settings.y, this.basesFormat, TextFieldAutoSize.CENTER, shadowSettings, baseMain);
			this.timer = new TextExt("timer", settings.width - iconWidth, settings.text_settings.y, this.basesFormat, TextFieldAutoSize.RIGHT, shadowSettings, baseMain);
			this.invaders = new TextExt("invaders", iconWidth, settings.text_settings.y, this.basesFormat, TextFieldAutoSize.LEFT, shadowSettings, baseMain);
			
			baseMain.scaleX = baseMain.scaleY = settings.scale;
			this.x = App.appWidth / 2 - baseMain.width / 2;
			this.y = settings.y;
			
			if (Params.AnimationEnabled)
			{
				this.animation = new Tween(this.progressBar, "scaleX", null, this.progressBar.scaleX, 0, 1, true);
				this.animation.FPS = 30;
			}
		}
	
	}
}