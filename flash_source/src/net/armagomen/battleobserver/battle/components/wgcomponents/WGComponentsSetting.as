package net.armagomen.battleobserver.battle.components.wgcomponents
{
	import flash.display.Sprite;
	import net.armagomen.battleobserver.battle.utils.Params;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.*;

	public class WGComponentsSetting extends BattleDisplayable
	{
		private var questview:Sprite = null;
		private var teamBases:Sprite = null;

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

		public function as_clearScene():void
		{
			var battlePage:* = parent;
			if (this.questview){
				var questTopView:* = battlePage.getComponent(BATTLE_VIEW_ALIASES.QUEST_PROGRESS_TOP_VIEW);
				if (questTopView)
				{
					battlePage.addChild(questTopView);
					this.questview.removeChildren();
				}
			}
			if (this.teamBases){
				var teamBasesPanel:* = battlePage.getComponent(BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL);
				if (teamBasesPanel)
				{
					battlePage.addChild(teamBasesPanel);
					this.teamBases.removeChildren();
				}
			}
			while (this.numChildren > 0){
				this.removeChildAt(0);
			}
			this.questview = null;
			this.teamBases = null;
			battlePage.unregisterComponent(this.name);
		}

		public function as_moveQuests(move:Boolean):void
		{
			var battlePage:* = parent;
			var questTopView:* = battlePage.getComponent(BATTLE_VIEW_ALIASES.QUEST_PROGRESS_TOP_VIEW);
			if (questTopView)
			{
				if (move)
				{
					this.questview = new Sprite();
					this.questview.y = 30;
					this.questview.addChild(questTopView);
					battlePage.addChildAt(this.questview, 0);
				}
				else
				{
					battlePage.setChildIndex(questTopView, 0);
				}
			}
		}

		public function as_hideShadowInPreBattle():void
		{
			var battlePage:* = parent;
			var prebattleTimer:* = battlePage.getComponent(BATTLE_VIEW_ALIASES.PREBATTLE_TIMER);
			if (prebattleTimer)
			{
				prebattleTimer.background.removeChild(prebattleTimer.background.shadow);
			}
		}

		public function as_hideMessenger():void
		{
			var battlePage:* = parent;
			var battleMessenger:* = battlePage.getComponent(BATTLE_VIEW_ALIASES.BATTLE_MESSENGER);
			if (battleMessenger)
			{
				battlePage.removeChild(battleMessenger);
			}
		}

		public function as_enableAnimation(enable:Boolean):void
		{
			Params.AnimationEnabled = enable;
		}
		
		public function as_moveTeamBasesPanel():void
		{
			var battlePage:* = parent;
			var teamBasesPanel:* = battlePage.getComponent(BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL);
			if (teamBasesPanel)
			{
				this.teamBases = new Sprite();
				battlePage.addChild(this.teamBases);
				this.teamBases.y = 30;
				this.teamBases.addChild(teamBasesPanel);
			}
		}

		//public function as_hideDeadTips():void
		//{
			//var battlePage:* = parent;
			//var postmotremPanel:* = battlePage.getComponent(BATTLE_VIEW_ALIASES.POSTMORTEM_PANEL);
			//if (postmotremPanel)
			//{
				//postmotremPanel.removeChild(postmotremPanel.vehiclePanel);
			//}
		//}
	}
}