import pytesseract
from pytesseract import Output
from dotmap import DotMap

front = [
    'REPUBLIC', 'OF', 'TURKEY', 'IDENTITY', 'CARD'
]

back = [
    'T.C.', 'ICISLERI', 'BAKANLIGI'
]

class Recognize:

    def isValid(self, frame):
        results = pytesseract.image_to_data(frame, output_type=Output.DICT)
        result = DotMap()
        if all(item in results['text'] for item in front):
            result.status = True
            result.face = 'Front'
        elif all(item in results['text'] for item in back):
            result.status = True
            result.face = 'Back'
        else:
            result.status = False
            result.face = ''
        return result

    def recognize(self, frame):
        results = pytesseract.image_to_data(frame, output_type=Output.DICT)
        '''
        if conf > 70:
            text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)
        '''
        return self.setData(results)

    def setData(self, results):
        data = DotMap()
        data.id = ''
        data.surname = ''
        data.name = ''
        data.date = ''
        data.documentNo = ''
        data.validDate = ''
        data.gender = ''
        for i in range(0, len(results["text"])):
            x = results["left"][i]
            y = results["top"][i]
            w = results["width"][i]
            h = results["height"][i]
            text = results["text"][i]
            conf = float(results["conf"][i])
            if text.isnumeric() and len(text) == 11:
                data.id = text
            if text == 'Soyadi' or text == 'Surname':
                for j in range(i, len(results["text"])):
                    if results['text'][j].isupper():
                        data.surname = results['text'][j]
                        break
            if text == 'Adi' or text == 'Given':
                for j in range(i, len(results["text"])):
                    if results['text'][j].isupper():
                        data.name = results['text'][j]
                        break
            if text == 'Dogum' or text == 'Date':
                for j in range(i, len(results["text"])):
                    if '.' in results['text'][j]:
                        data.date = results['text'][j]
                        break
            if text == 'Seri' or text == 'Document':
                for j in range(i, len(results["text"])):
                    if results['text'][j].isupper():
                        data.documentNo = results['text'][j]
                        break
            if text == 'Son' or text == 'Valid':
                for j in range(i, len(results["text"])):
                    if '.' in results['text'][j]:
                        data.date = results['text'][j]
                        break
            if text.isnumeric() and len(text) == 9:
                data.serialNo = text
            if text == 'E/M' or text == 'K/F':
                data.gender = text
        return data