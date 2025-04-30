package net.armagomen.battle_observer.battle.components
{
	import flash.events.Event;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.ProgressBar;
	
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
			
			if (not_initialized)
			{
				super.onPopulate();
				this.onResizeHandle(null);
				var settings:Object = this.getSettings();
				var colors:Object = this.getColors().global;
				this.own_health = new ProgressBar(settings.x - 90, settings.y, 180, 22, this.getAVGColor(), colors.bgColor, 0.2);
				this.own_health.setOutline(180, 22);
				this.own_health.addTextField(90, -3, TextFieldAutoSize.CENTER, Constants.middleText);
				this.addChild(this.own_health);
			}
			else
			{
				super.onPopulate();
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
		
		public function as_BarVisible(vis:Boolean):void
		{
			this.own_health.visible = vis;
		}
		
		override public function onResizeHandle(event:Event):void 
		{
			this.x = App.appWidth >> 1;
			this.y = App.appHeight >> 1;
		}
	}
}