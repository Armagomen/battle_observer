package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.display.*;
	import flash.events.*;
	import flash.filters.*;
	import flash.geom.ColorTransform;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.components.teamshealth.Default;
	import net.armagomen.battleobserver.battle.components.teamshealth.Legue;
	import net.armagomen.battleobserver.battle.utils.Filters;
	import net.armagomen.battleobserver.battle.utils.Params;
	import net.armagomen.battleobserver.battle.utils.TextExt;
	import net.armagomen.battleobserver.battle.utils.Utils;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.*;

	public class TeamsHealthUI extends BattleDisplayable
	{
		private var greenText:TextField;
		private var redText:TextField;
		private var greenDiff:TextField;
		private var redDiff:TextField;
		private var colors:Object = null;
		private var hpBars:* = null;
		public var getShadowSettings:Function;

		public function TeamsHealthUI(compName:String)
		{
			super();
			this.name = compName;
		}

		public function as_startUpdate(settings:Object, colorBlind:Boolean):void
		{
			this.colors = settings.colors;
			Params.setIslegue(settings["style"] == 'legue');
			Params.setcBlind(colorBlind);
			Params.setAllyColor(Utils.colorConvert(colors.ally));
			Params.setEnemyColor(Utils.colorConvert(Params.cBlind ? colors.enemyColorBlind : colors.enemy));
			Params.setHpBarsEnabled(settings.enabled);

			if (settings.enabled)
			{
				this.x = App.appWidth >> 1;
				var barWidth:Number = Math.max(settings.barsWidth, 150.0);
				var textXpos:Number = !Params.isLegue ? 50 + (barWidth / 2) : 30 + barWidth;
				hpBars = this.createHpbars(settings, barWidth);

				var shadowSettings:Object = getShadowSettings();
				greenText = new TextExt("greenText", -textXpos, 2, Filters.middleText, !Params.isLegue ? TextFieldAutoSize.CENTER : TextFieldAutoSize.LEFT, shadowSettings, this);
				redText = new TextExt("redText", textXpos, 2, Filters.middleText, !Params.isLegue ? TextFieldAutoSize.CENTER : TextFieldAutoSize.RIGHT, shadowSettings, this);
				greenDiff = new TextExt("greenDiff", -55, 2, Filters.middleText, TextFieldAutoSize.RIGHT, shadowSettings, this);
				redDiff = new TextExt("redDiff", 55, 2, Filters.middleText, TextFieldAutoSize.LEFT, shadowSettings, this);

				var wgPanel:DisplayObject = this.getWGpanel();
				if (wgPanel != null)
				{
					parent.removeChild(wgPanel);
				}
			}
			App.utils.data.cleanupDynamicObject(settings);
		}

		private function getWGpanel():DisplayObject
		{
			var battlePage:* = parent;
			switch (true)
			{
			case battlePage._componentsStorage.hasOwnProperty(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR):
				return battlePage.getComponent(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR);
			case battlePage._componentsStorage.hasOwnProperty(BATTLE_VIEW_ALIASES.EPIC_RANDOM_SCORE_PANEL):
				return battlePage.getComponent(BATTLE_VIEW_ALIASES.EPIC_RANDOM_SCORE_PANEL);
			default:
				return null;
			}
		}

		private function createHpbars(settings:Object, barWidth:Number):DisplayObject
		{
			switch (settings["style"])
			{
			case "legue":
				return this.addChild(new Legue(settings, barWidth));
			case "normal":
				return this.addChild(new Default(settings, barWidth));
			default:
				return this.addChild(new Legue(settings, barWidth));
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
			this.removeEventListener(Event.RESIZE, this._onResizeHandle);
			super.onDispose();
		}

		public function as_clearScene():void
		{
			while (this.numChildren > 0){
				this.removeChildAt(0);
			}
			this.greenText = null;
			this.redText = null;
			this.greenDiff = null;
			this.redDiff = null;
			App.utils.data.cleanupDynamicObject(this.colors);
			this.colors = null;
			this.hpBars = null;
			var page:* = parent;
			page.unregisterComponent(this.name);
		}

		public function as_colorBlind(enabled:Boolean):void
		{
			Params.setcBlind(enabled);
			var newColor:uint = Utils.colorConvert(enabled ? this.colors.enemyColorBlind : this.colors.enemy);
			Params.setEnemyColor(newColor);
			var barColor:ColorTransform = hpBars.enemyHpBar.transform.colorTransform;
			barColor.color = newColor;
			hpBars.enemyHpBar.transform.colorTransform = barColor;
		}

		public function as_difference(param:int):void
		{
			if (param < 0)
			{
				redDiff.text = "+".concat((-param).toString());
				greenDiff.text = "";
			}
			else if (param > 0)
			{
				greenDiff.text = "+".concat(param.toString());
				redDiff.text = "";
			}
			else
			{
				greenDiff.text = "";
				redDiff.text = "";
			}
		}

		public function as_updateHealth(alliesHP:int, enemiesHP:int, totalAlliesHP:int, totalEnemiesHP:int):void
		{
			hpBars.setBarScale("green", totalAlliesHP > 0 ? alliesHP / totalAlliesHP : 1);
			hpBars.setBarScale("red", totalEnemiesHP > 0 ? enemiesHP / totalEnemiesHP : 1);
			greenText.text = alliesHP.toString();
			redText.text = enemiesHP.toString();
		}

		private function _onResizeHandle(event:Event):void
		{
			this.x = App.appWidth >> 1;
		}
	}
}