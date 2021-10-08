package net.armagomen.battleobserver.battle.components.playerspanels 
{
	import flash.display.Sprite;
	
	public class ListItem extentds Sprite
	{
		
		public function ListItem(enemy:Boolean) 
		{
			super();
			this.name = "battleObserver";
			this.x = enemy ? -381 : 380;
			
		}
		
	}

}