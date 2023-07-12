from .models_loader import yolo_model


def predict(frame):
    results = yolo_model(source=frame, stream=True, save=False)
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
                output.append((car, car_plate))
                plates.pop(index)

    for plate in plates:
        output.append((None, plate))
        
    return output
    
def within(plate, car):
    return plate[0] > car[0] and plate[1] > car[1] and plate[2] < car[2] and plate[3] < car[3]