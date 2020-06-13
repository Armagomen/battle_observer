package net.armagomen.battleobserver.battle.components.teambases
{
	import flash.display.*;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.data.Constants;
	import net.armagomen.battleobserver.battle.utils.Animation;
	import net.armagomen.battleobserver.battle.utils.Params;
	import net.armagomen.battleobserver.battle.utils.TextExt;
	import net.armagomen.battleobserver.battle.utils.Utils;

	/**
	 * ...
	 * @author Armagomen
	 */
	public dynamic class TeamBase extends Sprite
	{
		public var progressBar:Shape = new Shape();
		public var BaseText:TextField;
		public var BaseTimer:TextField;
		public var BaseVehicles:TextField;
		private var basesFormat:TextFormat = new TextFormat("$TitleFont", 16, 0xFAFAFA);
		private var animation:Animation = null;
		[Embed(source = "players.png")]
		private var Players:Class;
		[Embed(source = "timer.png")]
		private var Time:Class;


		public function TeamBase(team:String)
		{
			super();
			this.name = team;
		}

		public function setBarScale(newScale:Number, rate:Number, invadersCnt:Number):void
		{
			this.animation.setNewSpeed(Constants.ANIMATE_SPEED_TEAMBASE * rate * invadersCnt);
			this.animation.runAnimation(newScale);
		}

		public function stopAnimation():void
		{
			this.animation.stopAnimation();
		}

		public function create(bases:Object, shadowSettings:Object):void
		{
			basesFormat = new TextFormat(bases.text_settings.font, bases.text_settings.size, Utils.colorConvert(bases.text_settings.color), bases.text_settings.bold, bases.text_settings.italic, bases.text_settings.underline);
			createBase(bases, shadowSettings);
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

		private function createBase(settings:Object, shadowSettings:Object):void
		{
			var progressBarColor:uint = Utils.colorConvert(!Params.cBlind ? settings.colors[this.name] : this.name != "green" ? settings.colors.purple : settings.colors[this.name]);

			var baseMain:Sprite = new Sprite()
			this.addChild(baseMain)
			var iconWidth:Number = settings.height + 2;

			baseMain.y = 1;
			baseMain.graphics.beginFill(Utils.colorConvert(settings.colors.bgColor), Math.max(0.05, settings.colors.bgAlpha));
			baseMain.graphics.drawRect(0, 0, settings.width, settings.height);
			baseMain.graphics.endFill();

			if (settings.outline.enabled)
			{
				baseMain.graphics.lineStyle(1, Utils.colorConvert(settings.outline.color), Math.max(0.05, settings.colors.bgAlpha), true, LineScaleMode.NONE);
				baseMain.graphics.drawRect(-1, -1, settings.width + 1, settings.height + 1);
			}

			progressBar.name = this.name;
			progressBar.graphics.beginFill(progressBarColor, Math.max(0.05, settings.colors.alpha));
			progressBar.graphics.drawRect(0, 0, settings.width, settings.height);
			progressBar.graphics.endFill();
			progressBar.scaleX = 0.01;
			baseMain.addChild(progressBar);
			baseMain.addChild(PlayersIcon(iconWidth));
			baseMain.addChild(TimeIcon(iconWidth, settings.width));


			BaseText = new TextExt("BaseText", settings.width >> 1, settings.text_settings.y, basesFormat, TextFieldAutoSize.CENTER, shadowSettings, baseMain);
			BaseTimer = new TextExt("BaseTimer", settings.width - iconWidth, settings.text_settings.y, basesFormat, TextFieldAutoSize.RIGHT, shadowSettings, baseMain);
			BaseVehicles = new TextExt("BaseVehicles", iconWidth, settings.text_settings.y, basesFormat, TextFieldAutoSize.LEFT, shadowSettings, baseMain);

			baseMain.scaleX = baseMain.scaleY = settings.scale;
			this.x = App.appWidth / 2 - baseMain.width / 2;
			this.y = settings.y;

			this.animation = new Animation(this.progressBar, Constants.ANIMATE_SPEED_TEAMBASE, true);
		}
	}
}