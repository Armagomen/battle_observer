package net.armagomen.battle_observer.battle.components.teambases
{
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.battle.components.teambases.TeamBase;
	
	public class TeamBasesUI extends ObserverBattleDisplayable
	{
		private var bases:Object = {};
		private var settings:Object;
		private var colors:Object;
		private var yPos:Number = 60;
		
		public function TeamBasesUI()
		{
			super();
		}
		
		override protected function onPopulate():void 
		{
			super.onPopulate();
			this.settings = this.getSettings();
			this.colors = this.getColors().global;
			this.yPos = this.settings.y >= 0 ? this.settings.y : App.appHeight + this.settings.y;
		}
		
		override protected function onBeforeDispose():void 
		{
			App.utils.data.cleanupDynamicObject(this.bases);
			App.utils.data.cleanupDynamicObject(this.settings);
			App.utils.data.cleanupDynamicObject(this.colors);
			super.onBeforeDispose();
		}
		
		public function as_addTeamBase(team:String, points:int, invadersCnt:int, time:String, text:String):void
		{
			if (this.bases[team])
			{
				this.bases[team].updateBase(points, invadersCnt, time, text);
			}
			else
			{
				var base:TeamBase = new TeamBase(this.isColorBlind());
				base.create(this.settings, this.colors, team);
				base.updateBase(points, invadersCnt, time, text);
				var offset:Number = this.settings.y >= 0 ? this.settings.height + 4 : -(this.settings.height + 4);
				for each (var t_base:TeamBase in this.bases) 
				{
					if (t_base){
						base.y += offset;
					}
				}
				this.addChild(base);
				this.bases[team] = base;
			}
		}
		
		public function as_updateBase(team:String, points:int, invadersCnt:int, time:String, text:String):void
		{
			if (this.bases[team])
			{
				this.bases[team].updateBase(points, invadersCnt, time, text);
			}
		}
		
		public function as_updateCaptureText(team:String, captureText:String):void
		{
			if (this.bases[team])
			{
				this.bases[team].updateCaptureText(captureText);
			}
		}
		
		public function as_removeTeamBase(team:String):void
		{
			if (this.bases[team])
			{
				this.bases[team].remove();
				this.removeChild(this.bases[team]);
				this.bases[team] = null;
			}
			for each (var base:TeamBase in this.bases) 
			{
				if (base && base.y != this.yPos){
					base.y = this.yPos;
				}
			}
		}
	
	}
}