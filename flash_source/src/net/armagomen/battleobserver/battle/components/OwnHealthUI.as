package net.armagomen.battleobserver.battle.components
{
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.ProgressBar;
	
	public class OwnHealthUI extends ObserverBattleDispalaysble
	{
		private var own_health:ProgressBar;
		
		public function OwnHealthUI()
		{
			super();
		}
		
		public function as_startUpdate(data:Object):void
		{
			if (this.own_health == null)
			{
				var colors:Object = getColors();
				this.own_health = new ProgressBar(animationEnabled(), data.x - 70, data.y, 140, 20, Math.max(0.05, colors.global.alpha), Math.max(0.05, colors.global.bgAlpha), null, colors.global.ally, null, 0.4);
				this.own_health.setOutline(false, colors.global.ally, Math.max(0.05, colors.global.alpha));
				this.own_health.addTextField(70, -2, "center", Filters.normalText, getShadowSettings());
				this.own_health.setVisible(false);
				this.addChild(this.own_health);
			}
		}
		
		public function as_setOwnHealth(scale:Number, text:String, color:String):void
		{
			this.own_health.setNewScale(scale);
			this.own_health.setText(text);
			this.own_health.updateColor(color);
		}
		
		public function as_setVisible(param:Boolean):void
		{
			this.own_health.setVisible(param);
		}
	}
}