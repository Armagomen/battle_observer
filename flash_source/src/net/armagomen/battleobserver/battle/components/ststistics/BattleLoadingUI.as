package net.armagomen.battleobserver.battle.components.ststistics
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.text.TextFieldAutoSize;
	import flash.utils.setTimeout;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Utils;
	
	public class BattleLoadingUI extends ObserverBattleDisplayable
	{
		private var loading:*;
		public var py_getStatisticString:Function;
		public var py_getIconColor:Function;
		public var py_getIconMultiplier:Function;
		private var namesCache:Object         = new Object();
		private var iconsColors:Object        = new Object();
		private var statisticsEnabled:Boolean = false;
		private var iconEnabled:Boolean       = false;
		private var iconMultiplier:Number     = -1.25;
		
		public function BattleLoadingUI(loading:*, statsEnabled:Boolean, iconEnabled:Boolean)
		{
			this.loading = loading;
			this.statisticsEnabled = statsEnabled;
			this.iconEnabled = iconEnabled;
			super();
		}
		
		override public function as_onAfterPopulate():void
		{
			this.iconMultiplier = py_getIconMultiplier();
			this.loading.addEventListener(Event.CHANGE, this.onChange);
			setTimeout(this.addListeners, 1000);
		}
		
		override protected function onBeforeDispose():void
		{
			this.as_clear();
			this.loading.removeEventListener(Event.CHANGE, this.onChange);
			this.namesCache = null;
			this.iconsColors = null;
			super.onBeforeDispose();
		}
		
		public function as_clear():void
		{
			this.removeListeners();
			if (App.instance && App.utils)
			{
				App.utils.data.cleanupDynamicObject(this.namesCache);
				App.utils.data.cleanupDynamicObject(this.iconsColors);
			}
		}
		
		private function onChange(eve:Event):void
		{
			this.as_clear();
			this.addListeners();
		}
		
		private function addListeners():void
		{
			if (!this.loading.form || !this.loading.form._allyRenderers)
			{
				setTimeout(this.addListeners, 1000);
			}
			else
			{
				for each (var ally:* in this.loading.form._allyRenderers)
				{
					this.addItemListener(ally)
				}
				for each (var enemy:* in this.loading.form._enemyRenderers)
				{
					this.addItemListener(enemy)
				}
			}
		}
		
		private function addItemListener(item:*):void
		{
			if (!item.model || !item.model.vehicleType)
			{
				setTimeout(this.addItemListener, 200, item);
			}
			else
			{
				if (this.iconEnabled)
				{
					var typeColor:String = py_getIconColor(item.model.vehicleType);
					if (!this.iconsColors[item.model.vehicleType] && typeColor)
					{
						this.iconsColors[item.model.vehicleType] = Utils.colorConvert(typeColor);
					}
				}
				var icon:* = item._vehicleIcon;
				icon.item = item;
				if (!icon.hasEventListener(Event.RENDER))
				{
					icon.addEventListener(Event.RENDER, this.onRenderHendle, false, 0, true);
				}
				if (this.statisticsEnabled)
				{
					if (item.model.accountDBID != 0)
					{
						this.namesCache[item.model.accountDBID] = py_getStatisticString(item.model.accountDBID, item._isEnemy, item.model.clanAbbrev);
					}
					item._textField.autoSize = item._isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT;
				}
			}
		}
		
		private function removeListeners():void
		{
			if (!this.loading.form)
			{
				return;
			}
			for each (var ally:* in this.loading.form._allyRenderers)
			{
				this.removeListener(ally)
			}
			for each (var enemy:* in this.loading.form._enemyRenderers)
			{
				this.removeListener(enemy)
			}
		}
		
		private function removeListener(item:*):void
		{
			if (!item || !item._vehicleIcon)
			{
				return;
			}
			if (item._vehicleIcon.hasEventListener(Event.RENDER))
			{
				item._vehicleIcon.removeEventListener(Event.RENDER, this.onRenderHendle);
			}
		}
		
		private function onRenderHendle(eve:Event):void
		{
			var icon:* = eve.target;
			if (this.iconEnabled)
			{
				var iconColor:uint    = icon.transform.colorTransform.color;
				var newIconColor:uint = this.iconsColors[icon.item.model.vehicleType];
				if (iconColor != newIconColor || iconColor == 0)
				{
					var tColor:ColorTransform = new ColorTransform();
					tColor.color = newIconColor;
					tColor.alphaMultiplier = icon.transform.colorTransform.alphaMultiplier;
					tColor.alphaOffset = icon.transform.colorTransform.alphaOffset;
					tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
					icon.transform.colorTransform = tColor;
				}
			}
			if (this.statisticsEnabled && icon.item.model.accountDBID != 0)
			{
				this.setPlayerText(icon.item);
			}
		}
		
		private function setPlayerText(item:*):void
		{
			item._textField.htmlText = this.namesCache[item.model.accountDBID];
		}
	}
}