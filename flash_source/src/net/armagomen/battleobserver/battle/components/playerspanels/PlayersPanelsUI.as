package net.armagomen.battleobserver.battle.components.playerspanels
{
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.ProgressBar;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.utils.Utils;
	import net.wg.gui.battle.components.BattleAtlasSprite;
	import net.wg.gui.battle.components.stats.playersPanel.SpottedIndicator;
	import net.wg.gui.battle.components.stats.playersPanel.interfaces.IPlayersPanelListItem;
	import net.wg.gui.battle.random.views.stats.components.playersPanel.interfaces.IPlayersPanelListItemHolder;
	
	public class PlayersPanelsUI extends ObserverBattleDisplayable
	{
		private var playersPanel:*  = null;
		private var items:Object    = new Object();
		private var storage:Object  = new Object();
		public var onAddedToStorage:Function;
		private var animate:Boolean = false;
		
		public function PlayersPanelsUI(panels:*)
		{
			this.playersPanel = panels;
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			this.animate = this.animationEnabled();
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
			if (listitem && !listitem.hasOwnProperty("battleОbserver"))
			{
				var battleОbserver:Sprite = new Sprite();
				battleОbserver.name = "battleОbserver";
				battleОbserver.x = enemy ? -381 : 380;
				this.items[vehicleID] = listitem.addChild(battleОbserver);
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
		
		public function as_sethealthBarsVisible(vehicleID:int, vis:Boolean):void
		{
			if (this.storage.hasOwnProperty(vehicleID) && this.storage[vehicleID].hasOwnProperty("healthBar"))
			{
				var healthBar:ProgressBar = this.storage[vehicleID]["healthBar"];
				healthBar.setVisible(vis);
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
				var healthBar:ProgressBar = new ProgressBar(this.animate, barX, settings.players_bars_bar.y, barWidth, settings.players_bars_bar.height, colors.alpha, colors.bgAlpha, null, color, colors.bgColor, 0.6);
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
		
		public function as_setVehicleIconColor(vehicleID:int, color:String, multipler:Number, enemy:Boolean):void
		{
			var listitem:* = this.getListitem(vehicleID, enemy);
			if (listitem)
			{
				var icon:BattleAtlasSprite = listitem.vehicleIcon;
				icon['battleObserver'] = {"color": Utils.colorConvert(color), "multipler": multipler};
				if (!icon.hasEventListener(Event.RENDER))
				{
					icon.addEventListener(Event.RENDER, this.onRenderHendle);
				}
			}
			else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_setVehicleIconColor - listitem is Null !!!");
		}
		
		public function as_colorBlindPPbars(vehicleID:int, hpColor:String):void
		{
			if (this.storage.hasOwnProperty(vehicleID))
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
		
		private function onRenderHendle(eve:Event):void
		{
			var icon:BattleAtlasSprite = eve.target as BattleAtlasSprite;
			var tColor:ColorTransform  = icon.transform.colorTransform;
			tColor.color = icon['battleObserver']['color'];
			tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = icon['battleObserver']['multipler'];
			icon.transform.colorTransform = tColor;
		}
		
		private function getListitem(vehicleID:int, enemy:Boolean):IPlayersPanelListItem
		{
			if (playersPanel)
			{
				var list:*                             = enemy ? playersPanel.listRight : playersPanel.listLeft;
				var holder:IPlayersPanelListItemHolder = list.getHolderByVehicleID(vehicleID);
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