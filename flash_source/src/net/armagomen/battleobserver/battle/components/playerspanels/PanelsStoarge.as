package net.armagomen.battleobserver.battle.components.playerspanels {

import flash.display.Sprite;
import flash.events.Event;
import flash.geom.ColorTransform;

import net.armagomen.battleobserver.battle.utils.Filters;
import net.armagomen.battleobserver.battle.utils.Params;
import net.armagomen.battleobserver.battle.utils.ProgressBar;
import net.armagomen.battleobserver.battle.utils.TextExt;
import net.armagomen.battleobserver.battle.utils.Utils;
import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
import net.wg.gui.battle.components.BattleAtlasSprite;
import net.wg.gui.battle.components.BattleDisplayable;

public class PanelsStoarge extends BattleDisplayable {
    private var items: Object = {};
    private var stoarge: Object = {};
    public var getShadowSettings: Function;

    public function PanelsStoarge() {
        super();

    }

    override protected function configUI(): void {
        super.configUI();
        this.tabEnabled = false;
        this.tabChildren = false;
        this.mouseEnabled = false;
        this.mouseChildren = false;
        this.buttonMode = false;
    }

    override protected function onPopulate(): void {
        super.onPopulate();
        var playersPanel: * = this.getPlayersPanel();
        if (playersPanel) {
            var battlePage: * = parent;
            var timerIndex: int = battlePage.getChildIndex(battlePage.getComponent(BATTLE_VIEW_ALIASES.PREBATTLE_TIMER));
            battlePage.setChildIndex(playersPanel, timerIndex - 1);
        }
    }

    private function getPlayersPanel(): * {
        var battlePage: * = parent;
        if (battlePage._componentsStorage.hasOwnProperty(BATTLE_VIEW_ALIASES.PLAYERS_PANEL)) {
            return battlePage.getComponent(BATTLE_VIEW_ALIASES.PLAYERS_PANEL);
        }
        battlePage.unregisterComponent(this.name);
        return null;
    }

    public function as_clearScene(): void {
        if (this.stoarge) {
            App.utils.data.cleanupDynamicObject(this.stoarge);
        }
        if (this.items) {
            App.utils.data.cleanupDynamicObject(this.items);
        }
        var page: * = parent;
        page.unregisterComponent(this.name);
    }

    public function addVehicle(vehicle_id: int): void {
        if (this.stoarge.hasOwnProperty(vehicle_id)) {
            DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_AddVehIdToList - vehicle_id in stoarge !!!");
        } else {
            var playersPanel: * = this.getPlayersPanel();
            if (playersPanel) {
                var obse: Sprite = new Sprite();
                obse.name = "battleОbserver";
                obse.x = 380;
                var holder: * = playersPanel.listLeft.getHolderByVehicleID(vehicle_id);
                if (!holder) {
                    obse.x = -obse.x;
                    holder = playersPanel.listRight.getHolderByVehicleID(vehicle_id);
                }
                if (holder) {
                    if (holder._listItem) {
                        this.items[vehicle_id] = holder._listItem.addChild(obse);
                        this.stoarge[vehicle_id] = {};
                    } else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_AddVehIdToList - holder._listItem is Null !!!");
                } else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_AddVehIdToList - holder is Null !!!");
            } else DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_AddVehIdToList - playersPanel is Null !!!");
        }
    }

    public function addHpBar(vehID: int, color: String, settings: Object, team: String, startVisible: Boolean): void {
        if (this.stoarge.hasOwnProperty(vehID.toString())) {
            var barX: Number = settings.bar.x;
            var barWidth: Number = settings.bar.width;
            var textX: Number = settings.text.x;
            var autoSize: String = settings.text.align;
            if (team == "red") {
                if (autoSize != "center") {
                    autoSize = settings.text.align == "left" ? "right" : "left";
                }
                barWidth = -barWidth;
                barX = -barX;
                textX = -textX;
            }
            var bar: ProgressBar = new ProgressBar(barX, settings.bar.y, barWidth, settings.bar.height, settings.bar.colors.alpha, settings.bar.colors.bgAlpha, null, color, settings.bar.colors.bgColor, vehID.toString());
            if (settings.bar.outline.enabled) {
                bar.setOutline(settings.bar.outline.customColor, settings.bar.outline.color, settings.bar.outline.alpha);
            }
            bar.addTextField(textX, settings.text.y, autoSize, Filters.normalText, getShadowSettings());
            bar.setVisible(startVisible);
            this.stoarge[vehID]["HpBar"] = items[vehID].addChild(bar);
        }
        App.utils.data.cleanupDynamicObject(settings);
    }

    public function updateHPBar(vehID: int, currHP: Number, maxHP: Number, text: String): void {
        if (this.stoarge.hasOwnProperty(vehID.toString())) {
            var hpbar: ProgressBar = this.stoarge[vehID]["HpBar"];
            if (currHP > 0) {
                hpbar.visible && Params.AnimationEnabled ? hpbar.setBarScale(currHP / maxHP) : hpbar.bar.scaleX = currHP / maxHP;
            } else {
                hpbar.bar.scaleX = 0;
                hpbar.setVisible(false);
                this.items[vehID].removeChild(hpbar);
            }
            hpbar.uiText.htmlText = text;
        }
    }

    public function setHPbarVisible(vehID: int, vis: Boolean): void {
        if (this.stoarge.hasOwnProperty(vehID.toString())) {
            var hpbar: ProgressBar = this.stoarge[vehID]["HpBar"];
            hpbar.setVisible(vis && hpbar.bar.scaleX > 0);
        }
    }

    public function createTextField(vehID: int, name: String, params: Object, team: String): void {
        if (this.stoarge.hasOwnProperty(vehID.toString())) {
            var autoSize: String = params.align;
            if (team == "red" && autoSize != "center") {
                autoSize = params.align == "left" ? "right" : "left";
            }
            this.stoarge[vehID][name] = new TextExt(name, team == "red" ? -params.x : params.x, params.y, Filters.normalText, autoSize, getShadowSettings(), items[vehID]);
            this.stoarge[vehID][name].visible = name != "DamageTf";
        }
        App.utils.data.cleanupDynamicObject(params);
    }

    public function updateTextField(vehID: int, name: String, text: String): void {
        if (this.stoarge.hasOwnProperty(vehID.toString())) {
            this.stoarge[vehID][name].htmlText = text;
        }
    }

    private function onRenderHendle(eve: Event): void {
        var icon: BattleAtlasSprite = eve.target as BattleAtlasSprite;
        var tColor: ColorTransform = icon.transform.colorTransform;
        tColor.color = icon['battleObserver']['color'];
        tColor.redMultiplier = tColor.greenMultiplier = tColor.blueMultiplier = icon['battleObserver']['multipler'];
        icon.transform.colorTransform = tColor;
    }

    private function getHolder(vehID: int, enemy: Boolean): * {
        try {
            var playersPanel: * = this.getPlayersPanel();
            if (playersPanel) {
                if (enemy) {
                    return playersPanel.listRight.getHolderByVehicleID(vehID)._listItem;
                } else {
                    return playersPanel.listLeft.getHolderByVehicleID(vehID)._listItem;
                }
            }
        } catch (err: Error) {
            return null;
        }
    }

    public function setVehicleIconColor(vehID: int, color: String, multipler: Number, enemy: Boolean): void {
        var listitem: * = this.getHolder(vehID, enemy);
        if (listitem) {
            var icon: BattleAtlasSprite = listitem.vehicleIcon;
            icon['battleObserver'] = {"color": Utils.colorConvert(color), "multipler": multipler};
            if (!icon.hasEventListener(Event.RENDER)) {
                icon.addEventListener(Event.RENDER, this.onRenderHendle);
            }
        } else {
            DebugUtils.LOG_WARNING("[BATTLE_OBSERVER_INFO] as_setVehicleIconColor - listitem is Null !!!");
        }
    }

    public function colorBlindPPbars(vehID: int, hpColor: String): void {
        if (this.stoarge.hasOwnProperty(vehID.toString())) {
            var hpbar: ProgressBar = this.stoarge[vehID]["HpBar"];
            var colorInfo: ColorTransform = hpbar.bar.transform.colorTransform;
            colorInfo.color = Utils.colorConvert(hpColor);
            hpbar.bar.transform.colorTransform = colorInfo;
        }
    }

    public function setPlayersDamageVisible(vis: Boolean): void {
        if (this.stoarge) {
            for each (var field: Object in this.stoarge) {
                field.DamageTf.visible = vis;
            }
        }
    }
}

}