package net.armagomen.battleobserver.battle.components.teambases
{
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.battle.components.teambases.TeamBase;
	
	public class TeamBasesUI extends ObserverBattleDisplayable
	{
		private var bases:Object = {"green": null, "red": null};
		private var settings:Object;
		private var colors:Object;
		private var yPos:Number = 100;
		
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
		
		public function as_addTeamBase(team:String, points:Number, invadersCnt:int, time:String, text:String):void
		{
			if (this.bases[team])
			{
				this.bases[team].updateBase(points * 0.01, invadersCnt, time, text);
			}
			else
			{
				var base:TeamBase = new TeamBase(this.animationEnabled(), this.isColorBlind());
				base.create(this.settings, this.getShadowSettings(), this.colors, team);
				base.updateBase(points * 0.01, invadersCnt, time, text);
				if (this.bases["green"] || this.bases["red"])
				{
					var offset:Number = this.settings.y >= 0 ? this.settings.height + 4 : -(this.settings.height + 4);
					base.y += offset;
				}
				this.addChild(base);
				this.bases[team] = base;
			}
		}
		
		public function as_updateBase(team:String, points:Number, invadersCnt:int, time:String, text:String):void
		{
			if (this.bases[team])
			{
				this.bases[team].updateBase(points * 0.01, invadersCnt, time, text);
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
				this.removeChild(this.bases[team]);
				this.bases[team] = null;
			}
			
			if (this.bases["green"] && this.bases["green"].y != this.yPos)
			{
				this.bases["green"].y = this.yPos;
			}
			if (this.bases["red"] && this.bases["red"].y != this.yPos)
			{
				this.bases["red"].y = this.yPos;
			}
		}
	
	}
}