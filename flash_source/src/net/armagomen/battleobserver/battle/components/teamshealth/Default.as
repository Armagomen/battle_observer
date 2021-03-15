package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.display.*;
	import flash.geom.ColorTransform;
	import net.armagomen.battleobserver.data.Constants;
	import net.armagomen.battleobserver.utils.Params;
	import net.armagomen.battleobserver.utils.Utils;
	import net.armagomen.battleobserver.utils.ProgressBar;
	import fl.transitions.Tween;
	
	public class Default extends Sprite
	{
		
		private var allyHpBar:ProgressBar;
		private var enemyHpBar:ProgressBar;
		private var colors:Object;
		
		public function Default(settings:Object, barWidth:Number, colorBlind:Boolean, colors:Object)
		{
			super();
			this.colors = colors;
			
			this.allyHpBar = new ProgressBar(-50, 4, -barWidth, 22, Math.max(0.05, colors.alpha), Math.max(0.05, colors.bgAlpha), null, colors.ally, "allyBar");
			this.enemyHpBar = new ProgressBar(50, 4, barWidth, 22, Math.max(0.05, colors.alpha), Math.max(0.05, colors.bgAlpha), null, colorBlind ? colors.enemyColorBlind : colors.enemy, "enemyBar");
			
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
			Utils.updateColor(this.enemyHpBar, enabled ? this.colors.enemyColorBlind : this.colors.enemy);
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
	}
}