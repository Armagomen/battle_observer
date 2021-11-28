package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.display.*;
	import net.armagomen.battleobserver.utils.ProgressBar;
	import net.armagomen.battleobserver.utils.Utils;
	
	public class Default extends Sprite
	{
		
		private var allyHpBar:ProgressBar;
		private var enemyHpBar:ProgressBar;
		private var colors:Object;
		
		
		public function Default(settings:Object, barWidth:Number, colorBlind:Boolean, colors:Object)
		{
			super();
			this.colors = colors;
			
			this.allyHpBar = new ProgressBar(-50, 4, -barWidth, 22, Math.max(0.05, colors.alpha), Math.max(0.05, colors.bgAlpha), null, colors.ally);
			this.enemyHpBar = new ProgressBar(50, 4, barWidth, 22, Math.max(0.05, colors.alpha), Math.max(0.05, colors.bgAlpha), null, colorBlind ? colors.enemyColorBlind : colors.enemy);
			
			if (settings.outline.enabled)
			{
				this.allyHpBar.setOutline(true, settings.outline.color, Math.max(0.05, colors.bgAlpha));
				this.enemyHpBar.setOutline(true, settings.outline.color, Math.max(0.05, colors.bgAlpha));
			}
			
			this.addChild(this.allyHpBar);
			this.addChild(this.enemyHpBar);
		}
		
		public function setColorBlind(enabled:Boolean):void
		{	
			this.enemyHpBar.updateColor(enabled ? this.colors.enemyColorBlind : this.colors.enemy);
		}
		
		public function setBarScale(team:String, newScale:Number):void
		{
			if (team == "green")
			{
				this.allyHpBar.setNewScale(newScale);
			}
			else
			{
				this.enemyHpBar.setNewScale(newScale);
			}
		}
		
		public function remove():void
		{
			this.removeChildren();
			this.allyHpBar.remove();
			this.allyHpBar = null;
			this.enemyHpBar.remove();
			this.enemyHpBar = null;
		}
	}
}