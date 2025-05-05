package net.armagomen.battle_observer.battle.components.debugpanel

{
	import flash.display.Bitmap;
	
	/**
	 * ...
	 * @author Armagomen
	 */
	public class LagIcons
	{
		[Embed(source = "ping_img/good.png")]
		private var good:Class;
		[Embed(source = "ping_img/bad.png")]
		private var bad:Class;
		[Embed(source = "ping_img/bad_cb.png")]
		private var bad_cb:Class;
		
		public var lag:Bitmap    = null;
		public var no_lag:Bitmap = null;
		
		public function LagIcons()
		{
			this.lag = App.colorSchemeMgr.getIsColorBlindS() ? new bad_cb() : new bad();
			this.no_lag = new good();
		}	
	}

}