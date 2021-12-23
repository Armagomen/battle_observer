package net.armagomen.battleobserver.battle.components
{
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.ProgressBar;
	
	public class OwnHealthUI extends ObserverBattleDisplayable
	{
		private var own_health:ProgressBar;
		
		public function OwnHealthUI()
		{
			super();
		}
		
		override protected function onPopulate():void 
		{
			super.onPopulate();
			if (!this.own_health)
			{
				var settings:Object = this.getSettings();
				var colors:Object = this.getColors();
				this.own_health = new ProgressBar(-settings.width / 2, settings.y, settings.width, settings.height, settings.alpha, settings.alpha * 0.7, null, colors.global.ally, null, 0.2);
				this.own_health.setOutline(false, colors.global.ally, settings.alpha, settings.width, settings.height);
				this.own_health.addTextField(settings.width / 2, -2, "center", Filters.normalText, this.getShadowSettings());
				this.addChild(this.own_health);
			}
		}
		
		override protected function onBeforeDispose():void 
		{
			super.onBeforeDispose();
			this.own_health.remove()
			this.own_health = null;
		}
		
		public function as_setOwnHealth(scale:Number, text:String, color:String):void
		{
			this.own_health.setNewScale(scale);
			this.own_health.setText(text);
			this.own_health.updateColor(color);
		}
	}
}