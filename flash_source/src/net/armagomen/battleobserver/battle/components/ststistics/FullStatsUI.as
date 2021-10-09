package net.armagomen.battleobserver.battle.components.ststistics
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.text.TextFieldAutoSize;
	import flash.utils.setTimeout;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Utils;
	import net.wg.gui.battle.components.BattleAtlasSprite;
	
	public class FullStatsUI extends ObserverBattleDisplayable
	{
		private var fullStats:*               = null;
		public var py_getStatisticString:Function;
		public var py_getIconColor:Function;
		public var py_getIconMultiplier:Function;
		public var py_statisticEnabled:Function;
		public var py_iconEnabled:Function;
		private var cached:Object             = new Object();
		private var namesCache:Object         = new Object();
		private var statisticsEnabled:Boolean = false;
		private var iconEnabled:Boolean       = false;
		private var count:Number              = 0;
		
		public function FullStatsUI(fullStats:*)
		{
			this.fullStats = fullStats
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			this.statisticsEnabled = py_statisticEnabled();
			this.iconEnabled = py_iconEnabled();
			this.createCache();
		}
		
		override protected function onBeforeDispose():void
		{
			this.removeListeners();
			App.utils.data.cleanupDynamicObject(this.cached);
			super.onBeforeDispose();
		}
		
		private function timeout():void
		{
			this.count++;
			if (count < 100)
			{
				setTimeout(this.createCache, 100);
			}
		}
		
		private function createCache():void
		{
			if (!this.fullStats._tableCtrl || !this.fullStats._tableCtrl._allyRenderers)
			{
				this.timeout();
				return;
			}
			for each (var ally:* in this.fullStats._tableCtrl._allyRenderers)
			{
				if (!ally.data)
				{
					this.timeout();
					return;
				}
				this.cached[ally.data.vehicleID] = ally;
			}
			for each (var enemy:* in this.fullStats._tableCtrl._enemyRenderers)
			{
				if (!enemy.data)
				{
					this.timeout();
					return;
				}
				this.cached[enemy.data.vehicleID] = enemy;
			}
			this.addListeners();
		}
		
		private function addListeners():void
		{
			for each (var holder:* in this.cached)
			{
				var icon:BattleAtlasSprite = holder.statsItem.vehicleIcon;
				var tColor:ColorTransform  = icon.transform.colorTransform;
				tColor.color = Utils.colorConvert(py_getIconColor(holder.data.vehicleType));
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = py_getIconMultiplier();
				icon['cTansform'] = tColor;
				icon['vehicleID'] = holder.data.vehicleID;
				if (!icon.hasEventListener(Event.RENDER))
				{
					icon.addEventListener(Event.RENDER, this.onRenderHendle);
				}
				holder.statsItem._playerNameTF.autoSize = holder.statsItem._isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT;
			}
		}
		
		private function removeListeners():void
		{
			for each (var holder:* in this.cached)
			{
				if (!holder || !holder.statsItem || !holder.statsItem.vehicleIcon)
				{
					continue;
				}
				if (holder.statsItem.vehicleIcon.hasEventListener(Event.RENDER))
				{
					holder.statsItem.vehicleIcon.removeEventListener(Event.RENDER, this.onRenderHendle);
				}
			}
		}
		
		private function onRenderHendle(eve:Event):void
		{
			var icon:BattleAtlasSprite = eve.target as BattleAtlasSprite;
			if (this.iconEnabled)
			{
				icon.transform.colorTransform = icon['cTansform'];
			}
			if (this.statisticsEnabled)
			{
				this.setPlayerText(this.cached[icon['vehicleID']]);
			}
		
		}
		
		private function setPlayerText(holder:*):void
		{
			if (holder.data.accountDBID != 0)
			{
				if (!this.namesCache.hasOwnProperty(holder.data.accountDBID))
				{
					this.namesCache[holder.data.accountDBID] = py_getStatisticString(holder.data.accountDBID, holder.statsItem._isEnemy, holder.data.clanAbbrev);
				}
				if (this.namesCache[holder.data.accountDBID])
				{
					holder.statsItem._playerNameTF.htmlText = this.namesCache[holder.data.accountDBID];
					if (!holder.data.isAlive())
					{
						holder.statsItem._playerNameTF.alpha = 0.6;
					}
				}
			}
		}
	}
}