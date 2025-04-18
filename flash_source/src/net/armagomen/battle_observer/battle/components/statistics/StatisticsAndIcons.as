package net.armagomen.battle_observer.battle.components.statistics
{
	import flash.utils.clearTimeout;
	import flash.utils.setTimeout;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.battle.components.statistics.components.BattleLoading;
	import net.armagomen.battle_observer.battle.components.statistics.components.FullStats;
	import net.armagomen.battle_observer.battle.components.statistics.components.Panels;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class StatisticsAndIcons extends ObserverBattleDisplayable
	{
		private var battleLoading:BattleLoading = null;
		private var fullStats:FullStats         = null;
		private var panels:Panels               = null;
		private var timeoutID:Number            = 0;
		
		public function StatisticsAndIcons()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			var battlePage:*    = this.parent;
			var settings:Object = this.getSettings();
			var colors:Object   = this.getColors()["vehicle_types_colors"];
			
			this.panels = new Panels(battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL));
			this.panels.setIconColors(colors);
			this.panels.setSettings(settings);
			this.panels.addEventListeners();
			
			if (this.isComp7Battle())
			{
				this.fullStats = new FullStats(battlePage.getComponent(BATTLE_VIEW_ALIASES.FULL_STATS));
				this.fullStats.setIconColors(colors);
				this.fullStats.setSettings(settings);
			}
			else
			{
				this.battleLoading = new BattleLoading(battlePage.getComponent(BATTLE_VIEW_ALIASES.BATTLE_LOADING));
				this.battleLoading.setIconColors(colors);
				this.battleLoading.setSettings(settings);
			}
			this.updateALL();
		}
		
		override protected function onBeforeDispose():void
		{
			this.newTimeout(0);
			this.panels.removeEventListeners();
			this.panels.removeTimeout();
			this.battleLoading = null;
			this.fullStats = null;
			this.panels = null;
			super.onBeforeDispose();
		}
		
		public function as_update_wgr_data(statsData:Object):void
		{
			if (this.isComp7Battle())
			{
				this.fullStats.set_wgr_data(statsData);
			}
			else
			{
				this.battleLoading.set_wgr_data(statsData);
			}
			this.panels.set_wgr_data(statsData);
			
			App.utils.data.cleanupDynamicObject(statsData);
			this.updateALL();
		}
		
		public function as_updateAll(timeout:Number):void
		{
			this.newTimeout(setTimeout(this.updateALL, timeout));
		}
		
		public function as_updateFullStatsOnkey(timeout:Number):void
		{
			if (this.fullStats)
			{
				this.newTimeout(setTimeout(this.fullStats.updateFullStats, timeout));
			}
		}
		
		private function newTimeout(id:Number):void
		{
			if (this.timeoutID)
			{
				clearTimeout(this.timeoutID);
			}
			this.timeoutID = id;
		}
		
		private function updateALL():void
		{
			if (this.panels)
			{
				this.panels.updatePlayersPanel();
			}
			if (this.fullStats && this.fullStats.visible)
			{
				this.fullStats.updateFullStats();
			}
			if (this.battleLoading && this.battleLoading.visible)
			{
				this.battleLoading.updateBattleloading();
			}
		}
	}
}