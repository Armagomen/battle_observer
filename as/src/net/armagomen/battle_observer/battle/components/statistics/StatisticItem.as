package net.armagomen.battle_observer.battle.components.statistics

{
	import flash.display.Sprite;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	
	public class StatisticItem extends Sprite
	{
		private var _text:TextExt;
		private var data:Object;
		
		private const position:Number = 385;
		private const DEAD_ALPHA:Number = 0.7;
		
		public function StatisticItem(data:Object, isEnemy:Boolean)
		{
			super();
			var w:Number = 42;
			this.data = data;
			this.x = isEnemy ? -this.position - w : this.position;
			this.graphics.beginFill(data.color, 0.92);
			this.graphics.drawRoundRect(0, 3, w, 18, 6, 6);
			this.graphics.endFill();
			
			this._text = new TextExt(w >> 1, 1, Constants.diff, "center", this);
			this._text.text = data.winRate;
		}
		
		public function setVisible(active:Boolean):void
		{
			if (this.visible != active)
			{
				this.visible = active;
			}
		}
		
		public function altMode(enable:Boolean):void
		{
			this._text.text = enable ? this.data.battles : this.data.winRate;
		}
		
		public function setDead(value:Boolean):void
		{
			this.alpha = value ? DEAD_ALPHA : 1.0;
		}
	}
}