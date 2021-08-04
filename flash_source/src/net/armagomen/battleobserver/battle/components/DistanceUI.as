package net.armagomen.battleobserver.battle.components
{
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class DistanceUI extends ObserverBattleDispalaysble
	{
		private var distance:TextExt;
		
		public function DistanceUI()
		{
			super();
		}
		
		public function as_startUpdate(flyght:Object):void
		{
			if (this.distance == null)
			{
				distance = new TextExt("distance", flyght.x, flyght.y, Filters.middleText, flyght.align, getShadowSettings(), this);
			}
		}
		
		public function as_setDistance(text:String):void
		{
			distance.htmlText = text;
		}
	}
}