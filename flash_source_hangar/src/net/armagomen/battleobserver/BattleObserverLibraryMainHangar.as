package net.armagomen.battleobserver
{
	/**
	 * ...
	 * @author Armagomen
	 */
	import net.armagomen.battleobserver.hangar.ObserverDateTimesUI;
	import net.armagomen.battleobserver.hangar.ObserverEfficiencyUI;
	import net.wg.gui.lobby.LobbyPage;
	import net.wg.infrastructure.base.AbstractView;
	
	public class BattleObserverLibraryMainHangar extends AbstractView
	{
		public function BattleObserverLibraryMainHangar()
		{
			super();
			LobbyPage.prototype.as_BattleObserverCreate = function(aliases:Array):void
			{
				for each (var alias:String in aliases)
				{
					switch (alias)
					{
					case "Observer_DateTimes_UI": 
						this.registerFlashComponent(this.addChildAt(new ObserverDateTimesUI, 2), alias);
						break;
					case "Observer_Efficiency_UI": 
						this.registerFlashComponent(this.addChildAt(new ObserverEfficiencyUI, 0), alias);
						break;
					}
				}
			}
		}
	}
}