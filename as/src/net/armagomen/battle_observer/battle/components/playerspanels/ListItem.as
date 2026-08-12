package net.armagomen.battle_observer.battle.components.playerspanels
{
	import flash.display.Sprite;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.ProgressBar;
	import net.armagomen.battle_observer.utils.TextExt;
	
	
	public class ListItem extends Sprite
	{
		private var healthBar:ProgressBar = null;
		private var damage:TextExt        = null;
		public var isEnemy:Boolean        = false;
		private const position:Number     = 400;
		
		public function ListItem(enemy:Boolean)
		{
			super();
			this.isEnemy = enemy;
			this.x = enemy ? -this.position : this.position;
		}
		
		public function updateDamage(value:int):void
		{
			if (this.damage)
			{
				this.damage.text = value.toString();
			}
		}
		
		public function addDamage():void
		{
			if (!this.damage)
			{
				var autoSize:String = this.isEnemy ? TextFieldAutoSize.LEFT : TextFieldAutoSize.RIGHT; 
				this.damage = new TextExt(this.isEnemy ? 40 : -40, 1, Constants.middleText2, autoSize, this);
				this.damage.visible = false;
			}
		}
		
		public function addHealth(color:String, colorParams:Object, startVisible:Boolean):void
		{
			var barX:Number     = Constants.statistics ? 34 : 10;
			var barWidth:Number = Constants.statistics ? 64 : 70;
			var textX:Number    = (barWidth >> 1) - 1;
			if (this.isEnemy)
			{
				barWidth = -barWidth;
				barX = -barX;
				textX = -textX;
			}
			this.healthBar = new ProgressBar(barX, 3, barWidth, 18, color, colorParams.bgColor, 0);
			this.healthBar.setOutline(barWidth, 18);
			this.healthBar.addTextField(textX, -2, TextFieldAutoSize.CENTER, Constants.diff);
			this.healthBar.setVisible(startVisible);
			this.addChild(this.healthBar);
		}
		
		public function updateHealth(percent:Number, text:String):void
		{
			if (this.healthBar)
			{
				this.healthBar.setNewScale(percent * Constants.HUNDREDTH);
				this.healthBar.setText(text);
			}
		}
		
		public function setHealthVisible(vis:Boolean):void
		{
			if (this.healthBar)
			{
				this.healthBar.setVisible(vis);
			}
		}
		
		public function setDamageVisible(vis:Boolean):void
		{
			if (this.damage && this.damage.visible != vis)
			{
				this.damage.visible = vis
			}
		}
		
		public function setColor(hpColor:String):void
		{
			if (this.healthBar)
			{
				this.healthBar.updateColor(hpColor);
			}
		}
		
		public function setDeath():void
		{
			if (this.healthBar)
			{
				this.healthBar.remove();
				this.removeChild(this.healthBar);
				this.healthBar = null;
			}
		}
		
		public function remove():void
		{
			this.removeChildren();
			this.healthBar = null;
			this.damage = null;
			this.isEnemy = null;
			App.utils.data.cleanupDynamicObject(this);
		}
	}
}