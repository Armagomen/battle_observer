package net.armagomen.battleobserver.battle.components.wgcomponents
{
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class WGComponentsSetting extends ObserverBattleDispalaysble
	{
		
		public function WGComponentsSetting()
		{
			super();
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