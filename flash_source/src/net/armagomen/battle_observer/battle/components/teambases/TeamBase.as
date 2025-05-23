﻿package net.armagomen.battle_observer.battle.components.teambases
{
	import Math;
	import flash.display.*;
	import flash.text.*;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	import net.armagomen.battle_observer.utils.Utils;
	import net.armagomen.battle_observer.utils.tween.Tween;
	
	/**
	 * ...
	 * @author Armagomen
	 */
	public dynamic class TeamBase extends Sprite
	{
		private var colorBlind:Boolean     = false;
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
		
		public function TeamBase(colorBlind:Boolean)
		{
			super();
			this.colorBlind = colorBlind;
		}
		
		public function updateBase(points:int, invadersCnt:int, time:String, text:String):void
		{
			var scale:Number = Math.min(1.0, (points < 100 ? points + invadersCnt : points) * Constants.HUNDREDTH);
			this.animation.continueTo(scale, scale > this.progressBar.scaleX ? 1.0 : Constants.HUNDREDTH);
			this.status.htmlText = text;
			this.timer.text = time;
			this.invaders.text = invadersCnt.toString();
		}
		
		public function updateCaptureText(captureText:String):void
		{
			this.status.htmlText = captureText;
		}
		
		public function create(settings:Object, colors:Object, team:String):void
		{
			this.basesFormat = new TextFormat(settings.text_settings.font, settings.text_settings.size, Utils.colorConvert(settings.text_settings.color), settings.text_settings.bold, settings.text_settings.italic, settings.text_settings.underline);
			this.createBase(settings, colors, team);
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
		
		private function createBase(settings:Object, colors:Object, team:String):void
		{
			var progressBarColor:uint = Utils.colorConvert(team == "green" ? colors.ally : this.colorBlind ? colors.enemyColorBlind : colors.enemy);
			
			var baseMain:Sprite       = new Sprite()
			this.addChild(baseMain)
			var iconWidth:Number = settings.height + 2;
			
			baseMain.y = 1;
			baseMain.graphics.beginFill(Utils.colorConvert(colors.bgColor), Constants.BG_ALPHA);
			baseMain.graphics.drawRect(0, 0, settings.width, settings.height);
			baseMain.graphics.endFill();
			baseMain.graphics.lineStyle(1, progressBarColor, Constants.ALPHA, true, LineScaleMode.NONE);
			baseMain.graphics.drawRect(-1, -1, settings.width + 1, settings.height + 1);
			this.progressBar.graphics.beginFill(progressBarColor, Constants.ALPHA);
			this.progressBar.graphics.drawRect(0, 0, settings.width, settings.height);
			this.progressBar.graphics.endFill();
			this.progressBar.scaleX = Constants.HUNDREDTH;
			baseMain.addChild(this.progressBar);
			baseMain.addChild(PlayersIcon(iconWidth));
			baseMain.addChild(TimeIcon(iconWidth, settings.width));
			
			this.status = new TextExt(settings.width * 0.5, settings.text_settings.y, this.basesFormat, TextFieldAutoSize.CENTER, baseMain);
			this.timer = new TextExt(settings.width - iconWidth, settings.text_settings.y, this.basesFormat, TextFieldAutoSize.RIGHT, baseMain);
			this.invaders = new TextExt(iconWidth, settings.text_settings.y, this.basesFormat, TextFieldAutoSize.LEFT, baseMain);
			
			this.x = App.appWidth * 0.5 - baseMain.width * 0.5;
			this.y = settings.y >= 0 ? settings.y : App.appHeight + settings.y;
			
			this.animation = new Tween(this.progressBar, "scaleX", this.progressBar.scaleX, 1.0);
		}
	}
}