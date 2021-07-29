package net.armagomen.battleobserver.battle.components.teambases
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.components.teambases.TeamBase;
	import net.wg.gui.battle.components.*;
	
	public class TeamBasesUI extends BattleDisplayable
	{
		private var bases:Object = {"green": null, "red": null};
		private var settings:Object;
		private var colors:Object;
		private var shadowSettings:Object;
		private var yPos:Number = 100;
		public var getShadowSettings:Function;
		public var isColorBlind:Function;
		public var animationEnabled:Function;
		
		public function TeamBasesUI()
		{
			super();
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
		
		public function as_startUpdate(basesSettings:Object, colors:Object):void
		{
			this.settings = basesSettings;
			this.colors = colors;
			this.shadowSettings = getShadowSettings();
			this.yPos = basesSettings.y >= 0 ? basesSettings.y : App.appHeight + basesSettings.y;
		}
		
		public function as_addTeamBase(team:String, points:Number, invadersCnt:String, time:String, text:String):void
		{
			if (this.bases[team])
			{
				this.bases[team].updateBase(points * 0.01, invadersCnt, time, text);
			}
			else
			{
				var base:TeamBase = new TeamBase(this.animationEnabled(), this.isColorBlind());
				base.create(this.settings, this.shadowSettings, this.colors, team);
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
		
		public function as_updateBase(team:String, points:Number, invadersCnt:String, time:String, text:String):void
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