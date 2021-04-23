package net.armagomen.battleobserver.battle.components.teamshealth.classic {

import flash.display.*;
import flash.geom.ColorTransform;

import net.armagomen.battleobserver.data.Constants;
import net.armagomen.battleobserver.utils.Params;
import net.armagomen.battleobserver.utils.Utils;
import net.armagomen.battleobserver.utils.ProgressBar;

import net.armagomen.battleobserver.utils.tween.Tween;

/**
 * ...
 * @author ...
 */
public class Classic extends Sprite {

    {

        private var allyHpBar: ProgressBar;
        private var enemyHpBar: ProgressBar;
        private var colors: Object;
        [Embed(source="PAVLON.png")]
        private var PavlonBG: Class;

        public function Classic(name: String, colorBlind: Boolean, colors: Object) {
            super();
            this.colors = colors;

            this.allyHpBar = new ProgressBar(-50, 4, -150, 20, 0.6, 0, null, colors.ally, "allyBar");
            this.enemyHpBar = new ProgressBar(50, 4, 150, 20, 0.6, 0, null, colorBlind ? colors.enemyColorBlind : colors.enemy, "enemyBar");

            var bg: Bitmap = this.CreateBG(name);
            bg.x = -bg.width >> 1;
            bg.smoothing = true;
            bg.alpha = 0.8;

            this.addChild(bg);
            this.addChild(this.allyHpBar);
            this.addChild(this.enemyHpBar);
        }

        public function setColorBlind(enabled: Boolean): void {
            Utils.updateColor(this.enemyHpBar, enabled ? this.colors.enemyColorBlind : this.colors.enemy);
        }

        public function setBarScale(team: String, newScale: Number): void {
            if (team == "green") {
                this.allyHpBar.setNewScale(newScale);
            } else {
                this.enemyHpBar.setNewScale(newScale);
            }
        }

        private function CreateBG(name: String): Bitmap {
            switch (name) {
                case "pavlon":
                    return new PavlonBG();
                case "armagomen":
                    return new PavlonBG();
                default:
                    return new PavlonBG();
            }
        }
    }

}

}