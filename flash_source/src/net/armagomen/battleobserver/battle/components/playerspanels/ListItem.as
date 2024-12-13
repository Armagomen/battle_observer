package net.armagomen.battleobserver.battle.components.playerspanels
{
	import flash.display.Sprite;
	import net.armagomen.battleobserver.utils.Constants;
	import net.armagomen.battleobserver.utils.ProgressBar;
	import net.armagomen.battleobserver.utils.TextExt;
	
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
		
		public function updateDamage(text:String):void
		{
			if (this.damage)
			{
				this.damage.htmlText = text;
			}
		}
		
		public function addDamage(params:Object):void
		{
			if (!this.damage)
			{
				var autoSize:String = params.align;
				if (this.isEnemy && autoSize != "center")
				{
					autoSize = params.align == "left" ? "right" : "left";
				}
				this.damage = new TextExt(this.isEnemy ? -params.x : params.x, params.y, null, autoSize, this);
				this.damage.visible = false;
			}
		}
		
		public function addHealth(color:String, colorParams:Object, startVisible:Boolean):void
		{
			var barX:Number     = 10;
			var barWidth:Number = 80;
			var textX:Number    = 40;
			if (this.isEnemy)
			{
				barWidth = -barWidth;
				barX = -barX;
				textX = -textX;
			}
			this.healthBar = new ProgressBar(barX, 2, barWidth, 20, color, colorParams.bgColor, 0.2);
			this.healthBar.setOutline(barWidth, 20);
			this.healthBar.addTextField(textX, -2, "center", Constants.normalText15);
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
	}
}