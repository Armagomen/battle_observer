package net.armagomen.battleobserver
{
	/**
	 * ...
	 * @author Armagomen
	 */
	import flash.display.*;
	import flash.events.*;
	import flash.utils.*;
	import net.armagomen.battleobserver.hangar.ObserverDateTimesUI;
	import net.wg.gui.lobby.LobbyPage;

	public class BattleObserverLibraryMainHangar extends MovieClip
	{
		public function BattleObserverLibraryMainHangar()
		{
			super();
			LobbyPage.prototype['as_createBattleObserverComp'] = function(ui_name:String):void
			{
				switch (ui_name)
				{
				case "Observer_DateTimes_UI":
					if (!this.isFlashComponentRegisteredS(ui_name))
					{
						this.registerFlashComponent(this.addChildAt(new ObserverDateTimesUI(ui_name), 0), ui_name);
					}
					break;
				}
			}
		}
	}
}