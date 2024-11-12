from ultralytics import YOLO
import torch
torch.cuda.empty_cache()

if __name__ == '__main__':
    # 加载预训练模型
    model = YOLO('yolov8n.pt')  # 加载预训练模型

    # 训练模型
    model.train(
        data='E:/Py_code/yolov8/dataset_v2/data.yaml',  # 数据集配置文件路径
        epochs=100,  # 训练周期数
        imgsz=800,  # 输入图像的尺寸
        batch=8,  # 批次大小
        optimizer='SGD',  # 优化器
        device='cuda',  # 使用GPU
    )

