from ultralytics import YOLO
import torch
import os

# Use the weights previously obtained from training.
model = YOLO(os.path.join(os.getcwd() , 'car_tracking/license_plate_processor/utils/yolo_weights/best.pt'))
# If a supported GPU is avaliable, use it instead of cpu.
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("#"*50 + "YOLO Model" + "#"*50)
print(f"Using: {device}")
print("#" * 110)
model.to(device)

def predict(frame):
    results = model(source=frame, stream=True)
    cars = []
    plates = []
    for result in results:
        classes = result.boxes.cls.tolist()
        xyxys = result.boxes.xyxy.tolist()     
        for i, c in enumerate(classes):
            if(c == 1):
                cars.append(xyxys[i])
            else:
                plates.append(xyxys[i])
    
    output = []
    for car in cars:
        car_plate = None
        for index, plate in enumerate(plates):
            if(within(plate, car)):
                car_plate = plate
                plates.pop(index)
        output.append((car, car_plate))
    
    for plate in plates:
        output.append((None, plate))
        
    return output
    
def within(plate, car):
    return plate[0] > car[0] and plate[1] > car[1] and plate[2] < car[2] and plate[3] < car[3]