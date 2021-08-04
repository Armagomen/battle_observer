package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.events.Event;
	import flash.text.TextFieldAutoSize;
	import flash.text.TextFormat;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDispalaysble;
	import net.armagomen.battleobserver.battle.components.teamshealth.Default;
	import net.armagomen.battleobserver.battle.components.teamshealth.League;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.data.constants.Linkages;
	import net.wg.gui.battle.views.BaseBattlePage;
	
	public class TeamsHealthUI extends ObserverBattleDispalaysble
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
		public var animationEnabled:Function;
		public var getShadowSettings:Function;
		public var getAlpha:Function;
		
		public function TeamsHealthUI()
		{
			super();
		}
		
		public function as_startUpdate(settings:Object, colors:Object, colorBlind:Boolean):void
		{
			if (!this.loaded)
			{
				var battlePage:*      = parent;
				var fragCorrelation:* = battlePage.getComponent(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR);
				if (fragCorrelation != null)
				{
					parent.removeChild(fragCorrelation);
					this.x = App.appWidth >> 1;
					this.colors = colors;
					this.isColorBlind = colorBlind;
					var shadowSettings:Object = getShadowSettings();
					var barWidth:Number       = Math.max(settings.barsWidth, 150.0);
					this.hpBars = this.createHpbars(settings, barWidth);
					var isLeague:Boolean     = this.hpBars as League;
					var textXpos:Number      = !isLeague ? 50 + (barWidth / 2) : 20 + barWidth;
					var textStyle:TextFormat = !isLeague ? Filters.normalText : Filters.middleText;
					this.addChild(this.hpBars);
					this.greenText = new TextExt("greenText", -textXpos, 1, textStyle, !isLeague ? TextFieldAutoSize.CENTER : TextFieldAutoSize.LEFT, shadowSettings, this);
					this.redText = new TextExt("redText", textXpos, 1, textStyle, !isLeague ? TextFieldAutoSize.CENTER : TextFieldAutoSize.RIGHT, shadowSettings, this);
					this.greenDiff = new TextExt("greenDiff", -55, 1, textStyle, TextFieldAutoSize.RIGHT, shadowSettings, this);
					this.redDiff = new TextExt("redDiff", 55, 1, textStyle, TextFieldAutoSize.LEFT, shadowSettings, this);
					this.score = new Score(shadowSettings, colorBlind, this.colors, settings.style);
					this.addChild(this.score);
					if (settings.markers.enabled)
					{
						this.markers = new Markers(settings.markers, shadowSettings, this.getAlpha());
						this.addChild(this.markers);
					}
					this.loaded = true;
				}
			}
		}
		
		private function createHpbars(settings:Object, barWidth:Number):*
		{
			switch (settings.style)
			{
			case "league": 
				return new League(animationEnabled(), settings, barWidth, this.isColorBlind, this.colors);
			default: 
				return new Default(animationEnabled(), settings, barWidth, this.isColorBlind, this.colors);
			}
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
				this.redDiff.text = "+".concat(Math.abs(param).toString());
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
		
		override public function onResizeHandle(event:Event):void
		{
			this.x = App.appWidth >> 1;
		}
	}
}