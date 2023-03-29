package net.armagomen.battleobserver.battle.interfaces 
{
	/**
	 * ...
	 * @author ...
	 */
	public interface ITeamHealth 
	{
		function setColorBlind(enabled:Boolean):void;
		function setBarScale(isEnemy:Boolean, percent:Number):void;
		function update(alliesHP:int, enemiesHP:int, totalAlliesHP:int, totalEnemiesHP:int):void;
		function updateScore(ally:int, enemy:int):void;
		function remove():void;
	}
	
}