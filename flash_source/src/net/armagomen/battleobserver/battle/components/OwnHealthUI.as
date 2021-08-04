package net.armagomen.battleobserver.battle.components
{
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class OwnHealthUI extends ObserverBattleDispalaysble
	{
		private var own_health:TextExt;
		public var getShadowSettings:Function;
		private var loaded:Boolean = false;
		
		public function OwnHealthUI()
		{
			super();
		}
		
		public function as_startUpdate(data:Object):void
		{
			if (this.loaded) return;
			own_health = new TextExt("own_health", data.x, data.y, Filters.middleText, data.align, getShadowSettings(), this);
			App.utils.data.cleanupDynamicObject(data);
			this.loaded = true;
		}
		
		public function as_setOwnHealth(text:String):void
		{
			own_health.htmlText = text;
		}
		
		public function as_onCrosshairPositionChanged(x:Number, y:Number):void
		{
			this.x = x;
			this.y = y;
		}
	}
}