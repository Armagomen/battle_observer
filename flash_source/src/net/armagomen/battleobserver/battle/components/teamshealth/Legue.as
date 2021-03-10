package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.display.*;
	import net.armagomen.battleobserver.data.Constants;
	import net.armagomen.battleobserver.utils.Params;
	import net.armagomen.battleobserver.utils.Utils;
	import fl.transitions.Tween;

	public class Legue extends Sprite
	{
		private var allyHpBar:Shape = new Shape();
		private var enemyHpBar:Shape = new Shape();
		private var hpBars_bg:Shape = new Shape();
		private var allyAnimation:Tween = null;
		private var enemyAnimation:Tween = null;
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
			this.hpBars_bg.graphics.drawPath(defCommads, new <Number>[-barsWidth, 0, barsWidth, 0, barsWidth - 20, barHeight, -barsWidth + 20, barHeight, -barsWidth, 0]);
			this.hpBars_bg.graphics.endFill();
			this.allyHpBar.graphics.beginFill(Utils.colorConvert(colors.ally), Math.max(0.05, colors.alpha));
			this.allyHpBar.graphics.drawPath(defCommads, new <Number>[0, 0, -barsWidth, 0, -barsWidth + 20, barHeight, 0, barHeight, 0, 0]);
			this.allyHpBar.graphics.endFill();
			this.enemyHpBar.graphics.beginFill(Utils.colorConvert(Params.cBlind ? colors.enemyColorBlind : colors.enemy), Math.max(0.05, colors.alpha));
			this.enemyHpBar.graphics.drawPath(defCommads, new <Number>[0, 0, barsWidth, 0, barsWidth - 20, barHeight, 0, barHeight, 0, 0]);
			this.enemyHpBar.graphics.endFill();
			this.allyAnimation = new Tween(this.allyHpBar, "scaleX", null, this.allyHpBar.scaleX, 1.0, 1, true);
			this.allyAnimation.FPS = 30;
			this.enemyAnimation = new Tween(this.enemyHpBar, "scaleX", null, this.enemyHpBar.scaleX, 1.0, 1, true);
			this.enemyAnimation.FPS = 30;
		}
		
		public function stopAndClearAnimate():void{
			if (this.allyAnimation != null && this.allyAnimation.isPlaying){
				this.allyAnimation.stop();
			}
			if (this.enemyAnimation != null && this.enemyAnimation.isPlaying){
				this.enemyAnimation.stop();
			}
			this.allyAnimation = null;
			this.enemyAnimation = null;
			this.allyHpBar = null;
			this.enemyHpBar = null;
			this.hpBars_bg = null;
		}

		public function setBarScale(team:String, newScale:Number):void
		{
			if (Params.AnimationEnabled)
			{
				(team == "green" ? this.allyAnimation : this.enemyAnimation).continueTo(newScale, 1);
			}
			else
			{
				(team == "green" ? this.allyHpBar : this.enemyHpBar).scaleX = newScale;
			}
		}
	}

}