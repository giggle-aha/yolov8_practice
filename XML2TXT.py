import os
from lxml import etree

"""
将xml文件转成YOLO模型可以训练的txt文件
"""


def get_classes(source_path, files):
    """
    读取全部标签文件中的类别名称，并生成类别与数字的对应关系字典：
    :param files:
    :param source_path:
    :return:
    """
    class_set = set([])
    for file in files:
        with open(os.path.join(source_path, file), 'rb') as fb:
            try:
                # 使用etree.parse来解析XML文件
                tree = etree.parse(fb)  # 解析XML文件
                root = tree.getroot()  # 获取XML树的根节点
                labels = root.xpath('//object')  # 获取所有对象节点

                for label in labels:
                    name = label.xpath('./name/text()')[0]  # 获取标签的名称
                    class_set.add(name)  # 将标签名称加入集合中，去重
            except Exception as e:
                print(f"Error parsing {file}: {e}")
    return list(class_set)


def convert_xml2txt(file_name, source_path, label_path, class_dict, norm=False):
    """
    将xml标签文件转化为txt，并写在新的文件夹中：
    :param file_name:
    :param source_path:
    :param label_path:
    :param class_dict:
    :param norm:
    :return:
    """
    # 创建txt文件，并打开、写入
    new_name = file_name.split('.')[0] + '.txt'
    with open(os.path.join(label_path, new_name), 'w') as f:
        try:
            with open(os.path.join(source_path, file_name), 'rb') as fb:
                # 开始解析xml文件，获取图像尺寸
                tree = etree.parse(fb)
                root = tree.getroot()

                width = int(root.xpath('//size/width/text()')[0])
                height = int(root.xpath('//size/height/text()')[0])

                # 获取对象标签
                labels = root.xpath('//object')  # 单张图片中的目标数量 len(labels)

                for label in labels:
                    xmin = int(label.xpath('./bndbox/xmin/text()')[0])
                    xmax = int(label.xpath('./bndbox/xmax/text()')[0])
                    ymin = int(label.xpath('./bndbox/ymin/text()')[0])
                    ymax = int(label.xpath('./bndbox/ymax/text()')[0])

                    # 处理标签框的xyxy --> xywh，并且根据需要进行归一化
                    name = label.xpath('./name/text()')[0]
                    label_class = class_dict[name]

                    # 归一化处理
                    if norm:
                        dw = 1 / width
                        dh = 1 / height
                        x_center = (xmin + xmax) / 2
                        y_center = (ymax + ymin) / 2
                        w = (xmax - xmin)
                        h = (ymax - ymin)

                        # 归一化后写入文件
                        x, y, w, h = x_center * dw, y_center * dh, w * dw, h * dh
                        f.write(f"{label_class} {x} {y} {w} {h}\n")
                    else:
                        # 如果不进行归一化，直接写原始坐标
                        f.write(f"{label_class} {xmin} {ymin} {xmax} {ymax}\n")

        except Exception as e:
            print(f"Error processing {file_name}: {e}")


if __name__ == '__main__':

    # xml格式标签文件存放的文件夹
    xml_path = r'E:/Py_code/yolov8/data/Annotations'
    # txt格式标签文件存放的文件夹
    txt_path = r'E:/Py_code/yolov8/data/labels'

    # 创建txt标签存放路径
    if not os.path.exists(txt_path):
        os.mkdir(txt_path)

    # 获取文件名称列表
    files = os.listdir(xml_path)
    classes = get_classes(xml_path, files)  # 获取所有类名

    # class_dict: a 0, b 1
    class_dict = dict(zip(classes, range(len(classes))))

    # 输出每个类对应的编号
    for key, value in class_dict.items():
        print(f"class_dict: {key} -> {value}")

    # 将每个XML文件转换为TXT文件
    for file in files:
        convert_xml2txt(file, xml_path, txt_path, class_dict, norm=True)

    print("xml文件转txt文件成功！")
