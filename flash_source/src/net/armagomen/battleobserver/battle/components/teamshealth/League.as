package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.display.*;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.battle.components.teamshealth.score.Score;
	import net.armagomen.battleobserver.battle.interfaces.ITeamHealth;
	import net.armagomen.battleobserver.utils.Constants;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.utils.Utils;
	import net.armagomen.battleobserver.utils.tween.Tween;
	
	public class League extends Sprite implements ITeamHealth
	{
		private var greenText:TextExt;
		private var redText:TextExt;
		private var greenDiff:TextExt;
		private var redDiff:TextExt;
		private var allyBar:Shape           = new Shape();
		private var enemyBar:Shape          = new Shape();
		private var background:Shape        = new Shape();
		private var allyAnimation:Tween     = null;
		private var enemyAnimation:Tween    = null;
		private var defCommads:Vector.<int> = new <int>[1, 2, 2, 2, 2];
		private var colors:Object;
		private var score:Score;
		private var duration:Number         = 0.5;
		
		public function League(colorBlind:Boolean, colors:Object)
		{
			super();
			this.addChild(background);
			this.addChild(allyBar);
			this.addChild(enemyBar);
			this.colors = colors;
			this.background.graphics.beginFill(Utils.colorConvert(colors.bgColor), Constants.BG_ALPHA);
			this.background.graphics.drawPath(defCommads, new <Number>[-250, 0, 250, 0, 230, 31, -230, 31, -250, 0]);
			this.background.graphics.endFill();
			this.allyBar.graphics.beginFill(Utils.colorConvert(colors.ally), Constants.ALPHA);
			this.allyBar.graphics.drawPath(defCommads, new <Number>[0, 0, -250, 0, -230, 31, 0, 31, 0, 0]);
			this.allyBar.graphics.endFill();
			this.enemyBar.graphics.beginFill(Utils.colorConvert(colorBlind ? colors.enemyColorBlind : colors.enemy), Constants.ALPHA);
			this.enemyBar.graphics.drawPath(defCommads, new <Number>[0, 0, 250, 0, 230, 31, 0, 31, 0, 0]);
			this.enemyBar.graphics.endFill();
			this.allyAnimation = new Tween(this.allyBar, "scaleX", 1.0, 0, this.duration);
			this.enemyAnimation = new Tween(this.enemyBar, "scaleX", 1.0, 0, this.duration);
			
			this.greenText = new TextExt(-220, 1, Constants.middleText, TextFieldAutoSize.LEFT, this);
			this.redText = new TextExt(220, 1, Constants.middleText, TextFieldAutoSize.RIGHT, this);
			this.greenDiff = new TextExt(-55, 4, Constants.diff, TextFieldAutoSize.RIGHT, this);
			this.redDiff = new TextExt(55, 4, Constants.diff, TextFieldAutoSize.LEFT, this);
			
			this.score = new Score(colorBlind);
			this.addChild(score);
		
		}
		
		public function setColorBlind(enabled:Boolean):void
		{
			Utils.updateColor(this.enemyBar, enabled ? this.colors.enemyColorBlind : this.colors.enemy);
			this.score.setColorBlind(enabled);
		}
		
		public function updateScore(ally:int, enemy:int):void
		{
			this.score.updateScore(ally, enemy);
		}
		
		public function setBarScale(isEnemy:Boolean, newScale:Number):void
		{
			var bar:Shape       = isEnemy ? this.enemyBar : this.allyBar;
			var animation:Tween = isEnemy ? this.enemyAnimation : this.allyAnimation
			if (bar.scaleX != newScale)
			{
				if (newScale > bar.scaleX)
				{
					animation.rewind(newScale);
				}
				else
				{
					animation.continueTo(newScale, this.duration);
				}
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
			this.greenText = null;
			this.redText = null;
			this.greenDiff = null;
			this.redDiff = null;
			this.score.removeChildren();
			this.score = null;
			App.utils.data.cleanupDynamicObject(this.colors);
		}
		
		private function difference(param:int):void
		{
			if (param < 0)
			{
				this.redDiff.text = "+".concat(Math.abs(param).toString());
				this.greenDiff.text = "";
			}
			else if (param > 0)
			{
				this.greenDiff.text = "+".concat(param.toString());
				this.redDiff.text = "";
			}
			else
			{
				this.greenDiff.text = "";
				this.redDiff.text = "";
			}
		}
		
		public function update(alliesHP:int, enemiesHP:int, totalAlliesHP:int, totalEnemiesHP:int):void
		{
			this.setBarScale(false, totalAlliesHP > 0 ? Math.min(alliesHP / totalAlliesHP, 1.0) : 1.0);
			this.setBarScale(true, totalEnemiesHP > 0 ? Math.min(enemiesHP / totalEnemiesHP, 1.0) : 1.0);
			this.greenText.text = alliesHP.toString();
			this.redText.text = enemiesHP.toString();
			this.difference(alliesHP - enemiesHP);
		}
	}
}