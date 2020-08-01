import pytesseract, PIL, time

def captcha():
    """This function will solve the captcha in image 'captcha.jpeg'
    using library pytesseract
    """
    print("\n[!] Obtaining CAPTCHA value")
    time.sleep(1)
    value = pytesseract.image_to_string(PIL.Image.open("captcha.jpeg"))

