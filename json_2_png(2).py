import cv2
import numpy as np
import json

import os
import os.path as osp
import shutil


category_types = [ "ground", "tile",  "border"]

def json2png(source_image_folder,
             label_json_folder, 
             image_save_folder, 
             mask_save_folder,
             mask_visible_folder):
    # 清空目标文件夹
    if osp.isdir(image_save_folder):
        shutil.rmtree(image_save_folder)
    if osp.isdir(mask_save_folder):
        shutil.rmtree(mask_save_folder)
    if osp.isdir(mask_visible_folder):
        shutil.rmtree(mask_visible_folder)
    # 创建目标文件夹
    os.makedirs(image_save_folder)
    os.makedirs(mask_save_folder)
    os.makedirs(mask_visible_folder)
    image_files = os.listdir(source_image_folder)
    # json_files = os.listdir(label_json_folder)
    i = 1
    for image_file in image_files:
        # 所有的jpg图片转为png并保存至目标文件夹
        source_path = osp.join(source_image_folder, image_file)
        img = cv2.imread(source_path)
        image_path = osp.join(image_save_folder, image_file[:-4]+"_square.png")
        cv2.imwrite(image_path, img)

        # 对应的Json 文件路径
        json_path = osp.join(label_json_folder, image_file[:-4]+".json")
        mask_path = osp.join(mask_save_folder, image_file[:-4]+"_square.png")
        mask_visible_path = osp.join(mask_visible_folder, image_file[:-4]+"_square_visible.png")

        # 对于第一个文件，输出过程参数
        if i == 1:
            print("source_path: ", source_path)
            print("json_path: ", json_path)
            print("image_path: ", image_path)
            print("mask_path: ", mask_path)
            print("mask_visible_path: ", mask_visible_path)
            h, w = img.shape[:2]
        i += 1
        print("images size: ", h, w)
        print("processing: ", image_file)

        # 创建三分类 mask   
        mask = np.zeros([h, w, 1], np.uint8)    # 创建一个大小和原图相同的空白图像
        mask2 = np.zeros([h, w, 1], np.uint8)    # 创建一个大小和原图相同的空白图像 
        # 第一类，全黑背景
        mask.fill(0)   
        mask2.fill(0)
        with open(json_path, "r") as f:
            label = json.load(f)
        shapes = label["shapes"]
        for shape in shapes:
            category = shape["label"]
            points = shape["points"]
            # 第二类 瓷砖 多边形填充
            points_array = np.array(points, dtype=np.int32)
            # print(points_array)
            # print(category_types.index(category))
            mask = cv2.fillPoly(mask, [points_array], category_types.index(category))
            mask2 = cv2.fillPoly(mask2, [points_array], 255)
            # 第三类 边界 多边形绘制
            mask = cv2.polylines(mask, [points_array], category_types.index("border"), color=(2, 2, 2), thickness=2)
            mask2 = cv2.polylines(mask2, [points_array], category_types.index("border"), color=(125, 2, 2), thickness=2)

        # cv2.imshow("mask", mask)
        # cv2.imshow("mask", mask2)
        # cv2.waitKey(0)

        # 图像边框处理
        # 横边框
        for i in [0, 1, 2, h-3, h-2, h-1]:
            for j in range(0, w-1):
                if mask[i][j] == 2:
                    mask[i][j] = 1
                    mask2[i][j] = 255
        # 竖边框
        for j in [0, 1, 2, w-3, w-2, w-1]:
            for i in range(0, h-1):
                if mask[i][j] == 2:
                    mask[i][j] = 1
                    mask2[i][j] = 255

        # cv2.imshow("mask", mask)
        # cv2.imshow("mask", mask2)
        # cv2.waitKey(0)

        cv2.imwrite(mask_path, mask)
        cv2.imwrite(mask_visible_path, mask2)

if __name__ == '__main__':
    source_img_dir = "D:/github/unet-nested-multiple-classification/data_tile/03_rmborder_source_images"	#原图
    source_lbl_dir = "D:/github/unet-nested-multiple-classification/data_tile/03_rmborder_source_labels" #json标注
    goal_img_dir = "D:/github/unet-nested-multiple-classification/data_tile/03_images"
    goal_mask_dir = "D:/github/unet-nested-multiple-classification/data_tile/03_masks_noboarder"
    goal_mask_visible_dir = "D:/github/unet-nested-multiple-classification/data_tile/03_masks_visible_noboarder"
    json2png(source_image_folder = source_img_dir,
             label_json_folder = source_lbl_dir, 
             image_save_folder = goal_img_dir, 
             mask_save_folder = goal_mask_dir,
             mask_visible_folder = goal_mask_visible_dir)


# ### if you want to show the mask in visible mode
# for shape in shapes:
#     category = shape["label"]
#     points = shape["points"]
#     points_array = np.array(points, dtype=np.int32)
#     if category == "tile":
#     	# 调试时将tile的填充颜色改为255，便于查看
#         mask = cv2.fillPoly(mask, [points_array], 255)
#     # 第三类 边界 多边形绘制
#     mask = cv2.polylines(mask, [points_array], category_types.index("border"), color=(125, 0, 0), thickness=3)
#     # elif category == "ground":
#     #     mask = cv2.fillPoly(mask, [points_array], 90)
#     # elif category == "border":
#     #     mask = cv2.fillPoly(mask, [points_array], 180)
#         # mask = cv2.fillPoly(mask, [points_array], category_types.index(category))

# # cv2.imshow("mask", mask)
# # cv2.waitKey(0)
# cv2.imwrite("data_tile/masks_visible/1.png", mask)
