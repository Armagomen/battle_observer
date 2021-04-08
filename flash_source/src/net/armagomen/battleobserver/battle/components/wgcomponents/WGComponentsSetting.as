package net.armagomen.battleobserver.battle.components.wgcomponents
{
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.*;
	
	
	public class WGComponentsSetting extends BattleDisplayable
	{
		
		public function WGComponentsSetting(compName:String)
		{
			super();
			this.name = compName;
		}
		
		override protected function configUI():void
		{
			super.configUI();
			this.tabEnabled = false;
			this.tabChildren = false;
			this.mouseEnabled = false;
			this.mouseChildren = false;
			this.buttonMode = false;
		}
			
		public function as_hideShadowInPreBattle():void
		{
			var battlePage:*     = parent;
			var prebattleTimer:* = battlePage.getComponent(BATTLE_VIEW_ALIASES.PREBATTLE_TIMER);
			if (prebattleTimer)
			{
				prebattleTimer.background.removeChild(prebattleTimer.background.shadow);
			}
		}
		
		public function as_hideMessenger():void
		{
			var battlePage:*      = parent;
			var battleMessenger:* = battlePage.getComponent(BATTLE_VIEW_ALIASES.BATTLE_MESSENGER);
			if (battleMessenger)
			{
				battlePage.removeChild(battleMessenger);
			}
		}
	}
}