 
import detectron2
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from detectron2.data import build_detection_test_loader

import pandas as pd
import matplotlib.pyplot as plt
import torch

def evaluate_model(cfg, coco_2017_val_100):
    evaluator = COCOEvaluator(coco_2017_val_100, cfg, False, output_dir="./output/")
    val_loader = build_detection_test_loader(cfg, coco_2017_val_100)
    metrics = inference_on_dataset(DefaultPredictor(cfg).model, val_loader, evaluator)
    return metrics

def save_metrics_to_csv(metrics, filename):
    df = pd.DataFrame(metrics).T.reset_index()
    df.columns = ['Metric', 'Value']
    df.to_csv(filename, index=False)

def plot_metrics(file_path, title, y_label):
    df = pd.read_csv(file_path)
    metrics = df['Metric']
    values = df['Value']

    plt.figure(figsize=(10, 6))
    plt.bar(metrics, values)
    plt.xlabel('Metrics')
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

# Configuration and evaluation
cfg_damage = get_cfg()
cfg_damage.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg_damage.MODEL.WEIGHTS = "damage/model_final.pth"
cfg_damage.MODEL.ROI_HEADS.NUM_CLASSES = 1
damage_metrics = evaluate_model(cfg_damage, "coco_2017_val_100")
save_metrics_to_csv(damage_metrics, "damage_metrics.csv")

# Plotting the metrics
plot_metrics("damage_metrics.csv", "Damage Model Metrics", "Value")
