import torch
from tqdm import tqdm


def inference(model, inference_data, device):
    model.eval()
    model.to(device)
    with torch.no_grad():
        answer = []
        for img in tqdm(inference_data):
            img=img.to(device)
            output = model(img)
            output = torch.sigmoid(output)
            probability, argmax = torch.max(output, 1)
            pred = argmax.item()
            answer.append(pred)

    return answer
            
