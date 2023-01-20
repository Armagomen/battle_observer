package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.events.Event;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.battle.components.teamshealth.Default;
	import net.armagomen.battleobserver.battle.components.teamshealth.League;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class TeamsHealthUI extends ObserverBattleDisplayable
	{
		private var greenText:TextExt;
		private var redText:TextExt;
		private var greenDiff:TextExt;
		private var redDiff:TextExt;
		private var colors:Object = null;
		private var hpBars:*      = null;
		private var score:Score;
		private var markers:Markers;
		
		public function TeamsHealthUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			if (this.hpBars == null)
			{
				var settings:Object = this.getSettings();
				this.colors = this.getColors().global;
				this.x = App.appWidth >> 1;
				var shadowSettings:Object = getShadowSettings();
				var barWidth:Number       = Math.max(settings.barsWidth, 150.0);
				this.hpBars = this.createHpBars(settings, barWidth);
				var isLeague:Boolean = this.hpBars as League;
				var textXpos:Number  = !isLeague ? 50 + (barWidth / 2) : 20 + barWidth;
				this.addChild(this.hpBars);
				this.greenText = new TextExt(-textXpos, 1, Filters.middleText, !isLeague ? TextFieldAutoSize.CENTER : TextFieldAutoSize.LEFT, shadowSettings, this);
				this.redText = new TextExt(textXpos, 1, Filters.middleText, !isLeague ? TextFieldAutoSize.CENTER : TextFieldAutoSize.RIGHT, shadowSettings, this);
				this.greenDiff = new TextExt(-55, 2, Filters.normalText, TextFieldAutoSize.RIGHT, shadowSettings, this);
				this.redDiff = new TextExt(55, 2, Filters.normalText, TextFieldAutoSize.LEFT, shadowSettings, this);
				this.score = new Score(shadowSettings, this.isColorBlind(), this.colors, settings.style);
				this.addChild(this.score);
				if (settings.markers.enabled)
				{
					this.markers = new Markers(settings.markers, shadowSettings, this.getAlpha());
					this.addChild(this.markers);
				}
			}
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.removeChildren();
			this.hpBars.remove();
			this.hpBars = null;
			this.greenDiff = null;
			this.greenText = null;
			this.redText = null;
			this.redText = null;
			this.score.removeChildren();
			this.score = null;
			if (this.markers)
			{
				this.markers.removeChildren();
				this.markers = null;
			}
			App.utils.data.cleanupDynamicObject(this.colors);
		}
		
		private function createHpBars(settings:Object, barWidth:Number):*
		{
			switch (settings.style)
			{
			case "league": 
				return new League(barWidth, this.isColorBlind(), this.colors);
			default: 
				return new Default(settings.outline, barWidth, this.isColorBlind(), this.colors);
			}
		}
		
		public function as_colorBlind(enabled:Boolean):void
		{
			this.hpBars.setColorBlind(enabled);
			this.score.setColorBlind(enabled);
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
			this.hpBars.setBarScale(false, totalAlliesHP > 0 ? Math.min(alliesHP / totalAlliesHP, 1.0) : 1.0);
			this.hpBars.setBarScale(true, totalEnemiesHP > 0 ? Math.min(enemiesHP / totalEnemiesHP, 1.0) : 1.0);
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