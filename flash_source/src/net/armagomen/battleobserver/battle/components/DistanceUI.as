package net.armagomen.battleobserver.battle.components
{
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Constants;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class DistanceUI extends ObserverBattleDisplayable
	{
		private var distance:TextExt;
		
		public function DistanceUI()
		{
			super();
		}
		
		override protected function onPopulate():void 
		{
			super.onPopulate();
			var settings:Object = this.getSettings();
			this.distance = new TextExt(settings.x, settings.y, Constants.middleText, settings.align, this);
		}
		
		override protected function onBeforeDispose():void 
		{
			super.onBeforeDispose();
			this.distance = null;
		}
		
		public function as_setDistance(text:String):void
		{
			this.distance.htmlText = text;
		}
	}
}