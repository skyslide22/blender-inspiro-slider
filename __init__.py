from os import remove
import bpy
from bpy.utils import register_class, unregister_class

from .operators import (OT_GoLeft, OT_GoRight, OT_ReloadGallery, setFirstImage)
from .panels    import (draw_slider_buttons)

classes = (
    OT_GoLeft,
    OT_GoRight,
    OT_ReloadGallery,
)

bl_info = {
    "name"          : "Inpspiro slide",
    "author"        : "skyslide",
    "description"   : "preview images in viewport",
    "blender"       : (3, 0, 0),
    "version"       : (0, 1, 0),
    "location"      : "View3D",
    "warning"       : "wawawa",
    "category"      : "Generic"
} 


def register():
    bpy.types.IMAGE_HT_header.append(draw_slider_buttons)
    bpy.types.Scene.image_slider_folder_src = bpy.props.StringProperty(
        name="slider src", 
        subtype="DIR_PATH",
        update=setFirstImage
        )
    for cls in classes: 
        register_class(cls)
    

def unregister():
    bpy.types.IMAGE_HT_header.remove(draw_slider_buttons)
    del bpy.types.Scene.image_slider_folder_src
    for cls in reversed(classes): 
        unregister_class(cls)