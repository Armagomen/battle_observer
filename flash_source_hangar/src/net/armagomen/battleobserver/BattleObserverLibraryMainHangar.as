package net.armagomen.battleobserver
{
	/**
	 * ...
	 * @author Armagomen
	 */
	import flash.display.MovieClip;
	import net.armagomen.battleobserver.hangar.ObserverDateTimesUI;
	import net.wg.gui.lobby.hangar.Hangar;

	public class BattleObserverLibraryMainHangar extends MovieClip
	{
		public function BattleObserverLibraryMainHangar()
		{
			super();
			Hangar.prototype['as_createBattleObserverComp'] = function(ui_name:String):void
			{
				switch (ui_name)
				{
				case "Observer_DateTimes_UI":
					if (!this.isFlashComponentRegisteredS(ui_name))
					{
						this.registerFlashComponent(this.addChild(new ObserverDateTimesUI), ui_name);
					}
					break;
				}
			}
		}
	}
}