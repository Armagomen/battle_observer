package net.armagomen.battleobserver.battle.components.teambases
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.components.teambases.TeamBase;
	import net.armagomen.battleobserver.utils.Params;
	import net.wg.gui.battle.components.*;
	
	public class TeamBasesUI extends BattleDisplayable
	{
		private var bases:Object = {"green": null, "red": null};
		private var settings:Object;
		private var shadowSettings:Object;
		public var getShadowSettings:Function;
		
		public function TeamBasesUI(compName:String)
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
		
		public function as_startUpdate(bases:Object):void
		{
			this.settings = App.utils.data.cloneObject(bases);
			this.shadowSettings = getShadowSettings();
			App.utils.data.cleanupDynamicObject(bases);
		}
		
		public function as_addTeamBase(team:String, points:Number, invadersCnt:String, time:String, text:String):void
		{
			if (this.bases[team])
			{
				this.as_updateBase(team, points, invadersCnt, time, text);
			}
			else
			{
				var base:TeamBase = new TeamBase(team);
				base.create(this.settings, this.shadowSettings);
				base.BaseText.htmlText = text;
				base.BaseTimer.text = time;
				base.BaseVehicles.text = invadersCnt;
				if (this.bases["green"] || this.bases["red"])
				{
					base.y += this.settings.height + 4;
				}
				this.addChild(base);
				this.bases[team] = base;
				base.progressBar.scaleX = points / 100.0;
			}
		}
		
		public function as_updateBase(team:String, points:Number, invadersCnt:String, time:String, text:String):void
		{
			if (this.bases[team])
			{
				var base:TeamBase = this.bases[team] as TeamBase;
				base.BaseText.htmlText = text;
				base.BaseTimer.text = time;
				base.BaseVehicles.text = invadersCnt;
				if (Params.AnimationEnabled)
				{
					base.setBarScale(points / 100.0);
				}
				else
				{
					base.progressBar.scaleX = points / 100.0;
				}
			}
		}
		
		public function as_updateCaptureText(team:String, captureText:String):void
		{
			if (this.bases[team])
			{
				this.bases[team].BaseText.htmlText = captureText;
			}
		}
		
		public function as_removeTeamBase(team:String):void
		{
			if (this.bases[team])
			{
				if (Params.AnimationEnabled)
				{
					this.bases[team].stopAndClearAnimate();
				}
				this.removeChild(this.bases[team] as TeamBase);
				this.bases[team] = null;
			}
			
			if (this.bases["green"] && this.bases["green"].y != this.settings.y)
			{
				this.bases["green"].y = this.settings.y;
			}
			if (this.bases["red"] && this.bases["red"].y != this.settings.y)
			{
				this.bases["red"].y = this.settings.y;
			}
		}
	}
}