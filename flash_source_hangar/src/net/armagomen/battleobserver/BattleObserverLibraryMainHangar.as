package net.armagomen.battleobserver
{
	/**
	 * ...
	 * @author Armagomen
	 */
	import flash.filters.GlowFilter;
	import net.armagomen.battleobserver.hangar.ObserverDateTimesUI;
	import net.wg.gui.lobby.hangar.Hangar;
	import net.wg.infrastructure.base.AbstractView;
	
	public class BattleObserverLibraryMainHangar extends AbstractView
	{
		public function BattleObserverLibraryMainHangar()
		{
			super();
			Hangar.prototype.as_BattleObserverCreate = function(aliases:Array):void
			{
				for each (var alias:String in aliases)
				{
					switch (alias)
					{
					case "Observer_DateTimes_UI": 
						this.registerFlashComponent(this.addChild(new ObserverDateTimesUI), alias);
						break;
					}
				}
			}
			Hangar.prototype.as_BattleObserverShadow = function():void
			{
				var filter:GlowFilter = new GlowFilter(0, 0.5, 2, 2, 4);
				this.ammunitionPanel.vehicleStatus.message.textField.filters = [filter];
				this.ammunitionPanel.vehicleStatus.roleMessage.textField.filters = [filter];
			}
		}
	}
}