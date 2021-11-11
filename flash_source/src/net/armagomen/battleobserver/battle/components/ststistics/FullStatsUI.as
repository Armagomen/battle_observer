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
		public var py_getStatisticString:Function;
		public var py_getIconColor:Function;
		public var py_getIconMultiplier:Function;
		private var fullStats:*               = null;
		private var namesCache:Object         = new Object();
		private var iconsColors:Object        = new Object();
		private var statisticsEnabled:Boolean = false;
		private var iconEnabled:Boolean       = false;
		private var count:Number              = 0;
		private var iconMultiplier:Number     = -1.25;
		
		public function FullStatsUI(fullStats:*, statsEnabled:Boolean, iconEnabled:Boolean)
		{
			this.fullStats = fullStats;
			this.statisticsEnabled = statsEnabled;
			this.iconEnabled = iconEnabled;
			super();
		}
		
		override public function as_onAfterPopulate():void
		{
			super.as_onAfterPopulate();
			this.iconMultiplier = py_getIconMultiplier();
			this.addListeners();
		}
		
		override protected function onBeforeDispose():void
		{
			this.removeListeners();
			if (App.instance && App.utils)
			{
				App.utils.data.cleanupDynamicObject(this.namesCache);
				App.utils.data.cleanupDynamicObject(this.iconsColors);
			}
			this.namesCache = null;
			this.iconsColors = null;
			super.onBeforeDispose();
		}
		
		private function timeout():void
		{
			this.count++;
			if (count < 100)
			{
				setTimeout(this.addListeners, 1000);
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
			if (!item.containsData || !item.statsItem || !item.data.vehicleType)
			{
				setTimeout(this.addItemListener, 200, item);
			}
			else
			{
				if (this.iconEnabled)
				{
					var typeColor:String = py_getIconColor(item.data.vehicleType);
					if (!this.iconsColors[item.data.vehicleType] && typeColor)
					{
						this.iconsColors[item.data.vehicleType] = Utils.colorConvert(typeColor);
					}
				}
				var icon:* = item.statsItem._vehicleIcon;
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

			if (this.iconEnabled)
			{
				var iconColor:uint = icon.transform.colorTransform.color;
				var newIconColor:uint = this.iconsColors[icon.item.data.vehicleType];
				if  (iconColor != newIconColor || iconColor == 0)
				{
					var tColor:ColorTransform = new ColorTransform();
					tColor.color = newIconColor;
					tColor.alphaMultiplier = icon.transform.colorTransform.alphaMultiplier;
					tColor.alphaOffset = icon.transform.colorTransform.alphaOffset;
					tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
					icon.transform.colorTransform = tColor;
				}
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