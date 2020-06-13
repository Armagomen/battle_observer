package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.display.*;
	import net.armagomen.battleobserver.battle.data.Constants;
	import net.armagomen.battleobserver.battle.utils.Animation;
	import net.armagomen.battleobserver.battle.utils.Params;
	import net.armagomen.battleobserver.battle.utils.Utils;

	public class Legue extends Sprite
	{
		private var allyHpBar:Shape = new Shape();
		private var enemyHpBar:Shape = new Shape();
		private var hpBars_bg:Shape = new Shape();
		private var allyAnimation:Animation = null;
		private var enemyAnimation:Animation = null;
		private var defCommads:Vector.<int> = new <int>[1, 2, 2, 2, 2];

		public function Legue(settings:Object, barWidth:Number)
		{
			super();
			this.addChild(hpBars_bg);
			this.addChild(allyHpBar);
			this.addChild(enemyHpBar);
			var colors:Object = settings.colors;
			var barsWidth:Number = 50 + barWidth;
			var barHeight:Number = 31;
			this.hpBars_bg.graphics.beginFill(Utils.colorConvert(colors.bgColor), Math.max(0.05, colors.bgAlpha));
			this.hpBars_bg.graphics.drawPath(defCommads, new <Number>[-barsWidth, 0, barsWidth, 0, barsWidth - 15, barHeight, -barsWidth + 15, barHeight, -barsWidth, 0]);
			this.hpBars_bg.graphics.endFill();
			this.allyHpBar.graphics.beginFill(Utils.colorConvert(colors.ally), Math.max(0.05, colors.alpha));
			this.allyHpBar.graphics.drawPath(defCommads, new <Number>[0, 0, -barsWidth, 0, -barsWidth + 15, barHeight, 0, barHeight, 0, 0]);
			this.allyHpBar.graphics.endFill();
			this.enemyHpBar.graphics.beginFill(Utils.colorConvert(Params.cBlind ? colors.enemyColorBlind : colors.enemy), Math.max(0.05, colors.alpha));
			this.enemyHpBar.graphics.drawPath(defCommads, new <Number>[0, 0, barsWidth, 0, barsWidth - 15, barHeight, 0, barHeight, 0, 0]);
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