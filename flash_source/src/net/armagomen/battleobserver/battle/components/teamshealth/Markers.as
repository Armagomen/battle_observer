package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.display.*;
	import flash.events.*;
	import flash.filters.*;
	import flash.text.*;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.gui.battle.components.*;
	
	public class Markers extends Sprite
	{
		private var allyM:TextExt;
		private var enemyM:TextExt;
		
		public function Markers(settings:Object, shadowSettings:Object, alpha:Number)
		{
			super();
			Filters.markersFormat.letterSpacing = 0.9;
			this.y = settings.y;
			
			this.allyM = new TextExt("allyM", -settings.x, 0, Filters.markersFormat, TextFieldAutoSize.RIGHT, shadowSettings, this);
			this.allyM.embedFonts = true;
			this.allyM.alpha = alpha;
			
			this.enemyM = new TextExt("enemyM", settings.x, 0, Filters.markersFormat, TextFieldAutoSize.LEFT, shadowSettings, this);
			this.enemyM.embedFonts = true;
			this.enemyM.alpha = alpha;
		}
		
		public function update_markers(correlationItemsLeft:String, correlationItemsRight:String):void
		{
			this.enemyM.htmlText = correlationItemsRight;
			this.allyM.htmlText = correlationItemsLeft;
		}
	}
}