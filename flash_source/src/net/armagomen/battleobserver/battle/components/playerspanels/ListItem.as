package net.armagomen.battleobserver.battle.components.playerspanels
{
	import flash.display.Sprite;
	import net.armagomen.battleobserver.utils.ProgressBar;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class ListItem extends Sprite
	{
		private var healthBar:ProgressBar = null;
		private var damage:TextExt        = null;
		public var isEnemy:Boolean       = false;
		private var shadowSettings:Object = null;
		
		public function ListItem(enemy:Boolean, shadowSettings:Object)
		{
			super();
			this.isEnemy = enemy;
			this.shadowSettings = shadowSettings;
			this.x = enemy ? -381 : 380;
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
				this.damage = new TextExt(this.isEnemy ? -params.x : params.x, params.y, null, autoSize, this.shadowSettings, this);
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
			this.healthBar = new ProgressBar(barX, settings.players_bars_bar.y, barWidth, settings.players_bars_bar.height, colorParams.alpha, colorParams.bgAlpha, null, color, colorParams.bgColor, 0.6);
			if (settings.players_bars_bar.outline.enabled)
			{
				this.healthBar.setOutline(settings.players_bars_bar.outline.customColor, settings.players_bars_bar.outline.color, settings.players_bars_bar.outline.alpha, barWidth, settings.players_bars_bar.height);
			}
			this.healthBar.addTextField(textX, settings.players_bars_text.y, autoSize, null, shadowSettings);
			this.healthBar.setVisible(startVisible);
			this.addChild(this.healthBar);
		}
		
		public function updateHealth(scale:Number, text:String):void
		{
			if (this.healthBar)
			{
				this.healthBar.setNewScale(scale);
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