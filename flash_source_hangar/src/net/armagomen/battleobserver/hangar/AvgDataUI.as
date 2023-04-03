package net.armagomen.battleobserver.hangar
{
	import flash.display.*;
	import flash.events.*;
	import flash.text.*;
	import net.armagomen.battleobserver.hangar.utils.Filters;
	import net.armagomen.battleobserver.hangar.utils.TextExt;
	import net.wg.infrastructure.base.BaseDAAPIComponent;
	
	public class AvgDataUI extends BaseDAAPIComponent
	{
		private var avgData:TextExt;
		
		public function AvgDataUI()
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
			var hangar:* = parent;
			var ammoPanel:* = hangar.ammunitionPanel;
			this.avgData = new TextExt(ammoPanel.width >> 1, ammoPanel.height - 2, Filters.mediumText, TextFieldAutoSize.CENTER, ammoPanel);
		}
		
		override protected function onDispose():void
		{
			this.avgData = null;
			super.onDispose();
		}
		
		public function as_setData(text:String):void
		{
			if (this.avgData)
			{
				this.avgData.htmlText = text;
			}
		}
	}
}