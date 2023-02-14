from random import uniform as ru, randint as ri

import bpy
import csv
import mathutils
import os

root_objects = ["Camera","Light","pool_table", "red_ball","Plane","yellow_ball"] #objects that musn't be supressed

#DONT FORGET TO PUT THE LAST BACKSLASH IN THE PATHS
master_path = "/mnt/data/Documents/A4/pool_temp"
mask_path = "/mnt/data/Documents/A4/pool_temp"

#Dimensions of my pool
width , height = 1.900, 0.956
x_min,x_max = -(width/2),width/2
y_min,y_max = -(height/2),height/2
z_pos = 0.120

#ball offset to avoid collisions
ball_offset = 0.059/2

#To initialize csv
def create_csv(
    path : str = master_path,
    filename : str = 'coords.csv'
    ) -> None :
    #Column names
    row_list = ["id","x","y","z",'color']
    fullpath = path + filename
    with open(fullpath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row_list)

def write_in_csv(
    id : int,
    coords : tuple,
    color : str,
    path : str = master_path,
    filename : str = 'coords.csv'
    ) -> None :
    fullpath = path+filename
    row = [id, *coords,color]
    with open(fullpath, 'a', newline='') as fd:
        writer = csv.writer(fd)
        writer.writerow(row)
    


def copy_obj(object_name : str) -> None:
    obj = bpy.data.objects[object_name].copy()
    bpy.context.collection.objects.link(obj)
    
def collide(x : float, y: float) -> bool :
    
    for obj in bpy.data.objects:
        x_obj, y_obj , *_ = obj.location
        if x_obj + ball_offset >= x and x_obj - ball_offset <= x :
            return True
        if y_obj + ball_offset >= y and y_obj - ball_offset <= y :
            return True
        
    return False
    
def generate_random_pos() -> tuple :
    return (ru(x_min + ball_offset,x_max - ball_offset),
            ru(y_min + ball_offset ,y_max - ball_offset),
            z_pos)
            
def moove_objects() -> None :
    for obj in bpy.data.objects :
        if obj.name in ['Camera','Light', "Plane",'pool_table','Light.001','Light.002']:
            continue
        (x,y,z) = generate_random_pos()
        
        while collide(x,y):
            (x,y,z) = generate_random_pos()
        obj.location = mathutils.Vector((x,y,z))

def delete_objects() -> None :
    for obj in bpy.data.objects :
        if obj.name not in root_objects :
            bpy.data.objects.remove(obj)
            


def hide_show(name : str, hide : bool) :
    obj = bpy.data.objects[name]
    obj.hide_viewport = hide
    obj.hide_render = hide

def generate_balls(nb_red : int = 7, nb_yellow : int = 7) -> None:

    for _ in range (nb_red-1) :
        copy_obj("red_ball")
    for _ in range (nb_yellow-1) :
        copy_obj("yellow_ball")
    if(nb_red == 0):
        hide_show("red_ball",True)
    else :
        hide_show("red_ball",False)
    if(nb_yellow == 0):
        hide_show("yellow_ball",True)
    else :
        hide_show("yellow_ball",False)
    
    moove_objects()
    
def render_and_export(
    id : int ,
    path : str = master_path+ "images",
    engine : str = 'CYCLES'
    #use_GPU : bool = False
    ) -> None :
    bpy.context.scene.render.engine = engine
    
    if engine == 'CYCLES' :
        choose_device(soft = "NONE",device = 'CPU')
        #choose_device(soft = "CUDA",device = 'GPU')
        
    name = str(id) + '.png'
    bpy.data.scenes['Scene'].render.resolution_x = 100
    bpy.data.scenes['Scene'].render.resolution_y = 56
    bpy.context.scene.render.filepath = os.path.join(path, name ) #(output_file_pattern_string % step)
    bpy.ops.render.render(write_still = True)
    for obj in bpy.data.objects :
        if obj.name not in root_objects or obj.name in ["red_ball", "yellow_ball"]: #Trash way to do it but easier.
            if obj.name.startswith("red"):
                write_in_csv(id, tuple(obj.location),'r')
            else :
                write_in_csv(id, tuple(obj.location),'y')
    #write_in_csv(id,
    

def choose_device(soft : str = "CUDA", device : str = "GPU") -> None:
    bpy.context.preferences.addons[
    "cycles"
    ].preferences.compute_device_type = soft # or "OPENCL"

    # Set the device and feature set
    bpy.context.scene.cycles.device = device
    #bpy.context.scene.cycles.use_preview_denoising = False
    #bpy.context.scene.use_nodes = False
    bpy.context.scene.cycles.use_denoising = False

    # get_devices() to let Blender detects GPU device
    bpy.context.preferences.addons["cycles"].preferences.get_devices()
    print(bpy.context.preferences.addons["cycles"].preferences.compute_device_type)
    for d in bpy.context.preferences.addons["cycles"].preferences.devices:
        d["use"] = 1 # Using all devices, include GPU and CPU
        print(d["name"], d["use"])

def moove_light() -> None:
    lights_names = [light.name for light in bpy.data.objects if light.name.startswith("Light")]
    for l in lights_names:
        max = 3
        x,y = ru(-max,max),ru(-max,max)
        z = ru(z_pos-0.10,max)
        bpy.data.objects[l].location = mathutils.Vector((x,y,z))
        
def generate_lights(nb_light : int = 2):
    for _ in range(nb_light-1):
        copy_obj("Light")
    moove_light()
        
def step(id : int)->None:
    delete_objects()
    generate_balls(ri(0,7),ri(0,7))
    generate_lights(ri(1,3))
    render_and_export(id)
    
def rotate_background(angle : float = ru(0,6.18)) ->None :

    obj = bpy.data.worlds["World"].node_tree
    obj.nodes["Mapping"].inputs[2].default_value[2] = angle

def moove_camera(liberty: float = 0.3, x : float = 0, y : float = 0, z : float = 3) ->None :
    for obj in bpy.data.objects :
        if obj.name == "Camera" :
            new_pos = (ru(x - liberty,x + liberty),
            ru(y - liberty  ,y + liberty),
            ru(z - liberty  ,z + liberty))
            obj.location = mathutils.Vector(new_pos)

def background_strength(strength :float = ru(0.5,1.5)) -> None :
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = strength 




#def generate_masks() -> None:
        

if __name__ == "__main__" : 
    #moove_camera()
    create_csv(
    path = master_path,
    filename = 'coords_hdr_camera.csv'
    )
    #moove_light()
    
    for i in range(10) :
         step(i)
         rotate_background(angle = ru(0,6.18))
         #moove_camera()
         background_strength(strength = ru(0.5,1.5))
         render_and_export(i,path = master_path+ "images_hdr_camera")
    
    
