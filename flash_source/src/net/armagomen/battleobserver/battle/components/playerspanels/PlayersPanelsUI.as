package net.armagomen.battleobserver.battle.components.playerspanels
{
	
	public class PlayersPanelsUI extends PanelsStoarge
	{
		
		public function PlayersPanelsUI()
		{
			super();
		}
		
		public function as_AddVehIdToList(vehicle_id:int, enemy:Boolean):void
		{
			this.addVehicle(vehicle_id, enemy);
		}
		
		public function as_updatePPanelBar(vehID:int, scale:Number, text:String):void
		{
			this.updateHPBar(vehID, scale, text);
		}
		
		public function as_setHPbarsVisible(vehID:int, vis:Boolean):void
		{
			this.setHPbarVisible(vehID, vis);
		}
		
		public function as_AddPPanelBar(vehID:int, color:String, colors:Object, settings:Object, team:String, startVisible:Boolean):void
		{
			this.addHpBar(vehID, color, colors, settings, team, startVisible);
		}
		
		public function as_AddTextField(vehID:int, name:String, params:Object, team:String):void
		{
			this.createTextField(vehID, name, params, team);
		}
		
		public function as_updateTextField(vehID:int, name:String, text:String):void
		{
			this.updateTextField(vehID, name, text);
		}
		
		public function as_setSpottedPosition(vehID:int):void
		{
			this.setSpottedPosition(vehID);
		}
		
		public function as_setVehicleIconColor(vehID:int, color:String, multipler:Number, enemy:Boolean):void
		{
			this.setVehicleIconColor(vehID, color, multipler, enemy);
		}
		
		public function as_colorBlindPPbars(vehID:int, hpColor:String):void
		{
			this.colorBlindPPbars(vehID, hpColor);
		}
		
		public function as_setPlayersDamageVisible(vis:Boolean):void
		{
			this.setPlayersDamageVisible(vis);
		}
	}
}