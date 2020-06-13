package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.display.*;
	import net.armagomen.battleobserver.battle.data.Constants;
	import net.armagomen.battleobserver.battle.utils.Animation;
	import net.armagomen.battleobserver.battle.utils.Params;
	import net.armagomen.battleobserver.battle.utils.Utils;

	public class Default extends Sprite
	{
		private var allyHpBar:Shape = new Shape();
		private var enemyHpBar:Shape = new Shape();
		private var hpBars_bg:Shape = new Shape();
		private var allyAnimation:Animation = null;
		private var enemyAnimation:Animation = null;

		public function Default(settings:Object, barWidth:Number)
		{
			super();
			this.addChild(hpBars_bg);
			this.addChild(allyHpBar);
			this.addChild(enemyHpBar);
			var colors:Object = settings.colors;
			this.hpBars_bg.graphics.beginFill(Utils.colorConvert(colors.bgColor), Math.max(0.05, colors.bgAlpha));
			this.hpBars_bg.graphics.drawRect(-50, 5, -barWidth, 20);
			this.hpBars_bg.graphics.drawRect(50, 5, barWidth, 20);
			this.hpBars_bg.graphics.endFill();
			if (settings.outline.enabled)
			{
				this.hpBars_bg.graphics.lineStyle(1, Utils.colorConvert(settings.outline.color), Math.max(0.05, colors.bgAlpha), true);
				this.hpBars_bg.graphics.drawRect(-50, 4, -(barWidth + 1), 21);
				this.hpBars_bg.graphics.drawRect(49, 4, barWidth + 1, 21);
			}
			this.allyHpBar.x = -50;
			this.allyHpBar.graphics.beginFill(Utils.colorConvert(colors.ally), Math.max(0.05, colors.alpha));
			this.allyHpBar.graphics.drawRect(0, 5, -barWidth, 20);
			this.allyHpBar.graphics.endFill();
			this.enemyHpBar.x = 50;
			this.enemyHpBar.graphics.beginFill(Utils.colorConvert(Params.cBlind ? colors.enemyColorBlind : colors.enemy), Math.max(0.05, colors.alpha));
			this.enemyHpBar.graphics.drawRect(0, 5, barWidth, 20);
			this.enemyHpBar.graphics.endFill();
			this.allyAnimation = new Animation(this.allyHpBar, Constants.ANIMATE_SPEED_MAINBAR);
			this.enemyAnimation = new Animation(this.enemyHpBar, Constants.ANIMATE_SPEED_MAINBAR);
		}

		public function setBarScale(team:String, newScale:Number):void
		{
			if (Params.AnimationEnabled)
			{
				(team == "green" ? this.allyAnimation : this.enemyAnimation).runAnimation(newScale);
			}
			else
			{
				(team == "green" ? this.allyHpBar : this.enemyHpBar).scaleX = newScale;
			}
		}
	}
}