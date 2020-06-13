package net.armagomen.battleobserver.battle.utils
{
	import flash.display.*;
	import flash.events.Event;

	public class Animation extends MovieClip
	{
		private var newScale:Number = 1.0;
		private var oldScale:Number = 1.0;
		private var animationObject:Shape = null;
		private var speed:Number = 0.002
		private var inverted:Boolean = false;

		public function Animation(target:Shape, speed:Number, inverted:Boolean = false)
		{
			super();
			this.speed = speed;
			this.animationObject = target;
			this.oldScale = target.scaleX;
			this.inverted = inverted;
			if (this.inverted){
				this.oldScale = 0.01;
			}
		}

		public function setNewSpeed(speed:Number):void
		{
			this.speed = speed;
		}

		private function animateBar(event:Event):void
		{
			if (!inverted && this.oldScale > this.newScale)
			{
				this.animationObject.scaleX -= this.speed;
			}
			else if (inverted && this.oldScale < this.newScale)
			{
				this.animationObject.scaleX += this.speed;
			}
			else
			{
				this.animationObject.scaleX = this.newScale;
				this.animationObject.removeEventListener(Event.ENTER_FRAME, animateBar);
			}
			this.oldScale = this.animationObject.scaleX;
		}

		public function stopAnimation():void
		{
			if (this.animationObject.hasEventListener(Event.ENTER_FRAME))
			{
				this.animationObject.removeEventListener(Event.ENTER_FRAME, animateBar);
			}
		}

		public function runAnimation(newScale:Number):void
		{
			this.newScale = newScale;
			if (!this.animationObject.hasEventListener(Event.ENTER_FRAME))
			{
				this.animationObject.addEventListener(Event.ENTER_FRAME, animateBar, false, 0, true);
			}
		}
	}
}