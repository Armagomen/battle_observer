package net.armagomen.battleobserver.battle.components.ststistics
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.text.TextFieldAutoSize;
	import flash.utils.setTimeout;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Utils;
	import net.wg.gui.battle.components.BattleAtlasSprite;
	
	public class BattleLoadingUI extends ObserverBattleDisplayable
	{
		private var loading:*;
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
		
		public function BattleLoadingUI(loading:*)
		{
			this.loading = loading;
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			this.statisticsEnabled = py_statisticEnabled();
			this.iconEnabled = py_iconEnabled();
			this.createCache();
			this.loading.addEventListener(Event.CHANGE, this.onChange);
		}
		
		override protected function onBeforeDispose():void
		{
			this.as_clear();
			this.loading.removeEventListener(Event.CHANGE, this.onChange);
			super.onBeforeDispose();
		}
		
		public function as_clear():void
		{
			this.removeListeners();
			App.utils.data.cleanupDynamicObject(this.cached);
			App.utils.data.cleanupDynamicObject(this.namesCache);
		}
		
		private function onChange(eve:Event):void
		{
			this.as_clear();
			this.createCache();
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
			if (!this.loading.form)
			{
				this.timeout();
				return;
			}
			for each (var ally:* in this.loading.form._allyRenderers)
			{
				if (!ally.model)
				{
					this.timeout();
					return;
				}
				this.cached[ally.model.vehicleID] = ally;
			}
			for each (var enemy:* in this.loading.form._enemyRenderers)
			{
				if (!enemy.model)
				{
					this.timeout();
					return;
				}
				this.cached[enemy.model.vehicleID] = enemy;
			}
			this.addListeners();
		}
		
		private function addListeners():void
		{
			for each (var holder:* in this.cached)
			{
				var icon:BattleAtlasSprite = holder._vehicleIcon;
				var tColor:ColorTransform  = icon.transform.colorTransform;
				tColor.color = Utils.colorConvert(py_getIconColor(holder.model.vehicleType));
				tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = py_getIconMultiplier();
				icon['cTansform'] = tColor;
				icon['vehicleID'] = holder.model.vehicleID;
				if (!icon.hasEventListener(Event.RENDER))
				{
					icon.addEventListener(Event.RENDER, this.onRenderHendle);
				}
				holder._textField.autoSize = holder._isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT;
			}
		}
		
		private function removeListeners():void
		{
			for each (var holder:* in this.cached)
			{
				if (!holder || !holder._vehicleIcon)
				{
					continue;
				}
				if (holder._vehicleIcon.hasEventListener(Event.RENDER))
				{
					holder._vehicleIcon.removeEventListener(Event.RENDER, this.onRenderHendle);
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
			if (holder.model.accountDBID != 0)
			{
				if (!this.namesCache.hasOwnProperty(holder.model.accountDBID))
				{
					this.namesCache[holder.model.accountDBID] = py_getStatisticString(holder.model.accountDBID, holder._isEnemy, holder.model.clanAbbrev);
				}
				if (this.namesCache[holder.model.accountDBID])
				{
					holder._textField.htmlText = this.namesCache[holder.model.accountDBID];
					if (!holder.model.isAlive())
					{
						holder._textField.alpha = 0.6;
					}
				}
			}
		}
	}
}