package net.armagomen.battleobserver.battle.components.playerspanels
{
	import flash.display.Sprite;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.ProgressBar;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.wg.gui.battle.components.stats.playersPanel.SpottedIndicator;
	
	public class PlayersPanelsUI extends ObserverBattleDisplayable
	{
		private var playersPanel:* = null;
		private var items:Object   = new Object();
		private var storage:Object = new Object();
		public var onAddedToStorage:Function;
		
		public function PlayersPanelsUI(panels:*)
		{
			this.playersPanel = panels;
			super();
		}
		
		public function as_clearStorage():void
		{
			App.utils.data.cleanupDynamicObject(storage);
			App.utils.data.cleanupDynamicObject(items);
		}
		
		override protected function onDispose():void
		{
			this.as_clearStorage();
			super.onDispose();
		}
		
		public function as_AddVehIdToList(vehicleID:int, enemy:Boolean):void
		{
			var listitem:* = this.getListitem(vehicleID, enemy);
			if (listitem && !listitem.hasOwnProperty("battleObserver"))
			{
				var battleObserver:Sprite = new Sprite();
				battleObserver.name = "battleObserver";
				battleObserver.x = enemy ? -381 : 380;
				this.items[vehicleID] = listitem.addChild(battleObserver);
				this.storage[vehicleID] = new Object();
				this.onAddedToStorage(vehicleID, enemy);
			}
		}
		
		public function as_updatePPanelBar(vehicleID:int, scale:Number, text:String):void
		{
			if (this.storage.hasOwnProperty(vehicleID) && this.storage[vehicleID].hasOwnProperty("healthBar"))
			{
				var healthBar:ProgressBar = this.storage[vehicleID]["healthBar"];
				healthBar.setNewScale(scale);
				healthBar.setText(text);
				if (scale == 0)
				{
					healthBar.setVisible(false);
				}
			}
		}
		
		public function as_setHealthBarsVisible(vehicles:Array, vis:Boolean):void
		{
			for each (var vehicleID:int in vehicles)
			{
				if (this.storage.hasOwnProperty(vehicleID) && this.storage[vehicleID].hasOwnProperty("healthBar"))
				{
					var healthBar:ProgressBar = this.storage[vehicleID]["healthBar"];
					healthBar.setVisible(vis);
				}
			}
		}
		
		public function as_AddPPanelBar(vehicleID:int, color:String, colors:Object, settings:Object, team:String, startVisible:Boolean):void
		{
			if (this.storage.hasOwnProperty(vehicleID))
			{
				var barX:Number     = settings.players_bars_bar.x;
				var barWidth:Number = settings.players_bars_bar.width;
				var textX:Number    = settings.players_bars_text.x;
				var autoSize:String = settings.players_bars_text.align;
				if (team == "red")
				{
					if (autoSize != "center")
					{
						autoSize = settings.players_bars_text.align == "left" ? "right" : "left";
					}
					barWidth = -barWidth;
					barX = -barX;
					textX = -textX;
				}
				var healthBar:ProgressBar = new ProgressBar(this.animationEnabled(), barX, settings.players_bars_bar.y, barWidth, settings.players_bars_bar.height, colors.alpha, colors.bgAlpha, null, color, colors.bgColor, 0.6);
				if (settings.players_bars_bar.outline.enabled)
				{
					healthBar.setOutline(settings.players_bars_bar.outline.customColor, settings.players_bars_bar.outline.color, settings.players_bars_bar.outline.alpha);
				}
				healthBar.addTextField(textX, settings.players_bars_text.y, autoSize, null, getShadowSettings());
				healthBar.setVisible(startVisible);
				this.storage[vehicleID]["healthBar"] = this.items[vehicleID].addChild(healthBar);
			}
		}
		
		public function as_AddTextField(vehicleID:int, name:String, params:Object, team:String):void
		{
			if (this.storage.hasOwnProperty(vehicleID))
			{
				var autoSize:String = params.align;
				if (team == "red" && autoSize != "center")
				{
					autoSize = params.align == "left" ? "right" : "left";
				}
				this.storage[vehicleID][name] = new TextExt(team == "red" ? -params.x : params.x, params.y, null, autoSize, getShadowSettings(), items[vehicleID]);
				this.storage[vehicleID][name].visible = name != "DamageTf";
			}
		}
		
		public function as_updateTextField(vehicleID:int, name:String, text:String):void
		{
			if (this.storage.hasOwnProperty(vehicleID) && this.storage[vehicleID].hasOwnProperty(name))
			{
				this.storage[vehicleID][name].htmlText = text;
			}
		}
		
		public function as_setVehicleDead(vehicleID:int):void
		{
			if (this.items.hasOwnProperty(vehicleID))
			{
				this.items[vehicleID].alpha = 0.5;
				this.as_updatePPanelBar(vehicleID, 0, "")
			}
		}
		
		public function as_setSpottedPosition(vehicleID:int):void
		{
			var listitem:* = this.getListitem(vehicleID, true);
			if (listitem)
			{
				var spottedIndicator:SpottedIndicator = listitem.spottedIndicator;
				spottedIndicator.scaleX = spottedIndicator.scaleY = 1.5;
				spottedIndicator.y = -6;
				spottedIndicator.x = -335;
			}
			else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_setSpottedPosition - listitem is Null !!!");
		}
		
		public function as_colorBlindPPbars(vehicleID:int, hpColor:String):void
		{
			if (this.storage.hasOwnProperty(vehicleID) && this.storage[vehicleID].hasOwnProperty("healthBar"))
			{
				var healthBar:ProgressBar = this.storage[vehicleID]["healthBar"];
				healthBar.updateColor(hpColor);
			}
		}
		
		public function as_setPlayersDamageVisible(vis:Boolean):void
		{
			if (this.storage)
			{
				for each (var field:Object in this.storage)
				{
					field.DamageTf.visible = vis;
				}
			}
		}
		
		private function getListitem(vehicleID:int, enemy:Boolean):*
		{
			if (playersPanel)
			{
				var list:*   = enemy ? playersPanel.listRight : playersPanel.listLeft;
				var holder:* = list.getHolderByVehicleID(vehicleID);
				if (holder && holder.getListItem())
				{
					return holder.getListItem();
				}
				else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] getListitem - holder is Null !!!");
			}
			else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] getListitem - playersPanel is Null !!!");
			
			return null;
		}
	}
}