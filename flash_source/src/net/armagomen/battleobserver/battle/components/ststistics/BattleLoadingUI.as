package net.armagomen.battleobserver.battle.components.ststistics
{
	import flash.events.Event;
	import flash.text.TextFieldAutoSize;
	import flash.utils.setTimeout;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.battle.components.ststistics.liasItem.BattleLoadingListItem;
	import net.armagomen.battleobserver.utils.Utils;
	
	public class BattleLoadingUI extends ObserverBattleDisplayable
	{
		private var loading:*;
		public var py_getStatisticString:Function;
		public var py_getIconColor:Function;
		public var py_getIconMultiplier:Function;
		public var py_statisticEnabled:Function;
		public var py_iconEnabled:Function;
		private var statisticsEnabled:Boolean = false;
		private var iconEnabled:Boolean       = false;
		private var count:Number              = 0;
		private var iconMultiplier:Number     = -1.25;
		private var listItems:Vector.<BattleLoadingListItem>;
		
		public function BattleLoadingUI(loading:*)
		{
			this.loading = loading;
			super();
		}
		
		override public function as_onAfterPopulate():void
		{
			super.as_onAfterPopulate();
			this.statisticsEnabled = py_statisticEnabled();
			this.iconEnabled = py_iconEnabled();
			this.iconMultiplier = py_getIconMultiplier();
			this.loading.addEventListener(Event.CHANGE, this.onChange);
			this.listItems = new Vector.<BattleLoadingListItem>();
			this.addListeners();
		}
		
		override protected function onBeforeDispose():void
		{
			this.as_clear();
			this.loading.removeEventListener(Event.CHANGE, this.onChange);
			this.listItems = null;
			super.onBeforeDispose();
		}
		
		public function as_clear():void
		{
			this.removeListeners();
			this.listItems.splice(0, this.listItems.length);
		}
		
		private function onChange(eve:Event):void
		{
			this.as_clear();
			this.listItems = new Vector.<BattleLoadingListItem>();
			this.addListeners();
		}
		
		private function timeout():void
		{
			this.count++;
			if (count < 100)
			{
				setTimeout(this.addListeners, 100);
			}
		}
		
		private function addListeners():void
		{
			if (!this.loading.form || !this.loading.form._allyRenderers)
			{
				this.timeout();
				return;
			}
			for each (var ally:* in this.loading.form._allyRenderers)
			{
				this.addItemListener(ally)
			}
			for each (var enemy:* in this.loading.form._enemyRenderers)
			{
				this.addItemListener(enemy)
			}
		}
		
		private function addItemListener(item:*):void
		{
			if (!item.model)
			{
				setTimeout(this.addItemListener, 100, item);
			}
			else
			{
				var statistic:Boolean = this.statisticsEnabled && item.model.accountDBID != 0;
				var listItem:BattleLoadingListItem = new BattleLoadingListItem(item, statistic, this.iconEnabled, false, Utils.colorConvert(py_getIconColor(item.model.vehicleType)), this.iconMultiplier);
				this.listItems.push(listItem)
				if (statistic)
				{
					listItem.setStatisticStrings(py_getStatisticString(item.model.accountDBID, item._isEnemy, item.model.clanAbbrev));
					item._textField.autoSize = item._isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT;
				}
				listItem.addListener();
			}
		}
		
		private function removeListeners():void
		{
			for each (var listItem:BattleLoadingListItem in this.listItems)
			{
				listItem.removeListener();
			}
		}
	
	}
}