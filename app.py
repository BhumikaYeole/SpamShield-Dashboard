from flask import *
from reader import read_latest
from pickle import load
import spacy
import threading
import time

nlp = spacy.load("en_core_web_lg")

f = open("model.pkl", "rb")
model = load(f)
f.close()

f = open("vectorizer.pkl", "rb")    
tv = load(f)
f.close()

def clean_function(text):
    text = text.lower()
    text = nlp(text)
    text = [t for t in text if not t.is_stop and not t.is_punct]
    text = [t.lemma_ for t in text]
    text = [str(t) for t in text]
    text = " ".join(text)
    return text



def make_preview(text, length=150):
    if not text:
        return ""
    text = " ".join(text.split())  # normalize whitespace
    return text[:length] + ("..." if len(text) > length else "")


latest_body = None
latest_result = None
live_event = threading.Event()



def live_checker():
    global latest_body, latest_result
    while live_event.is_set():
        emails = read_latest()
        email = emails[0]
        body = email['body']

        if body and body != latest_body:
            latest_body = body
            clean_body = clean_function(body)
            vector_body = tv.transform([clean_body])
            result = model.predict(vector_body)
            result = result[0]

            latest_result = {
                "from": email.get("from", "Unknown"),
                "subject": email.get("subject", "No subject"),
                "preview": make_preview(body),
                "type": result
            }

        time.sleep(10)



app = Flask(__name__)


# returns the latest live analysed mail
@app.route("/live-status")
def live_status():
    if latest_result:
        return jsonify(latest_result)
    return jsonify({"status": "waiting"})


# starts the background live analysis thread
@app.route("/live")
def live():
    global live_event
    if not live_event.is_set():
        live_event.set()
        threading.Thread(target = live_checker, daemon=True).start()
            
    return jsonify({"status": "started"})


# stops the live analysis by exitting thread loop
@app.route("/stop-live")
def stop_live():
    global live_event
    live_event.clear()
    return jsonify({"status": "stopped"})



@app.route("/" , methods =["GET"])
def home():

    emails = read_latest()
    spam = 0
    ham = 0
    for email in emails:
        body = email['body']
        if body is None:
            email["type"] = "ham"
            ham += 1
        else:
            clean_body = clean_function(body)
            vector_body = tv.transform([clean_body])
            prediction = model.predict(vector_body)
            email['body'] = make_preview(clean_body)
            email['type'] = prediction[0]
            if prediction[0] == "spam":
                spam += 1
            else:
                ham += 1

    active_filter = None

    if 'filter' in request.args:
        active_filter = request.args.get('filter')  

    if active_filter == "spam":
        emails = [e for e in emails if e['type'] == "spam"]
    elif active_filter == "ham":
        emails = [e for e in emails if e['type'] == "ham"]

    return render_template("index.html", emails = emails, spam = spam, ham = ham)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)