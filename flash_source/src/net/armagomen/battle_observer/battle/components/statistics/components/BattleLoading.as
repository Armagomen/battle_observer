package net.armagomen.battle_observer.battle.components.statistics.components
{
	/**
	 * ...
	 * @author Armagomen
	 */
	import net.armagomen.battle_observer.battle.components.statistics.components.base.BaseStatisticsComponent;
	import net.armagomen.battle_observer.utils.Utils;
	import net.wg.data.constants.generated.BATTLEATLAS;
	
	public class BattleLoading extends BaseStatisticsComponent
	{
		
		public function BattleLoading(component:*)
		{
			super(component);
		}
		
		public function updateBattleloading():void
		{
			if (this.component && this.component.form)
			{
				if (this.component.form._enemyRenderers)
				{
					for each (var enemy:* in this.component.form._enemyRenderers)
					{
						this.updateBattleloadingItem(enemy);
					}
				}
				if (this.component.form._allyRenderers)
				{
					for each (var ally:* in this.component.form._allyRenderers)
					{
						this.updateBattleloadingItem(ally);
					}
				}
			}
		}
		
		private function updateBattleloadingItem(holder:*):void
		{
			if (holder.model)
			{
				var vehicleID:int = holder.model.vehicleID;
				if (this.iconsEnabled && holder.model.vehicleType != BATTLEATLAS.UNKNOWN)
				{
					this.updateVehicleIconColor(holder._vehicleIcon, holder.model.vehicleType);
				}
				if (this.statisticsData[vehicleID])
				{
					if (this.statisticsData[vehicleID].fullName)
					{
						holder._textField.htmlText = this.statisticsData[vehicleID].fullName;
					}
					if (this.statisticsData[vehicleID].vehicleTextColor)
					{
						holder._vehicleField.textColor = Utils.colorConvert(this.statisticsData[vehicleID].vehicleTextColor);
					}
				}
			}
		}
	}
}