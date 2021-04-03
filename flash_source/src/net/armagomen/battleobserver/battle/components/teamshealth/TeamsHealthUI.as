package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.display.*;
	import flash.events.*;
	import flash.filters.*;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.components.teamshealth.Default;
	import net.armagomen.battleobserver.battle.components.teamshealth.League;
	import net.armagomen.battleobserver.battle.components.teamshealth.classic.Classic;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.utils.Utils;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.*;
	import net.wg.gui.battle.random.views.teamBasesPanel.TeamBasesPanel;
	
	public class TeamsHealthUI extends BattleDisplayable
	{
		private var greenText:TextExt;
		private var redText:TextExt;
		private var greenDiff:TextExt;
		private var redDiff:TextExt;
		private var colors:Object        = null;
		private var hpBars:*             = null;
		private var score:Score;
		private var markers:Markers;
		private var loaded:Boolean       = false;
		private var isColorBlind:Boolean = false;
		
		public var getShadowSettings:Function;
		public var getAlpha:Function;
		
		public function TeamsHealthUI(compName:String)
		{
			super();
			this.name = compName;
		}
		
		public function as_startUpdate(settings:Object, colors:Object, colorBlind:Boolean):void
		{
			if (!this.loaded)
			{
				var wgPanel:DisplayObject = this.getWGpanel();
				if (wgPanel != null)
				{
					parent.removeChild(wgPanel);
					this.x = App.appWidth >> 1;
					this.colors = colors;
					this.isColorBlind = colorBlind;
					
					var shadowSettings:Object = getShadowSettings();
					var barWidth:Number       = Math.max(settings.barsWidth, 150.0);
					this.hpBars = this.createHpbars(settings, barWidth);
					var isLeague:Boolean = this.hpBars as League;
					var textXpos:Number  = !isLeague ? 50 + (barWidth / 2) : 20 + barWidth;
					var textStyle:*      = !isLeague ? Filters.normalText : Filters.middleText;
					
					this.addChild(this.hpBars);
					
					this.greenText = new TextExt("greenText", -textXpos, 2, Filters.middleText, !isLeague ? TextFieldAutoSize.CENTER : TextFieldAutoSize.LEFT, shadowSettings, this);
					this.redText = new TextExt("redText", textXpos, 2, Filters.middleText, !isLeague ? TextFieldAutoSize.CENTER : TextFieldAutoSize.RIGHT, shadowSettings, this);
					this.greenDiff = new TextExt("greenDiff", -55, 2, Filters.middleText, TextFieldAutoSize.RIGHT, shadowSettings, this);
					this.redDiff = new TextExt("redDiff", 55, 2, Filters.middleText, TextFieldAutoSize.LEFT, shadowSettings, this);
					
					this.score = new Score(shadowSettings, colorBlind, this.colors, settings.style);
					this.markers = new Markers(settings.markers, shadowSettings, this.getAlpha());
					
					this.addChild(this.score);
					this.addChild(this.markers);
					
					this.loaded = true;
				}
			}
		}
		
		public function moveTeamBasesPanel():void
		{
			var battlePage:*                  = parent;
			var teamBasesPanel:TeamBasesPanel = battlePage.getComponent(BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL);
			if (teamBasesPanel)
			{
				teamBasesPanel.y += 10;
			}
		}
		
		private function getWGpanel():DisplayObject
		{
			var battlePage:* = parent;
			switch (true)
			{
			case battlePage._componentsStorage.hasOwnProperty(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR): 
				return battlePage.getComponent(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR);
			default: 
				return null;
			}
		}
		
		private function createHpbars(settings:Object, barWidth:Number):*
		{
			switch (settings.style)
			{
			case "league": 
				return new League(settings, barWidth, this.isColorBlind, this.colors);
			case "normal": 
				return new Default(settings, barWidth, this.isColorBlind, this.colors);
			//case "classic":
			//return new Classic(settings.style, this.isColorBlind, this.colors);
			default: 
				return new League(settings, barWidth, this.isColorBlind, this.colors);
			}
		}
		
		override protected function configUI():void
		{
			super.configUI();
			this.tabEnabled = false;
			this.tabChildren = false;
			this.mouseEnabled = false;
			this.mouseChildren = false;
			this.buttonMode = false;
			this.addEventListener(Event.RESIZE, this._onResizeHandle);
		}
		
		override protected function onDispose():void
		{
			this.hpBars = null;
			this.score = null;
			this.markers = null;
			App.utils.data.cleanupDynamicObject(this.colors);
			this.removeEventListener(Event.RESIZE, this._onResizeHandle);
			super.onDispose();
		}
		
		public function as_colorBlind(enabled:Boolean):void
		{
			if (this.isColorBlind != enabled)
			{
				this.isColorBlind = enabled;
				this.hpBars.setColorBlind(enabled);
				this.score.setColorBlind(enabled);
			}
		}
		
		public function as_difference(param:int):void
		{
			if (param < 0)
			{
				this.redDiff.text = "+".concat((-param).toString());
				this.greenDiff.text = "";
			}
			else if (param > 0)
			{
				this.greenDiff.text = "+".concat(param.toString());
				this.redDiff.text = "";
			}
			else
			{
				this.greenDiff.text = "";
				this.redDiff.text = "";
			}
		}
		
		public function as_updateHealth(alliesHP:int, enemiesHP:int, totalAlliesHP:int, totalEnemiesHP:int):void
		{
			this.hpBars.setBarScale("green", totalAlliesHP > 0 ? alliesHP / totalAlliesHP : 1);
			this.hpBars.setBarScale("red", totalEnemiesHP > 0 ? enemiesHP / totalEnemiesHP : 1);
			this.greenText.text = alliesHP.toString();
			this.redText.text = enemiesHP.toString();
		}
		
		public function as_updateScore(ally:int, enemy:int):void
		{
			this.score.updateScore(ally, enemy);
		}
		
		public function as_markers(correlationItemsLeft:String, correlationItemsRight:String):void
		{
			this.markers.update_markers(correlationItemsLeft, correlationItemsRight);
		}
		
		private function _onResizeHandle(event:Event):void
		{
			this.x = App.appWidth >> 1;
		}
	}
}