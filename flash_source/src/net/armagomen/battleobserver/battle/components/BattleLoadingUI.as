package net.armagomen.battleobserver.battle.components
{
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import flash.text.TextFieldAutoSize;
	import flash.text.TextField;
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
			var icon:BattleAtlasSprite = listitem._vehicleIcon;
			icon['battleObserver'] = {"color": Utils.colorConvert(py_getIconColor(listitem.model.vehicleID)), "multiplier": py_getIconMultiplier()};
			if (!icon.hasEventListener(Event.RENDER))
			{
				icon.addEventListener(Event.RENDER, this.onRenderHendle);
			}
		
		}
		
		public function as_showStats(statistics:Boolean, setIcon:Boolean):void
		{
			for each (var ally:* in this.loading.form._allyRenderers)
			{
				if (setIcon)
				{
					this.setVehicleIconColor(ally);
				}
				if (statistics)
				{
					this.setPlayerText(ally, false);
				}
				
			}
			for each (var enemy:* in this.loading.form._enemyRenderers)
			{
				if (setIcon)
				{
					this.setVehicleIconColor(enemy);
				}
				if (statistics)
				{
					this.setPlayerText(enemy, true);
				}
			}
		}
		
		private function setPlayerText(holder:*, isEnemy:Boolean):void
		{
			if (holder.model.accountDBID != 0){
				holder._textField.autoSize = isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT;
				holder._textField.htmlText = py_getStatisticString(holder.model.accountDBID, isEnemy);
			}
		}
	
	}

}