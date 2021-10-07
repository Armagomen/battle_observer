package net.armagomen.battleobserver.battle.components.ststistics
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.text.TextField;
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
		private var cached:Object             = new Object;
		private var statisticsEnabled:Boolean = false;
		private var iconEnabled:Boolean       = false;
		
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
		}
		
		override protected function onDispose():void
		{
			this.removeListeners();
			App.utils.data.cleanupDynamicObject(this.cached);
			super.onDispose();
		}
		
		private function timeout():void
		{
			setTimeout(this.createCache, 100);
		}
		
		private function createCache():void
		{
			if (this.loading.form)
			{
				for each (var ally:* in this.loading.form._allyRenderers)
				{
					if (!ally.model){
						this.timeout();
						return;
					}
					this.cached[ally.model.vehicleID] = ally;
				}
				for each (var enemy:* in this.loading.form._enemyRenderers)
				{
					if (!enemy.model){
						this.timeout();
						return;
					}
					this.cached[enemy.model.vehicleID] = enemy;
				}
				this.addListeners();
			}
			else
			{
				this.timeout();
			}
		}
		
		private function addListeners():void
		{
			for each (var holder:* in this.cached)
			{
				var icon:BattleAtlasSprite = holder._vehicleIcon;
				icon['battleObserver_color'] = Utils.colorConvert(py_getIconColor(holder.model.vehicleID));
				icon['battleObserver_multiplier'] = py_getIconMultiplier();
				icon['battleObserver_vehicleID'] = holder.model.vehicleID;
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
				this.setVehicleIconColor(icon);
			}
			if (this.statisticsEnabled)
			{
				this.setPlayerText(this.cached[icon['battleObserver_vehicleID']]);
			}
		}
		
		private function setVehicleIconColor(icon:BattleAtlasSprite):void
		{
			var tColor:ColorTransform = icon.transform.colorTransform;
			tColor.color = icon['battleObserver_color'];
			tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = icon['battleObserver_multiplier'];
			icon.transform.colorTransform = tColor;
		}
		
		private function setPlayerText(holder:*):void
		{
			if (holder.model.accountDBID != 0)
			{
				
				var playerNameHtml:String = py_getStatisticString(holder.model.accountDBID, holder._isEnemy, holder.model.vehicleID);
				if (playerNameHtml){
					holder._textField.htmlText = playerNameHtml;
					if (!holder.model.isAlive())
					{
						holder._textField.alpha = 0.6;
					}
				}
			}
		}
	}
}