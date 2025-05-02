package net.armagomen.battle_observer.battle.components.maingun
{
	import flash.display.Bitmap;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.text.TextFieldAutoSize;
	import net.armagomen.battle_observer.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battle_observer.utils.Constants;
	import net.armagomen.battle_observer.utils.TextExt;
	import net.armagomen.battle_observer.utils.ProgressBar;
	
	public class MainGunUI extends ObserverBattleDisplayable
	{
		[Embed(source = "img/main_gun.png")]
		private var _gun:Class;
		[Embed(source = "img/done.png")]
		private var _done:Class;
		[Embed(source = "img/warning_1.png")]
		private var _warn:Class;
		[Embed(source = "img/warning_2.png")]
		private var _warn_cb:Class;
		
		private var icons:Vector.<Bitmap> = null;
		private var mainGun:TextExt       = null;
		private var progress:ProgressBar;
		
		public function MainGunUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			
			if (not_initialized)
			{
				super.onPopulate();
				var _icons:Sprite = new Sprite();
				_icons.y = 2;
				this.addChild(_icons);
				if (!this.icons)
				{
					this.icons = new <Bitmap>[new this._gun(), new this._done(), App.colorSchemeMgr.getIsColorBlindS() ? new this._warn_cb() : new this._warn()];
					this.icons.fixed = true;
				}
				
				for each (var item:Bitmap in this.icons)
				{
					item.width = 26;
					item.height = 26;
					item.visible = false;
					_icons.addChild(item);
				}
				this.icons[0].visible = true;
				this.icons[2].alpha = 0.6;
				
				var settings:Object = this.getSettings();
				this.x = (App.appWidth >> 1) + settings.x;
				this.y = settings.y;
				if (settings.progress_bar)
				{
					var colors:Object = this.getColors().global;
					this.mainGun = new TextExt(50, 0, Constants.middleText, TextFieldAutoSize.CENTER, this);
					this.progress = new ProgressBar(30, 24, 42, 4, colors.ally, colors.bgColor, 0.2);
					this.progress.setNewScale(0);
					this.addChild(this.progress);
				}
				else
				{
					this.mainGun = new TextExt(28, 0, Constants.largeText, TextFieldAutoSize.LEFT, this);
				}
			}
			else
			{
				super.onPopulate();
			}
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.mainGun = null;
			this.progress = null;
		}
		
		private function setDoneVisible(value:Boolean):void
		{
			if (this.icons[1].visible != value)
			{
				this.icons[1].visible = value
			}
		}
		
		private function setWarningVisible(value:Boolean):void
		{
			if (this.icons[2].visible != value)
			{
				this.icons[2].visible = value
			}
		}
		
		public function as_gunData(damage:int, gun_score:int, warning:Boolean):void
		{
			var value:int = gun_score - damage;
			var notAchived:Boolean = value > 0;
			if (notAchived)
			{
				this.mainGun.text = value.toString();
			}
			else
			{
				this.mainGun.text = "++" + Math.abs(value).toString();
			}
			if (this.progress)
			{
				this.progress.setNewScale(Math.min(1.0, damage / gun_score))
			}
			this.setWarningVisible(warning);
			this.setDoneVisible(!notAchived);
		}
		
		override public function onResizeHandle(event:Event):void
		{
			this.x = (App.appWidth >> 1) + this.getSettings().x;
		}
	}
}