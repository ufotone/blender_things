bl_info = {
    "name": "Bevel All Selected Object Edges",
    "author": "Codex",
    "version": (1, 1, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Item > Bevel All Edges",
    "description": "Adds a bevel to every edge of selected mesh objects.",
    "category": "Object",
}

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty


BEVEL_SETTING_NAMES = (
    "affect",
    "offset_type",
    "width",
    "segments",
    "profile",
    "material",
    "harden_normals",
    "clamp_overlap",
    "loop_slide",
    "mark_seam",
    "mark_sharp",
    "miter_outer",
    "miter_inner",
    "profile_type",
    "face_strength_mode",
    "apply_modifier",
)


def selected_mesh_objects(context):
    return [obj for obj in context.selected_objects if obj.type == "MESH"]


def set_if_available(data, name, value):
    if hasattr(data, name):
        try:
            setattr(data, name, value)
        except (TypeError, ValueError):
            pass


def add_or_update_bevel_modifier(obj, settings):
    modifier = obj.modifiers.get("Bevel All Edges")
    if modifier is None or modifier.type != "BEVEL":
        modifier = obj.modifiers.new("Bevel All Edges", "BEVEL")

    modifier.width = settings.width
    modifier.segments = settings.segments
    modifier.profile = settings.profile
    modifier.material = settings.material
    modifier.limit_method = "NONE"
    modifier.harden_normals = settings.harden_normals

    set_if_available(modifier, "affect", settings.affect)
    set_if_available(modifier, "offset_type", settings.offset_type)
    set_if_available(modifier, "clamp_overlap", settings.clamp_overlap)
    set_if_available(modifier, "loop_slide", settings.loop_slide)
    set_if_available(modifier, "mark_seam", settings.mark_seam)
    set_if_available(modifier, "mark_sharp", settings.mark_sharp)
    set_if_available(modifier, "miter_outer", settings.miter_outer)
    set_if_available(modifier, "miter_inner", settings.miter_inner)
    set_if_available(modifier, "profile_type", settings.profile_type)
    set_if_available(modifier, "face_strength_mode", settings.face_strength_mode)

    if settings.harden_normals and hasattr(obj.data, "use_auto_smooth"):
        obj.data.use_auto_smooth = True

    return modifier


class BAE_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    affect: EnumProperty(
        name="Affect",
        items=(
            ("EDGES", "Edges", "Bevel edges"),
            ("VERTICES", "Vertices", "Bevel vertices"),
        ),
        default="EDGES",
    )

    offset_type: EnumProperty(
        name="Width Type",
        items=(
            ("OFFSET", "Offset", "Amount is offset from the original edge"),
            ("WIDTH", "Width", "Amount is the width of the new face"),
            ("DEPTH", "Depth", "Amount is perpendicular depth"),
            ("PERCENT", "Percent", "Amount is a percentage"),
            ("ABSOLUTE", "Absolute", "Amount is absolute adjacent edge distance"),
        ),
        default="OFFSET",
    )

    width: FloatProperty(
        name="Width",
        description="Bevel amount",
        default=0.03,
        min=0.0,
        soft_max=1.0,
        subtype="DISTANCE",
    )

    segments: IntProperty(
        name="Segments",
        description="Number of bevel segments",
        default=2,
        min=1,
        soft_max=16,
    )

    profile: FloatProperty(
        name="Profile",
        description="Shape of the bevel profile",
        default=0.5,
        min=0.0,
        max=1.0,
        precision=3,
    )

    material: IntProperty(
        name="Material Index",
        description="Material index for new bevel faces; -1 keeps adjacent material",
        default=-1,
        min=-1,
        soft_max=16,
    )

    harden_normals: BoolProperty(
        name="Harden Normals",
        description="Improve shading along bevels",
        default=True,
    )

    clamp_overlap: BoolProperty(
        name="Clamp Overlap",
        description="Prevent bevels from overlapping",
        default=True,
    )

    loop_slide: BoolProperty(
        name="Loop Slide",
        description="Prefer sliding along surrounding edges",
        default=True,
    )

    mark_seam: BoolProperty(
        name="Mark Seam",
        description="Mark new bevel edges as seams",
        default=False,
    )

    mark_sharp: BoolProperty(
        name="Mark Sharp",
        description="Mark new bevel edges as sharp",
        default=False,
    )

    miter_outer: EnumProperty(
        name="Outer Miter",
        items=(
            ("SHARP", "Sharp", "Sharp outer miter"),
            ("PATCH", "Patch", "Patch outer miter"),
            ("ARC", "Arc", "Arc outer miter"),
        ),
        default="SHARP",
    )

    miter_inner: EnumProperty(
        name="Inner Miter",
        items=(
            ("SHARP", "Sharp", "Sharp inner miter"),
            ("ARC", "Arc", "Arc inner miter"),
        ),
        default="SHARP",
    )

    profile_type: EnumProperty(
        name="Profile Type",
        items=(
            ("SUPERELLIPSE", "Superellipse", "Use the standard bevel profile"),
            ("CUSTOM", "Custom", "Use custom profile when available"),
        ),
        default="SUPERELLIPSE",
    )

    face_strength_mode: EnumProperty(
        name="Face Strength",
        items=(
            ("NONE", "None", "Do not set face strength"),
            ("NEW", "New", "Set strength on new faces"),
            ("AFFECTED", "Affected", "Set strength on affected faces"),
            ("ALL", "All", "Set strength on all faces"),
        ),
        default="NONE",
    )

    apply_modifier: BoolProperty(
        name="Apply",
        description="Apply the bevel modifier immediately",
        default=False,
    )

    def draw(self, context):
        draw_bevel_settings(self.layout, self)


def copy_preferences_to_operator(prefs, operator):
    for name in BEVEL_SETTING_NAMES:
        setattr(operator, name, getattr(prefs, name))


def copy_operator_to_preferences(operator, prefs):
    for name in BEVEL_SETTING_NAMES:
        setattr(prefs, name, getattr(operator, name))


def draw_bevel_settings(layout, settings):
    layout.prop(settings, "affect", expand=True)
    layout.prop(settings, "offset_type")
    layout.prop(settings, "width")
    layout.prop(settings, "segments")
    layout.prop(settings, "profile")
    layout.prop(settings, "material")
    layout.prop(settings, "harden_normals")
    layout.prop(settings, "clamp_overlap")
    layout.prop(settings, "loop_slide")
    layout.prop(settings, "mark_seam")
    layout.prop(settings, "mark_sharp")
    layout.prop(settings, "miter_outer")
    layout.prop(settings, "miter_inner")
    layout.prop(settings, "profile_type")
    layout.prop(settings, "face_strength_mode")
    layout.prop(settings, "apply_modifier")


class BAE_OT_bevel_all_edges(bpy.types.Operator):
    bl_idname = "bae.bevel_all_edges"
    bl_label = "Bevel All Edges"
    bl_description = "Bevel every edge on each selected mesh object"
    bl_options = {"REGISTER", "UNDO"}

    affect: EnumProperty(
        name="Affect",
        items=(
            ("EDGES", "Edges", "Bevel edges"),
            ("VERTICES", "Vertices", "Bevel vertices"),
        ),
        default="EDGES",
    )

    offset_type: EnumProperty(
        name="Width Type",
        items=(
            ("OFFSET", "Offset", "Amount is offset from the original edge"),
            ("WIDTH", "Width", "Amount is the width of the new face"),
            ("DEPTH", "Depth", "Amount is perpendicular depth"),
            ("PERCENT", "Percent", "Amount is a percentage"),
            ("ABSOLUTE", "Absolute", "Amount is absolute adjacent edge distance"),
        ),
        default="OFFSET",
    )

    width: FloatProperty(
        name="Width",
        description="Bevel amount",
        default=0.03,
        min=0.0,
        soft_max=1.0,
        subtype="DISTANCE",
    )

    segments: IntProperty(
        name="Segments",
        description="Number of bevel segments",
        default=2,
        min=1,
        soft_max=16,
    )

    profile: FloatProperty(
        name="Profile",
        description="Shape of the bevel profile",
        default=0.5,
        min=0.0,
        max=1.0,
        precision=3,
    )

    material: IntProperty(
        name="Material Index",
        description="Material index for new bevel faces; -1 keeps adjacent material",
        default=-1,
        min=-1,
        soft_max=16,
    )

    harden_normals: BoolProperty(
        name="Harden Normals",
        description="Improve shading along bevels",
        default=True,
    )

    clamp_overlap: BoolProperty(
        name="Clamp Overlap",
        description="Prevent bevels from overlapping",
        default=True,
    )

    loop_slide: BoolProperty(
        name="Loop Slide",
        description="Prefer sliding along surrounding edges",
        default=True,
    )

    mark_seam: BoolProperty(
        name="Mark Seam",
        description="Mark new bevel edges as seams",
        default=False,
    )

    mark_sharp: BoolProperty(
        name="Mark Sharp",
        description="Mark new bevel edges as sharp",
        default=False,
    )

    miter_outer: EnumProperty(
        name="Outer Miter",
        items=(
            ("SHARP", "Sharp", "Sharp outer miter"),
            ("PATCH", "Patch", "Patch outer miter"),
            ("ARC", "Arc", "Arc outer miter"),
        ),
        default="SHARP",
    )

    miter_inner: EnumProperty(
        name="Inner Miter",
        items=(
            ("SHARP", "Sharp", "Sharp inner miter"),
            ("ARC", "Arc", "Arc inner miter"),
        ),
        default="SHARP",
    )

    profile_type: EnumProperty(
        name="Profile Type",
        items=(
            ("SUPERELLIPSE", "Superellipse", "Use the standard bevel profile"),
            ("CUSTOM", "Custom", "Use custom profile when available"),
        ),
        default="SUPERELLIPSE",
    )

    face_strength_mode: EnumProperty(
        name="Face Strength",
        items=(
            ("NONE", "None", "Do not set face strength"),
            ("NEW", "New", "Set strength on new faces"),
            ("AFFECTED", "Affected", "Set strength on affected faces"),
            ("ALL", "All", "Set strength on all faces"),
        ),
        default="NONE",
    )

    apply_modifier: BoolProperty(
        name="Apply",
        description="Apply the bevel modifier immediately",
        default=False,
    )

    def invoke(self, context, event):
        prefs = context.preferences.addons[__name__].preferences
        copy_preferences_to_operator(prefs, self)
        return self.execute(context)

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        copy_operator_to_preferences(self, prefs)

        meshes = selected_mesh_objects(context)
        if not meshes:
            self.report({"WARNING"}, "No selected mesh objects")
            return {"CANCELLED"}

        active_before = context.view_layer.objects.active
        mode_before = context.object.mode if context.object else "OBJECT"

        if context.object and context.object.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")

        processed = 0
        for obj in meshes:
            modifier = add_or_update_bevel_modifier(
                obj,
                self,
            )

            if self.apply_modifier:
                context.view_layer.objects.active = obj
                obj.select_set(True)
                try:
                    bpy.ops.object.modifier_apply(modifier=modifier.name)
                except RuntimeError as error:
                    self.report({"WARNING"}, f"{obj.name}: {error}")
                    continue

            processed += 1

        if active_before:
            context.view_layer.objects.active = active_before

        if context.object and mode_before != "OBJECT":
            try:
                bpy.ops.object.mode_set(mode=mode_before)
            except RuntimeError:
                pass

        action = "Applied bevel to" if self.apply_modifier else "Added bevel modifier to"
        self.report({"INFO"}, f"{action} {processed} mesh object(s)")
        return {"FINISHED"}

    def draw(self, context):
        draw_bevel_settings(self.layout, self)


class BAE_PT_panel(bpy.types.Panel):
    bl_label = "Bevel All Edges"
    bl_idname = "BAE_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    def draw(self, context):
        prefs = context.preferences.addons[__name__].preferences
        layout = self.layout
        draw_bevel_settings(layout, prefs)
        layout.operator(BAE_OT_bevel_all_edges.bl_idname, icon="MOD_BEVEL")


classes = (
    BAE_AddonPreferences,
    BAE_OT_bevel_all_edges,
    BAE_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
