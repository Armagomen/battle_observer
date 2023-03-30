package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.display.*;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.battle.components.teamshealth.score.Score;
	import net.armagomen.battleobserver.battle.interfaces.ITeamHealth;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.ProgressBar;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class Default extends Sprite implements ITeamHealth
	{
		private var greenText:TextExt;
		private var redText:TextExt;
		private var greenDiff:TextExt;
		private var redDiff:TextExt;
		private var allyBar:ProgressBar;
		private var enemyBar:ProgressBar;
		private var colors:Object;
		private var score:Score;
		
		public function Default(colorBlind:Boolean, colors:Object)
		{
			super();
			this.colors = colors;

			var alpha:Number   = Math.max(0.2, colors.alpha);
			var bgAlpha:Number = Math.max(0.2, colors.bgAlpha);
			
			this.allyBar = new ProgressBar(-50, 4, -200, 22, alpha, bgAlpha, null, colors.ally, null, 0.5);
			this.enemyBar = new ProgressBar(50, 4, 200, 22, alpha, bgAlpha, null, colorBlind ? colors.enemyColorBlind : colors.enemy, null, 0.5);
			this.allyBar.setOutline(colors.ally, alpha, -200, 22);
			this.enemyBar.setOutline(colorBlind ? colors.enemyColorBlind : colors.enemy, alpha, 200, 22);
			this.addChild(this.allyBar);
			this.addChild(this.enemyBar);
			
			this.greenText = new TextExt(-150, 1, Filters.middleText, TextFieldAutoSize.CENTER, this);
			this.redText = new TextExt(150, 1, Filters.middleText, TextFieldAutoSize.CENTER, this);
			this.greenDiff = new TextExt(-55, 2, Filters.normalText, TextFieldAutoSize.RIGHT, this);
			this.redDiff = new TextExt(55, 2, Filters.normalText, TextFieldAutoSize.LEFT, this);
			
			this.score = new Score(colorBlind);
			this.addChild(score);
		
		}
		
		public function setColorBlind(enabled:Boolean):void
		{
			this.enemyBar.updateColor(enabled ? this.colors.enemyColorBlind : this.colors.enemy);
			this.score.setColorBlind(enabled);
		}
		
		public function updateScore(ally:int, enemy:int):void
		{
			this.score.updateScore(ally, enemy);
		}
		
		public function setBarScale(isEnemy:Boolean, percent:Number):void
		{
			(isEnemy ? this.enemyBar : this.allyBar).setNewScale(percent);
		}
		
		public function remove():void
		{
			this.removeChildren();
			this.allyBar.remove();
			this.allyBar = null;
			this.enemyBar.remove();
			this.enemyBar = null;
			this.greenText = null;
			this.redText = null;
			this.greenDiff = null;
			this.redDiff = null;
			this.score.removeChildren();
			this.score = null;
		}
		
		public function update(alliesHP:int, enemiesHP:int, totalAlliesHP:int, totalEnemiesHP:int):void
		{
			this.setBarScale(false, totalAlliesHP > 0 ? Math.min(alliesHP / totalAlliesHP, 1.0) : 1.0);
			this.setBarScale(true, totalEnemiesHP > 0 ? Math.min(enemiesHP / totalEnemiesHP, 1.0) : 1.0);
			this.greenText.text = alliesHP.toString();
			this.redText.text = enemiesHP.toString();
			this.difference(alliesHP - enemiesHP);
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
	}
}