package net.armagomen.battle_observer.battle.components
{
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.text.TextField;
	import flash.text.TextFieldAutoSize;
	import flash.utils.Dictionary;
	import flash.utils.setTimeout;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	import net.wg.gui.battle.components.events.PlayersPanelListEvent;
	import net.wg.gui.battle.random.views.stats.components.playersPanel.events.PlayersPanelEvent;
	
	public class Statistics extends ObserverBattleDisplayable
	{
		private var battleLoading:* = null;
		private var panels:* = null;
		private var statisticsData:Dictionary = new Dictionary();
		private var statisticsLoaded:Boolean = false;
		private static const DEAD_ALPHA:Number = 0.7;
		
		public function Statistics()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			if (this.notInitialized())
			{
				this.panels = this.battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
				this.battleLoading = this.battlePage.getComponent(BATTLE_VIEW_ALIASES.BATTLE_LOADING);
				this.addListeners();
			}
		}
		
		private function addListeners():void
		{
			this.panels.addEventListener(Event.CHANGE, this.as_updateALL, false, 0, true);
			this.panels.addEventListener(MouseEvent.MOUSE_OVER, this.as_updateALL, false, 0, true);
			this.panels.addEventListener(MouseEvent.MOUSE_OUT, this.as_updateALL, false, 0, true);
			this.panels.addEventListener(PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.as_updateALL, false, 0, true);
			if (this.panels.listRight)
			{
				this.panels.listRight.addEventListener(PlayersPanelListEvent.ITEMS_COUNT_CHANGE, this.as_updateALL, false, 0, true);
			}
		}
		
		override protected function onBeforeDispose():void
		{
			this.removeListeners();
			App.utils.data.cleanupDynamicObject(this.statisticsData);
			this.battleLoading = null;
			this.panels = null;
			super.onBeforeDispose();
		}
		
		private function removeListeners():void
		{
			this.removeListener(this.panels, Event.CHANGE, this.as_updateALL);
			this.removeListener(this.panels, MouseEvent.MOUSE_OVER, this.as_updateALL);
			this.removeListener(this.panels, MouseEvent.MOUSE_OUT, this.as_updateALL);
			this.removeListener(this.panels, PlayersPanelEvent.ON_ITEMS_COUNT_CHANGE, this.as_updateALL);
			
			if (this.panels.listRight)
			{
				this.removeListener(this.panels.listRight, PlayersPanelListEvent.ITEMS_COUNT_CHANGE, this.as_updateALL);
			}
		}
		
		private function removeListener(target:*, type:String, listener:Function):void
		{
			if (!target) return;
			if (target.hasEventListener(type))
			{
				target.removeEventListener(type, listener);
			}
		}

		
		public function as_updateALL(e:* = null):void
		{
			setTimeout(this.updateTextItems, 200, e);
		}
		
		//private function cloneTextField(original:TextField, isEnemy:Boolean):void
		//{
			//var copy:TextField = new TextField();
			//
			//copy.text = original.text;
			//copy.htmlText = original.htmlText;
			//copy.defaultTextFormat = original.defaultTextFormat;
			//copy.autoSize = original.autoSize;
			//copy.multiline = original.multiline;
			//copy.wordWrap = original.wordWrap;
			//copy.selectable = original.selectable;
			//copy.embedFonts = original.embedFonts;
			//
			//copy.x = original.x;
			//copy.y = original.y;
			//copy.scaleX = original.scaleX;
			//copy.scaleY = original.scaleY;
			//copy.rotation = original.rotation;
			//
			//if (isEnemy)
			//{
				//copy.scaleY *= -1;
			//}
			//
			//if (original.parent)
			//{
				//var parent:DisplayObjectContainer = original.parent;
				//var idx:int = parent.getChildIndex(original);
				//
				//parent.removeChild(original);
				//parent.addChildAt(copy, idx);
			//}
		//}
		
		public function as_update_wgr_data(statsData:Object):void
		{
			for (var key:String in statsData)
			{
				this.statisticsData[int(key)] = statsData[key];
			}
			App.utils.data.cleanupDynamicObject(statsData);
			this.statisticsLoaded = true;
		}
		
		private function updateTextItems(eve:* = null):void
		{
			var targetList:Array = eve && eve.type == PlayersPanelListEvent.ITEMS_COUNT_CHANGE ? [eve.target] : [this.panels.listLeft, this.panels.listRight];
			for each (var list:* in targetList)
			{
				for each (var item:* in list._items)
				{
					if (!item || !item._listItem) continue;
					this.updateStatisticsByItem(item, item._listItem._isRightAligned);
				}
			}
		}
		
		private function setVehicleTextColor(field:TextField, vehicleTextColor:uint):void
		{
			if (vehicleTextColor > 0 && field.textColor != vehicleTextColor)
			{
				field.textColor = vehicleTextColor;
			}
		}
		
		private function updateHtmlText(field:TextField, htmlText:String):void
		{
			field.htmlText = htmlText;
		}
		
		private function updateAutoSize(field:TextField, autoSize:String):void
		{
			if (field.autoSize != autoSize)
			{
				field.autoSize = autoSize;
			}
		}
		
		public function as_updateByVehicleID(vehicleID:int, isEnemy:Boolean):void
		{
			setTimeout(this.updateByVehicleID, 200, vehicleID, isEnemy);
		}
		
		private function updateByVehicleID(vehicleID:int, isEnemy:Boolean):void
		{
			var item:* = this.getPanelHolderByVehicleID(vehicleID, isEnemy);
			if (!item || !item._listItem) return;
			this.updateStatisticsByItem(item, isEnemy);
		}
		
		private function updateStatisticsByItem(item:*, isEnemy:Boolean):void
		{
			
			if (this.statisticsLoaded)
			{
				var data:Object = this.statisticsData[item.vehicleData.vehicleID];
				if (!data) return;
				
				this.setVehicleTextColor(item._listItem.vehicleTF, data.vehicleTextColor);
				this.updateHtmlText(item._listItem.playerNameFullTF, data.fullName);
				this.updateHtmlText(item._listItem.playerNameCutTF, data.cutName);
				
				//this.cloneTextField(item._listItem.vehicleTF, isEnemy);
				//this.cloneTextField(item._listItem.playerNameFullTF, isEnemy);
				//this.cloneTextField(item._listItem.playerNameCutTF, isEnemy);
				
				if (this.battleLoading.visible)
				{
					var loadingHolder:* = this.getLoadingHolderByVehicleID(item.vehicleData.vehicleID, isEnemy);
					this.updateAutoSize(loadingHolder._textField, loadingHolder._isEnemy ? TextFieldAutoSize.RIGHT : TextFieldAutoSize.LEFT)
					this.updateHtmlText(loadingHolder._textField, data.fullName);
					//this.cloneTextField(loadingHolder._textField, isEnemy);
					if (loadingHolder._vehicleField)
					{
						this.setVehicleTextColor(loadingHolder._vehicleField, data.vehicleTextColor);
							//this.cloneTextField(loadingHolder._vehicleField, isEnemy);
					}
				}
				
				if (!item._listItem.isAlive && item._listItem.playerNameFullTF.alpha != DEAD_ALPHA)
				{
					item._listItem.playerNameFullTF.alpha = item._listItem.playerNameCutTF.alpha = item._listItem.vehicleTF.alpha = DEAD_ALPHA;
				}
			}
		
		}
		
		// holder getters
		
		private function getPanelHolderByVehicleID(vehicleID:int, isEnemy:Boolean):*
		{
			var list:* = isEnemy ? this.panels.listRight : this.panels.listLeft;
			for each (var item:* in list._items)
			{
				if (item.vehicleData.vehicleID == vehicleID)
				{
					return item;
				}
			}
			return null;
		}
		
		private function getLoadingHolderByVehicleID(vehicleID:int, isEnemy:Boolean):*
		{
			var form:* = this.battleLoading.form;
			if (form)
			{
				var renderers:* = isEnemy ? form._enemyRenderers : form._allyRenderers;
				for each (var render:* in renderers)
				{
					if (render.model.vehicleID == vehicleID)
					{
						return render;
					}
				}
			}
			return null;
		}
	}
}