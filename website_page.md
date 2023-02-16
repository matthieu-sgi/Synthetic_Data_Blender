# State of the Art

Blender software is used to generate dataset for data segmentation
models. This software already has been employed to create food data to train segmentation model. The shape, volume, texture, color, and
composition of food vary. Blender allows to generate a huge amount of
data with variations (on food, lights and camera). In this case, the dataset trains a Mask R-CNN for instance segmentation.

# Tutorial

The objective of this tutorial is to show how to generate a dataset for a segmentation model. The dataset is generated using Blender software. The dataset is used to train a U-Net model for instance segmentation.

The dataset is composed of 2 parts :
    
- Images : the images are generated using Blender software. The images are saved in a folder. Those images are images of a pool table with different ball positions and light orientation.
- A file (.csv) : the file contains the position of the balls in the images and the color.

## Blender

Blender is a free and open-source 3D computer graphics software toolset used for creating animated films, visual effects, art and for many other application.

The use of Blender is pushed by the fact that the software can render images using ray tracing. Ray tracing is a rendering technique that simulates the physical behavior of light to render an image. It is a technique that can be used to create photorealistic images. The shadows are close to the reality and the reflections are also very realistic. The use of ray tracing is a good way to create a dataset for a segmentation model.

### Model

For the model, either you can create it or find model on the internet. In this tutorial, we will use a model of a pool table. The model is available on github[¹]. For the balls, we will use a simple sphere colored (yellow or red) with a glossy render close to real.

On Blender, you can see the objects that exist in your blender project in the `collection` section.

Example of collection section on the project :

![example of collection section on the project](media/collection.png)

The `"pool_table"`, `"red_ball"` and `"yellow_ball"` are the original model of the element. Only one instance of the each object is required to go further. 

### Layout

In Blender, the layout is essential. In order to use the python library of Blender (bpy), the easiest way is to code directly in the IDE (integrated development environment) provided by Blender.

Let's split the display. Get a corner of the model window and drag it.

![split display](media/split_display.png)

Then click on the `editor type` button and choose `text editor`.

![editor type](media/editor_type.png)

The text editor is now available. You can write your code in this editor and run it in the python console. But first, you need to create a new file. Click on the `new` button.
A new file is created. You can name it as you want.

Here is the layout that I use :

![layout](media/layout.png)

### Render engine

Blender has 3 render engines :
- Cycles
- Eevee
- Workbench

The Cycles render engine is the most powerful. It is based on ray tracing. It is the render engine that we will use to generate the dataset. The shadow and the reflection are very realistic. The render is slower than the Eevee render engine.

The Eevee render engine is a real-time render engine. It is based on ray tracing too.

The Workbench render engine is a simple render engine. It is used to render quickly.



## Python

First of all, I higly recommend to read the documentation of Blender. You can find it [here](https://docs.blender.org/api/current/). 

Also you need to know the basics of python. You can find the documentation [here](https://docs.python.org/3/).


Then if you are running on a linux distribution, you should run Blender using the terminal. It will allow you to see the errors that you will have.

```python
blender <name-of-your-file>.blend
```

### Imports

The first step is to import the python library of Blender. The library is called `bpy`. You can import it with the following code :

```python
import bpy
```

We also imported the `os` library to save the output.

```python
import os
```

And some other import that are necessary for the code.

```python
from random import uniform as ru, randint as ri # random uniform and random integer
import mathutils
import csv # to save the csv file
```
 


### Variables

The first step is to define the variables. The variables are the parameters of the dataset. The variables are the following :

- `master_path` : path to save the dataset
- `root_object` : objects that mustn't be suppressed
- `width` and `height` : dimensions of the pool in real life and in the modelisation
- `ball_offset` : half of the size of the ball (used to compute the colliding)
- `column_names` : name of the column in the output file (.csv)

### Methods

General methods for a dataset generation are the following :

- `create_csv` : create the csv file and write the header
- `write_in_csv` : write the data in the csv file
- `copy_object` : copy root object and link it to the collection
- `delete_objects` : delete all the objects except the root object
- `collide` : check if the ball collide with another ball
- `generate_random_pos` : generate a random position and return it
- `moove_object` : move all the objects to the position randomly generated
- `moove_light` : move the light to the position randomly generated
- `generate_light` : generate a random number of light and place them randomly
- `render_and_export` : render the scene and save the image + save coordinates of the balls in the csv file. The choice of the render engine is input as argument.
- `choose_device` : choose the device to render the scene (CPU or GPU)
- `step` : main function that call all the other functions

Specific methods for this dataset are the following :
- `generate_ball` : generate random number of balls and place them randomly


### Adding HDR lights


### Usage

The usage is the following :

```python
if __name__ == "__main__":
    # create the csv file
    create_csv()
    # for loop corresponding to the number of images that you want to generate
    for i in range(number_of_image):
        step(i)
```



# Output

The `master path` that you entered is the path where the dataset will be saved. 


The output is a dataset composed of 2 parts :
- Images
- A file (.csv) : the file contains the position of the balls in the images and the color

An example can be found [here](https://github.com/matthieu-sgi/Synthetic_Data_Blender/tree/main/examples/w_hdr).




# References

[1] : Github repository [@yliess86/Snook](https://github.com/yliess86/Snook)