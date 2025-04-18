package net.armagomen.battle_observer.battle.components.statistics.components
{
	/**
	 * ...
	 * @author Armagomen
	 */
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battle_observer.battle.components.statistics.components.base.BaseStatisticsComponent;
	import net.armagomen.battle_observer.utils.Utils;
	import net.wg.data.constants.generated.BATTLEATLAS;
	
	public class FullStats extends BaseStatisticsComponent
	{
		
		public function FullStats(component:*)
		{
			super(component);
		}
		
		public function updateFullStats():void
		{
			if (this.component && this.component.tableCtrl)
			{
				if (this.component.tableCtrl.allyRenderers)
				{
					for each (var ally:* in this.component.tableCtrl.allyRenderers)
					{
						this.updateFullStatsItem(ally, false);
					}
				}
				if (this.component.tableCtrl.enemyRenderers)
				{
					for each (var enemy:* in this.component.tableCtrl.enemyRenderers)
					{
						this.updateFullStatsItem(enemy, true);
					}
				}
			}
		}
		
		private function updateFullStatsItem(holder:*, isEnemy:Boolean):void
		{
			if (holder.data)
			{
				var vehicleID:int = holder.data.vehicleID;
				if (this.iconsEnabled && holder.data.vehicleType != BATTLEATLAS.UNKNOWN)
				{
					this.updateVehicleIconColor(holder.statsItem._vehicleIcon, holder.data.vehicleType);
				}
				if (this.statisticsData[vehicleID])
				{
					if (this.statisticsData[vehicleID].fullName)
					{
						holder.statsItem._playerNameTF.autoSize = isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT;
						holder.statsItem._playerNameTF.htmlText = this.statisticsData[vehicleID].fullName;
					}
					if (this.statisticsData[vehicleID].vehicleTextColor)
					{
						holder.statsItem._vehicleNameTF.textColor = Utils.colorConvert(this.statisticsData[vehicleID].vehicleTextColor);
					}
					if (!holder.data.isAlive())
					{
						holder.statsItem._playerNameTF.alpha = DEAD_TEXT_ALPHA;
						holder.statsItem._vehicleNameTF.alpha = DEAD_TEXT_ALPHA;
					}
				}
			}
		}
	
	}

}