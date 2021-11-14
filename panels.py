import bpy
from bpy.types import Panel


def draw_slider_buttons(cls, context):
    layout = cls.layout

    row = layout.row(align=True)
    row.operator(
        "image_slider.go_left", 
        text="", 
        icon="TRIA_LEFT"
        )
    row.operator(
        "image_slider.go_right", 
        text="", 
        icon="TRIA_RIGHT"
        )
    row.prop(context.scene, "image_slider_folder_src", text="")
    row.operator(
        "image_slider.reload_gallery",
        text="",
        icon="FILE_REFRESH"
    )

