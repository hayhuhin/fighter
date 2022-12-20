import pygame
from os import walk
from csv import reader


def import_csv_layout(path):
    index_list = []
    with open(path) as map_:
        level  = reader(map_,delimiter=",")
        for row in level:
            index_list.append(row)
    return index_list

def import_images(path):
    items_list = []
    for _,__,info in walk(path):
        for images in info:
            if "png" in images:
                full_path = path +"/"+ images
                images = pygame.image.load(full_path).convert_alpha()
                items_list.append(images)
            
    return items_list


def import_big_images(path):
    items_list = []
    for _,__,info in walk(path):
        for images in info:
            if "png" in images:
                full_path = path + "/" + images
                imgs = pygame.image.load(full_path).convert_alpha()
                adjusted_img = pygame.transform.scale(imgs,(32,64))
                items_list.append(adjusted_img)
            
                
    return items_list

