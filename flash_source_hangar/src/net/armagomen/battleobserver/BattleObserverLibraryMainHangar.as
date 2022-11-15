package net.armagomen.battleobserver
{
	/**
	 * ...
	 * @author Armagomen
	 */
	import flash.display.MovieClip;
	import net.armagomen.battleobserver.hangar.AvgDataUI;
	import net.armagomen.battleobserver.hangar.ObserverDateTimesUI;
	import net.wg.gui.lobby.hangar.Hangar;

	public class BattleObserverLibraryMainHangar extends MovieClip
	{
		public function BattleObserverLibraryMainHangar()
		{
			super();
			Hangar.prototype.as_observerCreateComponents = function(aliases:Array):void
			{
				for each (var alias:String in aliases) 
				{
					switch (alias)
					{
					case "Observer_DateTimes_UI":
						this.registerFlashComponent(this.addChild(new ObserverDateTimesUI), alias);
						break;
					case "Observer_AvgData_UI":
						this.registerFlashComponent(this.addChild(new AvgDataUI), alias);
						break;
					}
				}
			}
		}
	}
}