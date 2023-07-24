import cv2
from pyzbar import pyzbar

# img = cv2.imread(r"C:\Users\kc.hsu\Downloads\barcode.png")

def read_barcodes(frame):
    detectedBarcodes = pyzbar.decode(frame)

    for barcode in detectedBarcodes:
        (x, y, w, h) = barcode.rect
        #1
        barcode_info = barcode.data.decode("utf-8")
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        #2
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (0, 255, 0), 1)
        
        #3
        with open("./sales_related/Marketing相關/PI project/barcode.txt", mode="w") as file:
            file.write("Recongnized Barcode:" + barcode_info)
    return frame
        
        
def main():
    #1
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    
    #2
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame)
        cv2.imshow("Real Time Barcode Scanner", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    #3
    camera.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()