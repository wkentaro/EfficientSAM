from PIL import Image
import numpy as np
import torch
import onnxruntime
import imgviz


image = np.array(Image.open("figs/examples/dogs.jpg"))
image = image[:, :1024]
image = np.pad(image, ((0, 1024 - image.shape[0]), (0, 0), (0, 0)), mode="constant")

input_image = image.transpose(2, 0, 1)[None].astype(np.float32) / 255.0
# batch_size, num_queries, num_points, 2
input_points = np.array([[[[580, 350], [650, 350]]]], dtype=np.float32)
# batch_size, num_queries, num_points
input_labels = np.array([[[1, 1]]], dtype=np.float32)

inference_session = onnxruntime.InferenceSession("weights/efficient_sam_vitt.onnx")
predicted_logits, predicted_iou, predicted_lowres_logits = inference_session.run(
    output_names=None,
    input_feed={
        "batched_images": input_image,
        "batched_point_coords": input_points,
        "batched_point_labels": input_labels,
    },
)

mask = predicted_logits[0, 0, 0, :, :] >= 0
imgviz.io.pyplot_imshow(mask)