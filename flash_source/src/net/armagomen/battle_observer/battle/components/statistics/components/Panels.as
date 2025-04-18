package net.armagomen.battle_observer.battle.components.statistics.components
{
	/**
	 * ...
	 * @author Armagomen
	 */
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.utils.setTimeout;
	import net.armagomen.battle_observer.battle.components.statistics.components.base.BaseStatisticsComponent;
	import net.armagomen.battle_observer.utils.Utils;
	import net.wg.data.constants.generated.BATTLEATLAS;
	import net.wg.gui.battle.components.events.PlayersPanelListEvent;
	import net.wg.gui.battle.random.views.stats.components.playersPanel.events.PlayersPanelEvent;
	
	public class Panels extends BaseStatisticsComponent
	{
		
		public function Panels(component:*)
		{
			super(component);
		}
		
		public function addEventListeners():void
		{
			this.component.addEventListener(Event.CHANGE, this.onChange, false, 0, true);
			this.component.addEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.onChange, false, 0, true);
			this.component.listLeft.addEventListener(MouseEvent.ROLL_OVER, this.onChange, false, 0, true);
			this.component.listLeft.addEventListener(MouseEvent.ROLL_OUT, this.onChange, false, 0, true);
			this.component.listRight.addEventListener(MouseEvent.ROLL_OVER, this.onChange, false, 0, true);
			this.component.listRight.addEventListener(MouseEvent.ROLL_OUT, this.onChange, false, 0, true);
			this.component.listRight.addEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE, this.onChange, false, 0, true);
		}
		
		public function removeEventListeners():void
		{
			if (this.component.hasEventListener(Event.CHANGE))
			{
				this.component.removeEventListener(Event.CHANGE, this.onChange);
			}
			if (this.component.hasEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE))
			{
				this.component.removeEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.onChange);
			}
			if (this.component.listLeft && this.component.listLeft.hasEventListener(MouseEvent.ROLL_OVER))
			{
				this.component.listLeft.removeEventListener(MouseEvent.ROLL_OVER, this.onChange);
			}
			if (this.component.listLeft && this.component.listLeft.hasEventListener(MouseEvent.ROLL_OUT))
			{
				this.component.listLeft.removeEventListener(MouseEvent.ROLL_OUT, this.onChange);
			}
			if (this.component.listRight && this.component.listRight.hasEventListener(MouseEvent.ROLL_OVER))
			{
				this.component.listRight.removeEventListener(MouseEvent.ROLL_OVER, this.onChange);
			}
			if (this.component.listRight && this.component.listRight.hasEventListener(MouseEvent.ROLL_OUT))
			{
				this.component.listRight.removeEventListener(MouseEvent.ROLL_OUT, this.onChange);
			}
			if (this.component.listRight && this.component.listRight.hasEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE))
			{
				this.component.listRight.removeEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE, this.onChange);
			}
		}
		
		private function updatePlayersPanelItem(holder:*):void
		{
			if (holder.vehicleData)
			{
				var vehicleID:int = holder.vehicleData.vehicleID;
				var listItem:*    = holder.getListItem();
				if (this.iconsEnabled && holder.vehicleData.vehicleType != BATTLEATLAS.UNKNOWN)
				{
					this.updateVehicleIconColor(listItem.vehicleIcon, holder.vehicleData.vehicleType);
				}
				listItem.setPlayerNameFullWidth(this.fullWidth);
				if (listItem.playerNameCutTF.width != this.cutWidth)
				{
					listItem.playerNameCutTF.width = this.cutWidth
				}
				if (this.statisticsData[vehicleID])
				{
					if (this.statisticsData[vehicleID].vehicleTextColor)
					{
						listItem.vehicleTF.textColor = Utils.colorConvert(this.statisticsData[vehicleID].vehicleTextColor);
						listItem.vehicleTF.setTextFormat(this.format);
					}
					if (this.statisticsData[vehicleID].fullName)
					{
						listItem.playerNameFullTF.htmlText = this.statisticsData[vehicleID].fullName;
					}
					if (this.statisticsData[vehicleID].cutName)
					{
						listItem.playerNameCutTF.htmlText = this.statisticsData[vehicleID].cutName;
					}
					if (!listItem._isAlive)
					{
						listItem.playerNameCutTF.alpha = DEAD_TEXT_ALPHA;
						listItem.playerNameFullTF.alpha = DEAD_TEXT_ALPHA;
						listItem.vehicleTF.alpha = DEAD_TEXT_ALPHA;
					}
				}
			}
		}
		
		public function updatePlayersPanel():void
		{
			this.removeTimeout();
			if (this.component)
			{
				for each (var itemL:* in this.component.listLeft._items)
				{
					this.updatePlayersPanelItem(itemL);
				}
				for each (var itemR:* in this.component.listRight._items)
				{
					this.updatePlayersPanelItem(itemR);
				}
			}
		}
		
		private function onChange(eve:Event):void
		{
			this.removeTimeout();
			this.timeoutID = setTimeout(this.updatePlayersPanel, 100);
		}
	}
}