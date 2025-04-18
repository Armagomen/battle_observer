package net.armagomen.battle_observer.battle.components.statistics.components.base
{
	/**
	 * ...
	 * @author Armagomen
	 */
	
	import flash.geom.ColorTransform;
	import flash.text.TextFormat;
	import flash.utils.clearTimeout;
	import net.armagomen.battle_observer.utils.Utils;
	
	public class BaseStatisticsComponent
	{
		public var component:*                     = null;
		public var timeoutID:Number                = 0;
		public var format:TextFormat               = null;
		private var iconColors:Object              = {};
		public var statisticsData:Object           = {};
		public var iconsEnabled:Boolean            = false;
		public var iconMultiplier:Number           = -1.25;
		public var cutWidth:Number                 = 60.0;
		public var fullWidth:Number                = 150.0;
		public static const DEAD_TEXT_ALPHA:Number = 0.65;
		
		public function BaseStatisticsComponent(component:*)
		{
			this.component = component;
			this.format = new TextFormat();
			this.format.bold = true;
		}
		
		public function updateVehicleIconColor(vehicleIcon:*, vehicleType:String):void
		{
			var tColor:ColorTransform = vehicleIcon.transform.colorTransform;
			tColor.color = this.iconColors[vehicleType];
			tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = this.iconMultiplier;
			vehicleIcon.transform.colorTransform = tColor;
		}
		
		public function get visible():Boolean
		{
			return this.component.visible;
		}
		
		public function removeTimeout():void
		{
			if (this.timeoutID)
			{
				clearTimeout(this.timeoutID);
			}
		}
		
		public function setIconColors(colors:Object):void
		{
			for (var classTag:String in colors)
			{
				this.iconColors[classTag] = Utils.colorConvert(colors[classTag]);
			}
		}
		
		public function setSettings(settings:Object):void
		{
			this.iconMultiplier = settings["icons_blackout"];
			this.iconsEnabled = settings["icons"];
			this.cutWidth = settings["statistics_panels_cut_width"];
			this.fullWidth = settings["statistics_panels_full_width"];
		}
		
		public function set_wgr_data(statsData:Object):void
		{
			for (var key:String in statsData)
			{
				this.statisticsData[key] = statsData[key];
			}
		}
	}

}