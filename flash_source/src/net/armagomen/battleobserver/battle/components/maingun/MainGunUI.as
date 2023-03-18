package net.armagomen.battleobserver.battle.components.maingun
{
	import flash.display.Bitmap;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.utils.Filters;
	import net.armagomen.battleobserver.utils.TextExt;
	
	public class MainGunUI extends ObserverBattleDisplayable
	{
		[Embed(source = "img/main_gun.png")]
		private var Gun_icon:Class;
		[Embed(source = "img/done.png")]
		private var Done_icon:Class;
		[Embed(source = "img/warning_1.png")]
		private var Warning_icon:Class;
		[Embed(source = "img/warning_2.png")]
		private var Warning_icon_cb:Class;
		
		private var icons:Vector.<Bitmap> = null;
		private var mainGun:TextExt       = null;
		
		public function MainGunUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			this.icons = new <Bitmap>[new Gun_icon(), new Done_icon(), this.isColorBlind() ? new Warning_icon_cb() : new Warning_icon()];
			this.icons.fixed = true;
			
			var gun_icon:Bitmap     = this.icons[0];
			var done_icon:Bitmap    = this.icons[1];
			var warning_icon:Bitmap = this.icons[2];
			
			var _icons:Sprite       = new Sprite();
			_icons.y = 2;
			this.addChild(_icons);
			
			gun_icon.width = 26;
			gun_icon.height = 26;
			_icons.addChild(gun_icon);
			
			done_icon.width = 24;
			done_icon.height = 24;
			done_icon.x = 2;
			done_icon.y = 2;
			done_icon.visible = false;
			_icons.addChild(done_icon);
			
			warning_icon.width = 26;
			warning_icon.height = 26;
			warning_icon.alpha = 0.7;
			warning_icon.visible = false;
			_icons.addChild(warning_icon);
			
			var settings:Object = this.getSettings();
			this.x = (App.appWidth >> 1) + settings.x;
			this.y = settings.y;
			this.mainGun = new TextExt(28, 0, Filters.largeText, TextFieldAutoSize.LEFT, getShadowSettings(), this);
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.mainGun = null;
		}
		
		public function as_gunData(value:int, warning:Boolean):void
		{
			this.icons[2].visible = warning && value > 0;
			if (value > 0)
			{
				this.mainGun.text = value.toString();
			}
			else
			{
				this.mainGun.text = "+" + Math.abs(value).toString();
				this.icons[1].visible = true;
			}
		}
		
		override public function onResizeHandle(event:Event):void
		{
			this.x = (App.appWidth >> 1) + this.getSettings().x;
		}
	}
}