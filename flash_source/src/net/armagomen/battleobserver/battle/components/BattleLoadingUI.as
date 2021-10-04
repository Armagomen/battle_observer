package net.armagomen.battleobserver.battle.components
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.utils.Utils;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.wg.gui.battle.components.BattleAtlasSprite;

	public class BattleLoadingUI extends ObserverBattleDispalaysble
	{
		private var loading:*;
		public var py_getStatisticString:Function;
		public var py_getIconColor:Function;
		public var py_getIconMultiplier:Function;
		
		
		public function BattleLoadingUI(loading:*)
		{
			this.loading = loading;
			super();
		
		}
		
		private function onRenderHendle(eve:Event):void
		{
			var icon:BattleAtlasSprite = eve.target as BattleAtlasSprite;
			var tColor:ColorTransform  = icon.transform.colorTransform;
			tColor.color = icon['battleObserver']['color'];
			tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = icon['battleObserver']['multiplier'];
			icon.transform.colorTransform = tColor;
		}
		
		private function setVehicleIconColor(listitem:*):void
		{
			var color:String = py_getIconColor(listitem.model.vehicleID);
			var multiplier:Number = py_getIconMultiplier();
			var icon:BattleAtlasSprite = listitem._vehicleIcon;
			icon['battleObserver'] = {"color": Utils.colorConvert(color), "multiplier": multiplier};
			if (!icon.hasEventListener(Event.RENDER))
			{
				icon.addEventListener(Event.RENDER, this.onRenderHendle);
			}

		}
		
		public function afterPopulate():void
		{
			for each (var ally:* in this.loading.form._allyRenderers)
			{
				this.setVehicleIconColor(ally);
				ally._textField.autoSize = TextFieldAutoSize.LEFT;
				if (ally.model.accountDBID != 0)
				{
					ally._textField.htmlText = this.py_getStatisticString(ally.model.accountDBID, false);
				}
			}
			for each (var enemy:* in this.loading.form._enemyRenderers)
			{
				this.setVehicleIconColor(enemy);
				enemy._textField.autoSize = TextFieldAutoSize.RIGHT;
				if (enemy.model.accountDBID != 0)
				{
					enemy._textField.htmlText = this.py_getStatisticString(enemy.model.accountDBID, true);
				}
			}
		}
	
	}

}