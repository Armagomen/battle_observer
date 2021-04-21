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
		private var items:Object    = {};
		private var stoarge:Object  = {};
		public var getShadowSettings:Function;
		public var animationEnabled:Function;
		public var onAddedToStorage:Function;
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
			this.animate = this.animationEnabled();
			//var battlePage:*     = parent;
			//var prebattleTimer:* = battlePage.getComponent(BATTLE_VIEW_ALIASES.PREBATTLE_TIMER);
			//var playersPanel:* = battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
			//if (playersPanel && prebattleTimer)
			//{
				//var timerIndex:int = battlePage.getChildIndex(prebattleTimer);
				//battlePage.setChildIndex(playersPanel, timerIndex - 1);
			//}
		}
		
		public function as_clearStorage():void
		{
			App.utils.data.cleanupDynamicObject(stoarge);
			App.utils.data.cleanupDynamicObject(items);
		}
		
		override protected function onDispose():void
		{
			this.as_clearStorage();
			super.onDispose();
		}
		
		public function addVehicle(vehID:int, enemy:Boolean):void
		{
			if (this.stoarge.hasOwnProperty(vehID))
			{
				DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_AddVehIdToList - vehicle_id in stoarge !!!");
			}
			else
			{
				var listitem:* = this.getListitem(vehID, enemy);
				if (listitem)
				{
					var obse:Sprite = new Sprite();
					obse.name = "battleОbserver";
					obse.x = enemy ? -380 : 380;
					this.items[vehID] = listitem.addChild(obse);
					this.stoarge[vehID] = {};
					this.onAddedToStorage(vehID, enemy);
				}
			}
		}
		
		public function addHpBar(vehID:int, color:String, colors:Object, settings:Object, team:String, startVisible:Boolean):void
		{
			if (this.stoarge.hasOwnProperty(vehID))
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
			if (this.stoarge.hasOwnProperty(vehID))
			{
				var hpbar:ProgressBar = this.stoarge[vehID]["HpBar"];
				if (currHP > 0)
				{
					hpbar.setNewScale(currHP / maxHP);
					hpbar.setText(text);
				}
				else
				{
					hpbar.setVisible(false);
				}
			}
		}
		
		public function setHPbarVisible(vehID:int, vis:Boolean):void
		{
			if (this.stoarge.hasOwnProperty(vehID))
			{
				var hpbar:ProgressBar = this.stoarge[vehID]["HpBar"];
				hpbar.setVisible(vis);
			}
		}
		
		public function createTextField(vehID:int, name:String, params:Object, team:String):void
		{
			if (this.stoarge.hasOwnProperty(vehID))
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
			if (this.stoarge.hasOwnProperty(vehID))
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
		
		private function getListitem(vehID:int, enemy:Boolean):*
		{
			try
			{
				var battlePage:*   = parent;
				var playersPanel:* = battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
				if (playersPanel)
				{
					var list:*   = enemy ? playersPanel.listRight : playersPanel.listLeft;
					var holder:* = list.getHolderByVehicleID(vehID);
					if (holder && holder._listItem)
					{
						return holder._listItem;
					}
					else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] getListitem - holder is Null !!!");
				}
				else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] getListitem - playersPanel is Null !!!");
			}
			catch (err:Error)
			{
				return null;
			}
		}
		
		public function setSpottedPosition(vehID:int):void
		{
			var listitem:* = this.getListitem(vehID, true);
			if (listitem)
			{
				var spottedIndicator:SpottedIndicator = listitem.spottedIndicator;
				spottedIndicator.scaleX = spottedIndicator.scaleY = 1.5;
				spottedIndicator.y = -6;
				spottedIndicator.x = -335;
			}
			else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_setSpottedPosition - listitem is Null !!!");

		}
		
		public function setVehicleIconColor(vehID:int, color:String, multipler:Number, enemy:Boolean):void
		{
			var listitem:* = this.getListitem(vehID, enemy);
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
		
		public function colorBlindPPbars(vehID:int, hpColor:String):void
		{
			if (this.stoarge.hasOwnProperty(vehID))
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