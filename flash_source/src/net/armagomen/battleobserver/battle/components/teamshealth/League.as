package net.armagomen.battleobserver.battle.components.teamshealth
{
	import fl.transitions.Tween;
	import flash.display.*;
	import net.armagomen.battleobserver.utils.Utils;
	
	public class League extends Sprite
	{
		private var allyHpBar:Shape         = new Shape();
		private var enemyHpBar:Shape        = new Shape();
		private var hpBars_bg:Shape         = new Shape();
		private var allyAnimation:Tween     = null;
		private var enemyAnimation:Tween    = null;
		private var defCommads:Vector.<int> = new <int>[1, 2, 2, 2, 2];
		private var colors:Object;
		private var animationEnabled:Boolean = false
		
		public function League(animation:Boolean, settings:Object, barWidth:Number, colorBlind:Boolean, colors:Object)
		{
			super();
			this.animationEnabled = animation;
			this.addChild(hpBars_bg);
			this.addChild(allyHpBar);
			this.addChild(enemyHpBar);
			this.colors = colors;
			var barsWidth:Number = 50 + barWidth;
			var barHeight:Number = 31;
			this.hpBars_bg.graphics.beginFill(Utils.colorConvert(colors.bgColor), Math.max(0.1, colors.bgAlpha));
			this.hpBars_bg.graphics.drawPath(defCommads, new <Number>[-barsWidth, 0, barsWidth, 0, barsWidth - 20, barHeight, -barsWidth + 20, barHeight, -barsWidth, 0]);
			this.hpBars_bg.graphics.endFill();
			this.allyHpBar.graphics.beginFill(Utils.colorConvert(colors.ally), Math.max(0.1, colors.alpha));
			this.allyHpBar.graphics.drawPath(defCommads, new <Number>[0, 0, -barsWidth, 0, -barsWidth + 20, barHeight, 0, barHeight, 0, 0]);
			this.allyHpBar.graphics.endFill();
			this.enemyHpBar.graphics.beginFill(Utils.colorConvert(colorBlind ? colors.enemyColorBlind : colors.enemy), Math.max(0.1, colors.alpha));
			this.enemyHpBar.graphics.drawPath(defCommads, new <Number>[0, 0, barsWidth, 0, barsWidth - 20, barHeight, 0, barHeight, 0, 0]);
			this.enemyHpBar.graphics.endFill();
			if (this.animationEnabled)
			{
				this.allyAnimation = new Tween(this.allyHpBar, "scaleX", null, this.allyHpBar.scaleX, 1.0, 1, true);
				this.allyAnimation.FPS = 30;
				this.enemyAnimation = new Tween(this.enemyHpBar, "scaleX", null, this.enemyHpBar.scaleX, 1.0, 1, true);
				this.enemyAnimation.FPS = 30;
			}
		
		}
		
		public function setColorBlind(enabled:Boolean):void
		{
			Utils.updateColor(this.enemyHpBar, enabled ? this.colors.enemyColorBlind : this.colors.enemy);
		}
		
		public function setBarScale(team:String, newScale:Number):void
		{
			var bar:Shape = team == "green" ? this.allyHpBar : this.enemyHpBar
			if (bar.scaleX != newScale)
			{
				if (this.animationEnabled)
				{
					(team == "green" ? this.allyAnimation : this.enemyAnimation).continueTo(newScale, 1);
				}
				else
				{
					bar.scaleX = newScale;
				}
			}
		}
	}

}