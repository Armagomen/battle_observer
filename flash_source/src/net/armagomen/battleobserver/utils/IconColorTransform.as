package net.armagomen.battleobserver.utils 
{
	import flash.geom.ColorTransform;
	
	/**
	 * ...
	 * @author ...
	 */
	public class IconColorTransform extends ColorTransform 
	{
		
		public function IconColorTransform(redMultiplier:Number=1, greenMultiplier:Number=1, blueMultiplier:Number=1, alphaMultiplier:Number=1, redOffset:Number=0, greenOffset:Number=0, blueOffset:Number=0, alphaOffset:Number=0) 
		{
			super(redMultiplier, greenMultiplier, blueMultiplier, alphaMultiplier, redOffset, greenOffset, blueOffset, alphaOffset);
			
		}
		
	}

}