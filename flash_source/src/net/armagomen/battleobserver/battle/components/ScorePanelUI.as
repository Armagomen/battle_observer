package net.armagomen.battleobserver.battle.components
{
	import flash.display.*;
	import flash.events.*;
	import flash.filters.*;
	import flash.text.*;
	import net.armagomen.battleobserver.battle.utils.Filters;
	import net.armagomen.battleobserver.battle.utils.TextExt;
	import net.wg.gui.battle.components.*;

	public class ScorePanelUI extends BattleDisplayable
	{
		private var allyArrowVector:Vector.<Number> = new <Number>[-5, 7, 0, 7, 5, 15, 0, 23, -5, 23, 0, 15, -5, 7];
		private var enemyArrowVector:Vector.<Number> = new <Number>[5, 7, 0, 7, -5, 15, 0, 23, 5, 23, 0, 15, 5, 7];
		private var arrowCommands:Vector.<int> = new <int>[1, 2, 2, 2, 2, 2, 2];
		private var arrowDots:Shape;
		private var arrowGreen:Shape;
		private var arrowRed:Shape;
		private var greenScore:TextField;
		private var redScore:TextField;
		private var allyM:TextField;
		private var enemyM:TextField;
		public var getShadowSettings:Function;
		public var getAlpha:Function;

		public function ScorePanelUI(compName:String)
		{
			this.name = compName;
			super();
		}

		public function as_startUpdate(markers:Object):void
		{
			this.arrowDots = new Shape();
			this.arrowGreen = new Shape();
			this.arrowRed = new Shape();
			this.addChild(this.arrowDots);
			this.addChild(this.arrowGreen);
			this.addChild(this.arrowRed);

			this.x = App.appWidth >> 1;
			Filters.markersFormat.letterSpacing = 0.9;

			this.arrowDots.name = "arrowDots";
			this.arrowDots.filters = [Filters.glowScore];
			this.arrowDots.graphics.beginFill(0xFAFAFA, 1);
			this.arrowDots.graphics.drawCircle(0, 10, 3);
			this.arrowDots.graphics.drawCircle(0, 21, 3);
			this.arrowDots.graphics.endFill();
			this.arrowDots.visible = false;

			this.arrowGreen.name = "arrowGreen";
			this.arrowGreen.filters = [Filters.glowScore];
			this.arrowGreen.graphics.beginFill(0xFAFAFA, 1);
			this.arrowGreen.graphics.drawPath(this.arrowCommands, this.allyArrowVector);
			this.arrowGreen.graphics.endFill();
			this.arrowGreen.visible = false;

			this.arrowRed.name = "arrowRed";
			this.arrowRed.filters = [Filters.glowScore];
			this.arrowRed.graphics.beginFill(0xFAFAFA, 1);
			this.arrowRed.graphics.drawPath(this.arrowCommands, this.enemyArrowVector);
			this.arrowRed.graphics.endFill();
			this.arrowRed.visible = false;

			var shadowSettings:Object = getShadowSettings();

			this.greenScore = new TextExt("greenScore", -25, -3, Filters.scoreformat, TextFieldAutoSize.CENTER, shadowSettings, this);
			this.greenScore.antiAliasType = AntiAliasType.NORMAL;
			this.redScore = new TextExt("redScore", 25, -3, Filters.scoreformat, TextFieldAutoSize.CENTER, shadowSettings, this);
			this.redScore.antiAliasType = AntiAliasType.NORMAL;

			if (markers.enabled)
			{
				var alpha:Number = this.getAlpha();
				var allySpr:Sprite = new Sprite();
				allySpr.alpha = alpha;
				this.addChild(allySpr);
				this.allyM = new TextExt("allyM", -markers.x, markers.y, Filters.markersFormat, TextFieldAutoSize.RIGHT, shadowSettings, allySpr);
				this.allyM.embedFonts = true;

				var enemySpr:Sprite = new Sprite();
				enemySpr.alpha = alpha;
				this.addChild(enemySpr);
				this.enemyM = new TextExt("enemyM", markers.x, markers.y, Filters.markersFormat, TextFieldAutoSize.LEFT, shadowSettings, enemySpr);
				this.enemyM.embedFonts = true;
			}
			App.utils.data.cleanupDynamicObject(markers);
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

		public function as_clearScene():void
		{
			while (this.numChildren > 0){
				this.removeChildAt(0);
			}
			this.arrowDots = null;
			this.arrowGreen = null;
			this.arrowRed = null;
			this.greenScore = null;
			this.redScore = null;
			this.allyM = null;
			this.enemyM = null;
			var page:* = parent;
			page.unregisterComponent(this.name);
		}

		override protected function onDispose():void
		{
			this.removeEventListener(Event.RESIZE, this._onResizeHandle);
			super.onDispose();
		}

		public function as_updateScore(ally:int, enemy:int):void
		{
			this.arrowDots.visible = ally == enemy;
			this.arrowGreen.visible = ally > enemy;
			this.arrowRed.visible = ally < enemy;
			this.greenScore.text = ally.toString();
			this.redScore.text = enemy.toString();
		}

		public function as_markers(correlationItemsLeft:String, correlationItemsRight:String):void
		{
			if (correlationItemsRight)
			{
				this.enemyM.htmlText = correlationItemsRight;
			}
			if (correlationItemsLeft)
			{
				this.allyM.htmlText = correlationItemsLeft;
			}
		}

		public function as_clearMarkers():void
		{
			this.enemyM.htmlText = "";
			this.allyM.htmlText = "";
		}

		public function _onResizeHandle(event:Event):void
		{
			this.x = App.appWidth >> 1;
		}
	}

}