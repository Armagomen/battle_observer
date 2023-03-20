package net.armagomen.battleobserver.battle.components.teamshealth 
{
	import flash.display.*;
	import flash.display.Sprite;
	import flash.events.*;
	import flash.filters.*;
	import flash.text.*;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.utils.Utils;
	import net.wg.gui.battle.components.*;
	/**
	 * ...
	 * @author ...
	 */
	public class Score extends Sprite 
	{
		private var allyArrowVector:Vector.<Number>  = new <Number>[-5, 7, 0, 7, 5, 15, 0, 23, -5, 23, 0, 15, -5, 7];
		private var enemyArrowVector:Vector.<Number> = new <Number>[5, 7, 0, 7, -5, 15, 0, 23, 5, 23, 0, 15, 5, 7];
		private var arrowCommands:Vector.<int>       = new <int>[1, 2, 2, 2, 2, 2, 2];
		private var arrowDots:Shape;
		private var arrowGreen:Shape;
		private var arrowRed:Shape;
		private var greenScore:TextExt;
		private var redScore:TextExt;
		private var allyColor:String;
		private var ememyColor:String;
		private var enemyColorBlind:String;
		
		public function Score(colorBlind:Boolean, colors:Object, style:String) 
		{
			super();
			
			this.allyColor = style == "normal" ? colors.ally : "#FAFAFA";
			this.ememyColor = style == "normal" ? colors.enemy : "#FAFAFA";
			this.enemyColorBlind = style == "normal" ? colors.enemyColorBlind : "#FAFAFA";
			
			this.arrowDots = new Shape();
			this.arrowGreen = new Shape();
			this.arrowRed = new Shape();
			
			this.arrowDots.name = "arrowDots";
			this.arrowDots.filters = [Filters.glowScore];
			this.arrowDots.graphics.beginFill(0xFAFAFA, 1);
			this.arrowDots.graphics.drawCircle(0, 10, 3);
			this.arrowDots.graphics.drawCircle(0, 21, 3);
			this.arrowDots.graphics.endFill();
			this.arrowDots.visible = false;
			
			this.arrowGreen.name = "arrowGreen";
			this.arrowGreen.filters = [Filters.glowScore];
			this.arrowGreen.graphics.beginFill(Utils.colorConvert(this.allyColor), 1);
			this.arrowGreen.graphics.drawPath(this.arrowCommands, this.allyArrowVector);
			this.arrowGreen.graphics.endFill();
			this.arrowGreen.visible = false;
			
			this.arrowRed.name = "arrowRed";
			this.arrowRed.filters = [Filters.glowScore];
			this.arrowRed.graphics.beginFill(Utils.colorConvert(colorBlind ? this.enemyColorBlind : this.ememyColor), 1);
			this.arrowRed.graphics.drawPath(this.arrowCommands, this.enemyArrowVector);
			this.arrowRed.graphics.endFill();
			this.arrowRed.visible = false;
			
			this.greenScore = new TextExt(-25, -3, Filters.scoreformat, TextFieldAutoSize.CENTER, this);
			this.greenScore.antiAliasType = AntiAliasType.NORMAL;
			this.redScore = new TextExt(25, -3, Filters.scoreformat, TextFieldAutoSize.CENTER, this);
			this.redScore.antiAliasType = AntiAliasType.NORMAL;
			
			this.addChild(this.arrowDots);
			this.addChild(this.arrowGreen);
			this.addChild(this.arrowRed);
		}
		
		public function updateScore(ally:int, enemy:int):void
		{
			this.arrowDots.visible = ally == enemy;
			this.arrowGreen.visible = ally > enemy;
			this.arrowRed.visible = ally < enemy;
			this.greenScore.text = ally.toString();
			this.redScore.text = enemy.toString();
		}
		
		public function setColorBlind(enabled:Boolean):void
		{
			Utils.updateColor(this.arrowRed, enabled ? this.enemyColorBlind : this.ememyColor);
		}
	}

}