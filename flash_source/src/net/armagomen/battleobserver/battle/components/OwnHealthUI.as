package net.armagomen.battleobserver.battle.components
{
	import flash.events.Event;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Constants;
	import net.armagomen.battleobserver.utils.ProgressBar;
	
	public class OwnHealthUI extends ObserverBattleDisplayable
	{
		private var own_health:ProgressBar;
		public var getAVGColor:Function;
		
		public function OwnHealthUI()
		{
			super();
		}
		
		override protected function onPopulate():void 
		{
			super.onPopulate();
			var settings:Object = this.getSettings();
			var colors:Object = this.getColors().global;
			var healthCenter:Number = settings.width / 2;
			this.own_health = new ProgressBar(settings.x - healthCenter, settings.y, settings.width, settings.height, null, this.getAVGColor(), colors.bgColor, 0.2);
			this.own_health.setOutline(settings.width, settings.height);
			this.own_health.addTextField(healthCenter, -2, "center", Constants.normalText);
			this.addChild(this.own_health);
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