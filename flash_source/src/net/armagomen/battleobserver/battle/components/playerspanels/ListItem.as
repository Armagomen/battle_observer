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
		
		public function ListItem(enemy:Boolean, width:Number)
		{
			super();
			this.isEnemy = enemy;
			this.x = enemy ? -width : width;
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
		
		public function addHealth(color:String, colorParams:Object, settings:Object, startVisible:Boolean):void
		{
			
			var barX:Number     = settings.players_bars_bar.x;
			var barWidth:Number = settings.players_bars_bar.width;
			var textX:Number    = settings.players_bars_text.x;
			var autoSize:String = settings.players_bars_text.align;
			if (this.isEnemy)
			{
				if (autoSize != "center")
				{
					autoSize = settings.players_bars_text.align == "left" ? "right" : "left";
				}
				barWidth = -barWidth;
				barX = -barX;
				textX = -textX;
			}
			this.healthBar = new ProgressBar(barX, settings.players_bars_bar.y, barWidth, settings.players_bars_bar.height, color, colorParams.bgColor, 0.2);
			if (settings.players_bars_bar.outline)
			{
				this.healthBar.setOutline(barWidth, settings.players_bars_bar.height);
			}
			this.healthBar.addTextField(textX, settings.players_bars_text.y, autoSize, Constants.normalText15);
			this.healthBar.setVisible(startVisible);
			this.addChild(this.healthBar);
		}
		
		public function updateHealth(percent:Number, text:String):void
		{
			if (this.healthBar)
			{
				this.healthBar.setNewScale(percent * 0.01);
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