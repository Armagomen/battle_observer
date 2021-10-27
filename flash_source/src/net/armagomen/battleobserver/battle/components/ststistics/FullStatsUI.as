package net.armagomen.battleobserver.battle.components.ststistics
{
	import flash.text.TextFieldAutoSize;
	import flash.utils.setTimeout;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.battle.components.ststistics.liasItem.FullStatsListItem;
	import net.armagomen.battleobserver.utils.Utils;
	import net.wg.infrastructure.events.ListDataProviderEvent;
	
	ListDataProviderEvent.UPDATE_ITEM
	
	public class FullStatsUI extends ObserverBattleDisplayable
	{
		private var fullStats:*               = null;
		public var py_getStatisticString:Function;
		public var py_getIconColor:Function;
		public var py_getIconMultiplier:Function;
		public var py_statisticEnabled:Function;
		public var py_iconEnabled:Function;
		private var statisticsEnabled:Boolean = false;
		private var iconEnabled:Boolean       = false;
		private var count:Number              = 0;
		private var iconMultiplier:Number     = -1.25;
		private var listItems:Vector.<FullStatsListItem>;
		
		public function FullStatsUI(fullStats:*)
		{
			this.fullStats = fullStats
			super();
		}
		
		override public function as_onAfterPopulate():void
		{
			super.as_onAfterPopulate();
			this.statisticsEnabled = py_statisticEnabled();
			this.iconEnabled = py_iconEnabled();
			this.iconMultiplier = py_getIconMultiplier();
			this.listItems = new Vector.<FullStatsListItem>();
			this.addListeners();
		}
		
		override protected function onBeforeDispose():void
		{
			this.clear();
			this.listItems = null;
			super.onBeforeDispose();
		}
		
		private function clear():void
		{
			this.removeListeners();
			this.listItems.splice(0, this.listItems.length);
		}
		
		private function timeout():void
		{
			this.count++;
			if (count < 100)
			{
				setTimeout(this.addListeners, 2000);
			}
		}
		
		private function addListeners():void
		{
			if (!this.fullStats._tableCtrl || !this.fullStats._tableCtrl._allyRenderers)
			{
				this.timeout();
			}
			else
			{
				for each (var ally:* in this.fullStats._tableCtrl._allyRenderers)
				{
					this.addItemListener(ally)
				}
				for each (var enemy:* in this.fullStats._tableCtrl._enemyRenderers)
				{
					this.addItemListener(enemy)
				}
			}
		}
		
		private function addItemListener(item:*):void
		{
			if (!item.containsData || !item.statsItem)
			{
				setTimeout(this.addItemListener, 200, item);
			}
			else
			{
				var statistic:Boolean = this.statisticsEnabled && item.data.accountDBID != 0;
				var listItem:FullStatsListItem = new FullStatsListItem(item, statistic, this.iconEnabled, false, 
				                                                       Utils.colorConvert(py_getIconColor(item.data.vehicleType)), this.iconMultiplier);
				this.listItems.push(listItem);
				if (statistic)
				{
					listItem.setStatisticStrings(py_getStatisticString(item.data.accountDBID, item.statsItem._isEnemy, item.data.clanAbbrev));
					item.statsItem._playerNameTF.autoSize = item.statsItem._isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT;
				}
				listItem.addListener();
			}
		}
		
		private function removeListeners():void
		{
			for each (var listItem:FullStatsListItem in this.listItems)
			{
				listItem.removeListener();
			}
		}
		
	}
}