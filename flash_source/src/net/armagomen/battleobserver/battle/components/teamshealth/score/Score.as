package net.armagomen.battleobserver.battle.components.teamshealth.score
{
	import flash.display.*;
	import flash.display.Sprite;
	import flash.events.*;
	import flash.filters.*;
	import flash.text.*;
	import net.armagomen.battleobserver.utils.Constants;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.gui.battle.components.*;
	
	/**
	 * ...
	 * @author ...
	 */
	public class Score extends Sprite
	{
		private var arrowDots:Shape;
		[Embed(source = "ally.png")]
		private var arrowGreen:Class;
		[Embed(source = "enemy.png")]
		private var arrowRed:Class;
		[Embed(source = "enemy_cb.png")]
		private var arrowRedCB:Class;
		private var arrows:Vector.<Bitmap>;
		private var greenScore:TextExt;
		private var redScore:TextExt;
		private var isColorBlind:Boolean = false;
		
		public function Score(colorBlind:Boolean)
		{
			super();
			this.arrows = new <Bitmap>[new arrowGreen(), new arrowRed(), new arrowRedCB()];
			this.isColorBlind = colorBlind;
			this.arrowDots = new Shape();
			for each (var item:Bitmap in this.arrows)
			{
				item.width = item.height = 32;
				item.x = -16;
				item.y = -1;
				item.visible = false;
				this.addChild(item);
			}
			this.arrowDots.name = "arrowDots";
			this.arrowDots.filters = [Constants.glowScore];
			this.arrowDots.graphics.beginFill(0xFAFAFA, 1);
			this.arrowDots.graphics.drawCircle(0, 10, 3);
			this.arrowDots.graphics.drawCircle(0, 21, 3);
			this.arrowDots.graphics.endFill();
			this.arrowDots.visible = false;
			this.addChild(this.arrowDots);
			
			this.greenScore = new TextExt(-16, -3, Constants.scoreformat, TextFieldAutoSize.RIGHT, this);
			this.greenScore.antiAliasType = AntiAliasType.NORMAL;
			this.redScore = new TextExt(16, -3, Constants.scoreformat, TextFieldAutoSize.LEFT, this);
			this.redScore.antiAliasType = AntiAliasType.NORMAL;
		}
		
		public function updateScore(ally:int, enemy:int):void
		{
			this.arrowDots.visible = ally == enemy;
			this.arrows[0].visible = ally > enemy;
			this.arrows[this.isColorBlind ? 2 : 1].visible = ally < enemy;
			this.greenScore.text = ally.toString();
			this.redScore.text = enemy.toString();
		}
		
		public function setColorBlind(enabled:Boolean):void
		{
			this.isColorBlind = enabled;
			if (this.arrows[1].visible || this.arrows[2].visible)
			{
				this.arrows[1].visible = !enabled;
				this.arrows[2].visible = enabled;
			}
		}
	}
}