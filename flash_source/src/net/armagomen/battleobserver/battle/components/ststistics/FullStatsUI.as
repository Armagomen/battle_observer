package net.armagomen.battleobserver.battle.components.ststistics
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.text.TextFieldAutoSize;
	import flash.utils.setTimeout;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Utils;
	
	public class FullStatsUI extends ObserverBattleDisplayable
	{
		private var fullStats:*               = null;
		public var py_getStatisticString:Function;
		public var py_getIconColor:Function;
		public var py_getIconMultiplier:Function;
		public var py_statisticEnabled:Function;
		public var py_iconEnabled:Function;
		private var namesCache:Object         = new Object();
		private var statisticsEnabled:Boolean = false;
		private var iconEnabled:Boolean       = false;
		private var count:Number              = 0;
		private var iconColors:Object         = new Object();
		private var iconMultiplier:Number     = -1.25;
		
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
			this.addListeners();
		}
		
		override protected function onBeforeDispose():void
		{
			this.removeListeners();
			super.onBeforeDispose();
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
				var icon:* = item.statsItem._vehicleIcon;
				if (!this.iconColors[item.data.vehicleType])
				{
					this.iconColors[item.data.vehicleType] = Utils.colorConvert(py_getIconColor(item.data.vehicleType));
				}
				icon.item = item;
				if (!icon.hasEventListener(Event.RENDER))
				{
					icon.addEventListener(Event.RENDER, this.onRenderHendle);
				}
				if (this.statisticsEnabled)
				{
					if (item.data.accountDBID != 0)
					{
						this.namesCache[item.data.accountDBID] = py_getStatisticString(item.data.accountDBID, item.statsItem._isEnemy, item.data.clanAbbrev);
					}
					item.statsItem._playerNameTF.autoSize = item.statsItem._isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT;
				}
			}
		}
		
		private function removeListeners():void
		{
			if (!this.fullStats._tableCtrl || !this.fullStats._tableCtrl._allyRenderers)
			{
				return;
			}
			for each (var ally:* in this.fullStats._tableCtrl._allyRenderers)
			{
				this.removeListener(ally)
			}
			for each (var enemy:* in this.fullStats._tableCtrl._enemyRenderers)
			{
				this.removeListener(enemy)
			}
		}
		
		private function removeListener(item:*):void
		{
			if (!item || !item.statsItem || !item.statsItem._vehicleIcon)
			{
				return;
			}
			if (item.statsItem._vehicleIcon.hasEventListener(Event.RENDER))
			{
				item.statsItem._vehicleIcon.removeEventListener(Event.RENDER, this.onRenderHendle);
			}
		}
		
		private function onRenderHendle(eve:Event):void
		{
			var icon:* = eve.target;
			if (this.iconEnabled && icon.transform.colorTransform.color != this.iconColors[icon.item.data.vehicleType])
			{
				var tColor:ColorTransform = new ColorTransform();
				tColor.color = this.iconColors[icon.item.data.vehicleType];
				tColor.alphaMultiplier = icon.transform.colorTransform.alphaMultiplier;
				tColor.alphaOffset = icon.transform.colorTransform.alphaOffset;
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
				icon.transform.colorTransform = tColor;
			}
			if (this.statisticsEnabled && icon.item.data.accountDBID != 0)
			{
				this.setPlayerText(icon.item);
			}
		}
		
		private function setPlayerText(item:*):void
		{
			item.statsItem._playerNameTF.htmlText = this.namesCache[item.data.accountDBID];
			if (!item.data.isAlive())
			{
				item.statsItem._playerNameTF.alpha = 0.66;
			}
		}
	}
}