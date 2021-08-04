package net.armagomen.battleobserver.battle.components
{
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class OwnHealthUI extends ObserverBattleDispalaysble
	{
		private var own_health:TextExt;
		
		public function OwnHealthUI()
		{
			super();
		}
		
		public function as_startUpdate(data:Object):void
		{
			if (this.own_health == null)
			{
				own_health = new TextExt("own_health", data.x, data.y, Filters.middleText, data.align, this.getShadowSettings(), this);
			}
		}
		
		public function as_setOwnHealth(text:String):void
		{
			own_health.htmlText = text;
		}
	}
}