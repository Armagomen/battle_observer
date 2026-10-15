package net.armagomen.battle_observer.battle.components.teamshealth 
{
	import flash.display.*;
	import flash.display.Sprite;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battle_observer.battle.components.teamshealth.score.Score;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;

	public class Minimal extends Sprite 
	{
		private var greenDiff:TextExt;
		private var redDiff:TextExt;
		private var colors:Object;
		private var score:Score;
		private var greenText:TextExt;
		private var redText:TextExt;
		
		[Embed(source = "img/v3.png")]
		private var _bg:Class;
		
		[Embed(source = "img/v3_cb.png")]
		private var _bg_cb:Class;
			
		public function Minimal(colorBlind:Boolean, colors:Object) 
		{
			super();
			
			var backgroung:Bitmap = colorBlind ?  new this._bg_cb() as Bitmap: new this._bg() as Bitmap;
			this.addChild(backgroung);
			backgroung.x = -(backgroung.width >> 1);
			backgroung.alpha = 0.7;
			
			this.score = new Score(colorBlind);
			this.addChild(score);
			
			this.greenText = new TextExt(-52, 1, Constants.middleText, TextFieldAutoSize.RIGHT, this);
			this.redText = new TextExt(52, 1, Constants.middleText, TextFieldAutoSize.LEFT, this);
			
			this.greenDiff = new TextExt(-142, 4, Constants.diff, TextFieldAutoSize.LEFT, this);
			this.redDiff = new TextExt(142, 4, Constants.diff, TextFieldAutoSize.RIGHT, this);
			
			this.greenDiff.alpha = this.redDiff.alpha = 0.8;
		}
		
		public function setColorBlind(enabled:Boolean):void
		{
			this.score.setColorBlind(enabled);
		}
		
		public function updateScore(ally:int, enemy:int):void
		{
			this.score.updateScore(ally, enemy);
		}
		
		public function setBarScale(isEnemy:Boolean, percent:Number):void
		{
		}
		
		private function difference(param:int):void
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
		
		public function remove():void
		{
			this.removeChildren();
			this.greenDiff = null;
			this.redDiff = null;
			this.score.removeChildren();
			this.score = null;
			this.greenText = null;
			this.redText = null;
		}
		
		
		public function update(alliesHP:int, enemiesHP:int, totalAlliesHP:int, totalEnemiesHP:int):void
		{
			this.greenText.text = alliesHP.toString();
			this.redText.text = enemiesHP.toString();
			this.difference(alliesHP - enemiesHP);
		}
		
	}

}