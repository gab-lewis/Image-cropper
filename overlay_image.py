import os
import random

import cv2

def image_overlayer(object_name, bg_name, obj_class):
    """
    This function takes in an object without a background and overlays it onto a larger background image
    
    Args:
    object_name : str = Name of object image .png
    bg_name : str = Name of background image .jpg
    obj_class: int = Class number of specific object

    Returns:
    None
    Writes recombined image to recombined-images folder
    """

    s_img = cv2.imread(f"./images/objects/{object_name}", -1)
    l_img = cv2.imread(f"./images/backgrounds/{bg_name}", -1)

    #Positioning object within background
    for i in range(10): # 10 tries
        try:
            #randomizing image size
            new_x = random.randint(l_img.shape[1]//10, l_img.shape[1]//5)
            shrink_factor = new_x/s_img.shape[1]
            new_x = round(shrink_factor*s_img.shape[1])
            new_y = round(shrink_factor*s_img.shape[0])
            s_img = cv2.resize(s_img, (new_x, new_y))

            #deciding offset of x and y coordinates of object in bg (randomly)
            x_offset = random.randint(5, (l_img.shape[1]-(s_img.shape[1]+5)))
            y_offset = random.randint(5, (l_img.shape[0]-(s_img.shape[0]+5)))

            #calculating 4 corners of object offset
            x1, x2 = x_offset, x_offset + s_img.shape[1]
            y1, y2 = y_offset, y_offset + s_img.shape[0]
            
            #normalizing alpha values
            alpha_s = s_img[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s

            #overlay object onto background
            for c in range(0, 3):
                l_img[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] +
                                        alpha_l * l_img[y1:y2, x1:x2, c])
        
        except ValueError as E:
            # print(E)
            continue
        else:
            break
    
    file_count = len(os.listdir("./images/recombined-images/"))
    file_name = f"recombined-{file_count}"
    cv2.imwrite(f"./images/recombined-images/{file_name}.jpg", l_img)

    #generate yolo annotation
    annot_x = (((x2-x1)/2)+x1)/l_img.shape[1]
    annot_y = (((y2-y1)/2)+y1)/l_img.shape[0]
    obj_width = (s_img.shape[1])/l_img.shape[1]
    obj_height = (s_img.shape[0])/l_img.shape[0]

    f = open(f"./images/labels/{file_name}.txt", "w")
    f.write(f"{obj_class} {annot_x} {annot_y} {obj_width} {obj_height}")
    f.close()

if __name__ == "__main__":
    OBJECT_NAME = "000032_nobg.png"
    BACKGROUND_NAME = "tycho-atsma-_7-kV-1AOc4-unsplash-1920x1280.jpg"
    for i in range(5):
        image_overlayer(OBJECT_NAME, BACKGROUND_NAME, 0)