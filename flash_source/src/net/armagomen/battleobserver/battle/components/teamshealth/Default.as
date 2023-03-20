package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.display.*;
	import net.armagomen.battleobserver.utils.ProgressBar;
	
	public class Default extends Sprite
	{
		
		private var allyBar:ProgressBar;
		private var enemyBar:ProgressBar;
		private var colors:Object;
		
		public function Default(outline:Object, barWidth:Number, colorBlind:Boolean, colors:Object)
		{
			super();
			this.colors = colors;
			
			this.allyBar = new ProgressBar(-50, 4, -barWidth, 22, Math.max(0.2, colors.alpha), Math.max(0.2, colors.bgAlpha), null, colors.ally, null, 0.5);
			this.enemyBar = new ProgressBar(50, 4, barWidth, 22, Math.max(0.2, colors.alpha), Math.max(0.2, colors.bgAlpha), null, colorBlind ? colors.enemyColorBlind : colors.enemy, null, 0.5);
			
			if (outline.enabled)
			{
				this.allyBar.setOutline(true, outline.color, Math.max(0.2, colors.alpha), -barWidth, 22);
				this.enemyBar.setOutline(true, outline.color, Math.max(0.2, colors.alpha), barWidth, 22);
			}
			
			this.addChild(this.allyBar);
			this.addChild(this.enemyBar);
		}
		
		public function setColorBlind(enabled:Boolean):void
		{
			this.enemyBar.updateColor(enabled ? this.colors.enemyColorBlind : this.colors.enemy);
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
		}
	}
}