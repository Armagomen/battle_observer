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
		
		private var _lag:Bitmap    = App.colorSchemeMgr.getIsColorBlindS() ? new bad_cb() : new bad();
		private var _no_lag:Bitmap = new good();
		
		public function LagIcons()
		{
		
		}
		
		public function get lag():Bitmap  { return this._lag; }
		
		public function get no_lag():Bitmap  { return this._no_lag; }
	
	}

}