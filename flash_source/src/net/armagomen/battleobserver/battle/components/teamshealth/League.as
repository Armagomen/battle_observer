package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.display.*;
	import net.armagomen.battleobserver.utils.Utils;
	import net.armagomen.battleobserver.utils.tween.Tween;
	
	public class League extends Sprite
	{
		private var allyHpBar:Shape         = new Shape();
		private var enemyHpBar:Shape        = new Shape();
		private var hpBars_bg:Shape         = new Shape();
		private var allyAnimation:Tween     = null;
		private var enemyAnimation:Tween    = null;
		private var defCommads:Vector.<int> = new <int>[1, 2, 2, 2, 2];
		private var colors:Object;
		
		public function League(settings:Object, barWidth:Number, colorBlind:Boolean, colors:Object)
		{
			super();
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
			this.allyAnimation = new Tween(this.allyHpBar, "scaleX", 1.0, 1.0, 1, true);
			this.enemyAnimation = new Tween(this.enemyHpBar, "scaleX", 1.0, 1.0, 1, true);
		
		}
		
		public function setColorBlind(enabled:Boolean):void
		{
			Utils.updateColor(this.enemyHpBar, enabled ? this.colors.enemyColorBlind : this.colors.enemy);
		}
		
		public function setBarScale(isEnemy:Boolean, newScale:Number):void
		{
			var bar:Shape = isEnemy ? this.enemyHpBar : this.allyHpBar;
			if (bar.scaleX != newScale)
			{
				(isEnemy ? this.enemyAnimation : this.allyAnimation).continueTo(newScale, 1);
			}
		}
		
		public function remove():void
		{
			this.removeChildren();
			this.allyHpBar = null;
			this.enemyHpBar = null;
			this.hpBars_bg = null;
			this.allyAnimation.stop();
			this.allyAnimation = null;
			this.enemyAnimation.stop();
			this.enemyAnimation = null;
			App.utils.data.cleanupDynamicObject(this.colors);
		}
	}

}