package net.armagomen.battleobserver
{
	/**
	 * ...
	 * @author Armagomen
	 */
	import flash.filters.GlowFilter;
	import flash.utils.setTimeout;
	import net.armagomen.battleobserver.hangar.ObserverDateTimesUI;
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
						this.registerFlashComponent(this.addChild(new ObserverDateTimesUI), alias);
						break;
					}
				}
			}
		}
	}
}