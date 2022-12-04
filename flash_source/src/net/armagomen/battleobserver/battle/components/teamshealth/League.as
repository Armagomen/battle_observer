package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.display.*;
	import net.armagomen.battleobserver.utils.Utils;
	import net.armagomen.battleobserver.utils.tween.Tween;
	
	public class League extends Sprite
	{
		private var allyBar:Shape           = new Shape();
		private var enemyBar:Shape          = new Shape();
		private var background:Shape        = new Shape();
		private var allyAnimation:Tween     = null;
		private var enemyAnimation:Tween    = null;
		private var defCommads:Vector.<int> = new <int>[1, 2, 2, 2, 2];
		private var colors:Object;
		
		public function League(barWidth:Number, colorBlind:Boolean, colors:Object)
		{
			super();
			this.addChild(background);
			this.addChild(allyBar);
			this.addChild(enemyBar);
			this.colors = colors;
			var barsWidth:Number = 50 + barWidth;
			var barHeight:Number = 31;
			this.background.graphics.beginFill(Utils.colorConvert(colors.bgColor), Math.max(0.2, colors.bgAlpha));
			this.background.graphics.drawPath(defCommads, new <Number>[-barsWidth, 0, barsWidth, 0, barsWidth - 20, barHeight, -barsWidth + 20, barHeight, -barsWidth, 0]);
			this.background.graphics.endFill();
			this.allyBar.graphics.beginFill(Utils.colorConvert(colors.ally), Math.max(0.2, colors.alpha));
			this.allyBar.graphics.drawPath(defCommads, new <Number>[0, 0, -barsWidth, 0, -barsWidth + 20, barHeight, 0, barHeight, 0, 0]);
			this.allyBar.graphics.endFill();
			this.enemyBar.graphics.beginFill(Utils.colorConvert(colorBlind ? colors.enemyColorBlind : colors.enemy), Math.max(0.2, colors.alpha));
			this.enemyBar.graphics.drawPath(defCommads, new <Number>[0, 0, barsWidth, 0, barsWidth - 20, barHeight, 0, barHeight, 0, 0]);
			this.enemyBar.graphics.endFill();
			this.allyAnimation = new Tween(this.allyBar, "scaleX", 1.0, 0, 0.5);
			this.enemyAnimation = new Tween(this.enemyBar, "scaleX", 1.0, 0, 0.5);
		}
		
		public function setColorBlind(enabled:Boolean):void
		{
			Utils.updateColor(this.enemyBar, enabled ? this.colors.enemyColorBlind : this.colors.enemy);
		}
		
		public function setBarScale(isEnemy:Boolean, newScale:Number):void
		{
			var bar:Shape = isEnemy ? this.enemyBar : this.allyBar;
			if (bar.scaleX != newScale)
			{
				(isEnemy ? this.enemyAnimation : this.allyAnimation).continueTo(newScale, 0.5);
			}
		}
		
		public function remove():void
		{
			this.removeChildren();
			this.allyAnimation.stop();
			this.allyAnimation = null;
			this.enemyAnimation.stop();
			this.enemyAnimation = null;
			this.allyBar = null;
			this.enemyBar = null;
			this.background = null;
			App.utils.data.cleanupDynamicObject(this.colors);
		}
	}

}