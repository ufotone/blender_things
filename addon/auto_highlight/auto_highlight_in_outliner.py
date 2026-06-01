bl_info = {
    "name": "Auto Highlight in Outliner",
    "author": "Codex",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Item > Outliner",
    "description": "Automatically expands the Outliner and highlights the active selected object.",
    "category": "3D View",
}

import bpy
from bpy.props import BoolProperty, FloatProperty


_last_selection_key = None
_timer_running = False


def _selection_key(context):
    view_layer = context.view_layer
    active = view_layer.objects.active
    selected = tuple(sorted(obj.name_full for obj in context.selected_objects))
    return (active.name_full if active else "", selected)


def _outliner_regions(area):
    for region in area.regions:
        if region.type == "WINDOW":
            yield region


def highlight_active_in_outliners():
    """Reveal the active object in every visible Outliner editor."""
    context = bpy.context
    active = context.view_layer.objects.active
    if active is None:
        return False

    found_outliner = False

    for window in context.window_manager.windows:
        screen = window.screen
        if screen is None:
            continue

        for area in screen.areas:
            if area.type != "OUTLINER":
                continue

            found_outliner = True
            space = area.spaces.active
            previous_display_mode = getattr(space, "display_mode", None)
            prefs = context.preferences.addons[__name__].preferences

            # VIEW_LAYER is the mode where selected scene objects can be revealed reliably.
            if (
                prefs.force_view_layer_mode
                and previous_display_mode is not None
                and previous_display_mode != "VIEW_LAYER"
            ):
                space.display_mode = "VIEW_LAYER"

            for region in _outliner_regions(area):
                with context.temp_override(
                    window=window,
                    screen=screen,
                    area=area,
                    region=region,
                    space_data=space,
                    active_object=active,
                    selected_objects=context.selected_objects,
                ):
                    try:
                        bpy.ops.outliner.show_active("EXEC_DEFAULT")
                    except RuntimeError:
                        # Some Outliner states are not revealable; keep other editors working.
                        pass

    return found_outliner


def _timer_tick():
    global _last_selection_key, _timer_running

    prefs = bpy.context.preferences.addons[__name__].preferences
    if not prefs.enabled:
        _timer_running = False
        return None

    current_key = _selection_key(bpy.context)
    if current_key != _last_selection_key:
        _last_selection_key = current_key
        highlight_active_in_outliners()

    return max(0.05, prefs.poll_interval)


def ensure_timer():
    global _timer_running
    if not _timer_running:
        _timer_running = True
        bpy.app.timers.register(_timer_tick, first_interval=0.05, persistent=True)


class AHIO_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    enabled: BoolProperty(
        name="Auto Highlight",
        description="Automatically reveal the active object in the Outliner when selection changes",
        default=True,
        update=lambda self, context: ensure_timer() if self.enabled else None,
    )

    poll_interval: FloatProperty(
        name="Poll Interval",
        description="How often selection changes are checked, in seconds",
        default=0.15,
        min=0.05,
        max=2.0,
        subtype="TIME",
    )

    force_view_layer_mode: BoolProperty(
        name="Use View Layer Mode",
        description="Switch Outliner editors to View Layer mode before revealing objects",
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "enabled")
        layout.prop(self, "poll_interval")
        layout.prop(self, "force_view_layer_mode")


class AHIO_OT_show_active(bpy.types.Operator):
    bl_idname = "ahio.show_active"
    bl_label = "Highlight Active in Outliner"
    bl_description = "Expand the Outliner and highlight the active selected object"
    bl_options = {"REGISTER"}

    def execute(self, context):
        if context.view_layer.objects.active is None:
            self.report({"WARNING"}, "No active object to highlight")
            return {"CANCELLED"}

        found = highlight_active_in_outliners()
        if not found:
            self.report({"WARNING"}, "No visible Outliner editor found")
            return {"CANCELLED"}

        return {"FINISHED"}


class AHIO_PT_panel(bpy.types.Panel):
    bl_label = "Outliner Highlight"
    bl_idname = "AHIO_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    def draw(self, context):
        prefs = context.preferences.addons[__name__].preferences
        layout = self.layout
        layout.prop(prefs, "enabled", text="Auto Highlight")
        layout.prop(prefs, "poll_interval")
        layout.operator(AHIO_OT_show_active.bl_idname, icon="OUTLINER")


classes = (
    AHIO_AddonPreferences,
    AHIO_OT_show_active,
    AHIO_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    ensure_timer()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
