import bpy
from bpy.types import (
    Operator
)
import os


class OT_GoLeft(Operator):
    bl_idname = "image_slider.go_left"
    bl_description = "Show previous image"
    bl_label = "Go Left"
        
    def execute(self, context):
        setImage(context, go_right=False)
        return {"FINISHED"}

class OT_GoRight(Operator):
    bl_idname = "image_slider.go_right"
    bl_description = "Show next image"
    bl_label = "Go Right"
        
    def execute(self, context):
        setImage(context, go_right=True)
        return {"FINISHED"}

class OT_ReloadGallery(Operator):
    bl_idname = "image_slider.reload_gallery"
    bl_description = "Reload all images"
    bl_label = "Reload"
        
    def execute(self, ctx):
        setFirstImage(self, ctx)
        return {"FINISHED"}





SUPPORTED_IMAGE_FORMATS = (
    "DDS",
    "PNG",
    "JPEG",
    "JPG",
    "TGA",
    "PSD",
    "BMP",
    "ICO",
    "WEBP",
    "EXR"
)

active_image_index = 0
loaded_images      = []



def setImage(ctx, go_right=False, first=False) -> None:
    global active_image_index

    if go_right:
        active_image_index = active_image_index + 1 if active_image_index < len(loaded_images) - 1 else 0
    else:
        active_image_index = active_image_index - 1 if active_image_index > 0 else len(loaded_images) - 1
    
    if first: 
        active_image_index = 0

    for area in ctx.screen.areas:
        for space in area.spaces:
            if space.type == 'IMAGE_EDITOR':
                
                if space.use_image_pin is True:
                    continue # keep pinned image, eg: two editors, one has pinned img

                try:
                    img = loaded_images[active_image_index]
                
                except IndexError:
                    reloadImages()
                    if len(loaded_images) > 0:
                        img = loaded_images[0]
                    else:
                        img = None

                if img is not None:
                    try:
                        print(f"set image {active_image_index} - {img.name}")
                        space.image = img
                        bpy.ops.image.view_all(fit_view=True)    
                        # TODO: image not zoomed on first folder load
                        # TODO: & line above does not work for some reason ...
                    
                    except ReferenceError:
                        print("reference error, reload images ...")
                        reloadImages(ctx=ctx)



    


def setFirstImage(self, ctx) -> None:
    print("set first image")
    if reloadImages(None, ctx):
        setImage(ctx, first=True)



def reloadImages(self=None, ctx=None) -> bool:
    src_path = bpy.context.scene.image_slider_folder_src
    loaded_images.clear()
    print("reload images, count: 0")
    for filename in getListOfFiles(src_path):

        if filename.upper().endswith(SUPPORTED_IMAGE_FORMATS):
            
            filepath = src_path + "/" + filename
            img      = None
            
            try:
                img = bpy.data.images[filename]
                img.reload()
            
            except:
                img = bpy.data.images.load(filepath)
            
            finally:
                if img is not None:
                    print("add: ", filename)
                    loaded_images.append(img)
    

    print("images loaded, count: ", len(loaded_images))
    return True if len(loaded_images) > 0 else False
            

def getListOfFiles(folderpath: str) -> list:
    folders = []
    folderpath = bpy.path.abspath(folderpath)

    for file in os.listdir(folderpath):
        if os.path.isfile(folderpath + "/" + file):
            folders.append(file)
    
    return folders

