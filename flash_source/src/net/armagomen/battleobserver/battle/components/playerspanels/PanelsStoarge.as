package net.armagomen.battleobserver.battle.components.playerspanels
{
	
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.geom.ColorTransform;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.ProgressBar;
	import net.armagomen.battleobserver.utils.TextExt;
	import net.armagomen.battleobserver.utils.Utils;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.BattleAtlasSprite;
	import net.wg.gui.battle.components.BattleDisplayable;
	import net.wg.gui.battle.components.stats.playersPanel.SpottedIndicator;
	
	
	public class PanelsStoarge extends BattleDisplayable
	{
		private var items:Object   = {};
		private var stoarge:Object = {};
		public var getShadowSettings:Function;
		public var animationEnabled:Function;
		private var loaded:Boolean = false;
		private var animate:Boolean = false;
		
		public function PanelsStoarge()
		{
			super();
		
		}
		
		override protected function configUI():void
		{
			super.configUI();
			this.tabEnabled = false;
			this.tabChildren = false;
			this.mouseEnabled = false;
			this.mouseChildren = false;
			this.buttonMode = false;
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			if (!this.loaded)
			{
				this.loaded = true;
				var battlePage:* = parent;
				var playersPanel:* = this.getPlayersPanel();
				var prebattleTimer:* = battlePage.getComponent(BATTLE_VIEW_ALIASES.PREBATTLE_TIMER);
				if (playersPanel && prebattleTimer)
				{
					var timerIndex:int = battlePage.getChildIndex(prebattleTimer);
					battlePage.setChildIndex(playersPanel, timerIndex - 1);
				}
				this.animate = this.animationEnabled();
			}
			else
			{
				App.utils.data.cleanupDynamicObject(items);
				App.utils.data.cleanupDynamicObject(stoarge);
			}
		
		}
		
		override protected function onDispose():void
		{
			App.utils.data.cleanupDynamicObject(stoarge);
			App.utils.data.cleanupDynamicObject(items);
			super.onDispose();
		}
		
		private function getPlayersPanel():*
		{
			var battlePage:*   = parent;
			var playersPanel:* = battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
			if (playersPanel)
			{
				return playersPanel;
			}
			return null;
		}
		
		public function addVehicle(vehicle_id:int):void
		{
			if (this.stoarge.hasOwnProperty(vehicle_id))
			{
				DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_AddVehIdToList - vehicle_id in stoarge !!!");
			}
			else
			{
				var playersPanel:* = this.getPlayersPanel();
				if (playersPanel)
				{
					var obse:Sprite = new Sprite();
					obse.name = "battleОbserver";
					obse.x = 380;
					var holder:* = playersPanel.listLeft.getHolderByVehicleID(vehicle_id);
					if (!holder)
					{
						obse.x = -obse.x;
						holder = playersPanel.listRight.getHolderByVehicleID(vehicle_id);
					}
					if (holder)
					{
						if (holder._listItem)
						{
							this.items[vehicle_id] = holder._listItem.addChild(obse);
							this.stoarge[vehicle_id] = {};
						}
						else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_AddVehIdToList - holder._listItem is Null !!!");
					}
					else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_AddVehIdToList - holder is Null !!!");
				}
				else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_AddVehIdToList - playersPanel is Null !!!");
			}
		}
		
		public function addHpBar(vehID:int, color:String, colors:Object, settings:Object, team:String, startVisible:Boolean):void
		{
			if (this.stoarge.hasOwnProperty(vehID.toString()))
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
				var bar:ProgressBar = new ProgressBar(this.animate, barX, settings.players_bars_bar.y, barWidth, settings.players_bars_bar.height, colors.alpha, colors.bgAlpha, null, color, colors.bgColor, vehID.toString());
				if (settings.players_bars_bar.outline.enabled)
				{
					bar.setOutline(settings.players_bars_bar.outline.customColor, settings.players_bars_bar.outline.color, settings.players_bars_bar.outline.alpha);
				}
				bar.addTextField(textX, settings.players_bars_text.y, autoSize, Filters.normalText, getShadowSettings());
				bar.setVisible(startVisible);
				this.stoarge[vehID]["HpBar"] = this.items[vehID].addChild(bar);
			}
			App.utils.data.cleanupDynamicObject(settings);
		}
		
		public function updateHPBar(vehID:int, currHP:Number, maxHP:Number, text:String):void
		{
			if (this.stoarge.hasOwnProperty(vehID.toString()))
			{
				var hpbar:ProgressBar = this.stoarge[vehID]["HpBar"];
				if (currHP > 0)
				{
					hpbar.setNewScale(currHP / maxHP);
					hpbar.setText(text);
				}
				else
				{
					this.items[vehID].removeChild(hpbar);
				}
			}
		}
		
		public function setHPbarVisible(vehID:int, vis:Boolean):void
		{
			if (this.stoarge.hasOwnProperty(vehID.toString()))
			{
				var hpbar:ProgressBar = this.stoarge[vehID]["HpBar"];
				hpbar.setVisible(vis);
			}
		}
		
		public function createTextField(vehID:int, name:String, params:Object, team:String):void
		{
			if (this.stoarge.hasOwnProperty(vehID.toString()))
			{
				var autoSize:String = params.align;
				if (team == "red" && autoSize != "center")
				{
					autoSize = params.align == "left" ? "right" : "left";
				}
				this.stoarge[vehID][name] = new TextExt(name, team == "red" ? -params.x : params.x, params.y, Filters.normalText, autoSize, getShadowSettings(), items[vehID]);
				this.stoarge[vehID][name].visible = name != "DamageTf";
			}
			App.utils.data.cleanupDynamicObject(params);
		}
		
		public function updateTextField(vehID:int, name:String, text:String):void
		{
			if (this.stoarge.hasOwnProperty(vehID.toString()))
			{
				this.stoarge[vehID][name].htmlText = text;
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
		
		private function getHolder(vehID:int, enemy:Boolean):*
		{
			try
			{
				var playersPanel:* = this.getPlayersPanel();
				if (playersPanel)
				{
					if (enemy)
					{
						return playersPanel.listRight.getHolderByVehicleID(vehID)._listItem;
					}
					else
					{
						return playersPanel.listLeft.getHolderByVehicleID(vehID)._listItem;
					}
				}
			}
			catch (err:Error)
			{
				return null;
			}
		}
		
		public function setSpottedPosition(vehID:int):void
		{
			var listitem:* = this.getHolder(vehID, true);
			if (listitem)
			{
				var spottedIndicator:SpottedIndicator = listitem.spottedIndicator;
				spottedIndicator.scaleX = spottedIndicator.scaleY = 1.5;
				spottedIndicator.y = -6;
				spottedIndicator.x = -335;
			}
			else
			{
				DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_setSpottedPosition - listitem is Null !!!");
			}
		}
		
		public function setVehicleIconColor(vehID:int, color:String, multipler:Number, enemy:Boolean):void
		{
			var listitem:* = this.getHolder(vehID, enemy);
			if (listitem)
			{
				var icon:BattleAtlasSprite = listitem.vehicleIcon;
				icon['battleObserver'] = {"color": Utils.colorConvert(color), "multipler": multipler};
				if (!icon.hasEventListener(Event.RENDER))
				{
					icon.addEventListener(Event.RENDER, this.onRenderHendle);
				}
			}
			else
			{
				DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_setVehicleIconColor - listitem is Null !!!");
			}
		}
		
		public function colorBlindPPbars(vehID:int, hpColor:String):void
		{
			if (this.stoarge.hasOwnProperty(vehID.toString()))
			{
				var hpbar:ProgressBar = this.stoarge[vehID]["HpBar"];
				hpbar.updateColor(hpColor);
			}
		}
		
		public function setPlayersDamageVisible(vis:Boolean):void
		{
			if (this.stoarge)
			{
				for each (var field:Object in this.stoarge)
				{
					field.DamageTf.visible = vis;
				}
			}
		}
	}

}