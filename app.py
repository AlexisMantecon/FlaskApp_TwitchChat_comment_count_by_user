from flask import Flask, render_template, request
from chat_downloader import ChatDownloader
import pandas as pd

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/details", methods=["GET", "POST"])
def details():
    try:
        url=request.form["url_name"]
        chat = ChatDownloader().get_chat(url) # create a generator
        msg_counter = {}
        for message in chat: # iterate over messages
            username = message["author"]["name"]
            if username in msg_counter.keys():
                msg_counter[username] += 1
            else:
                msg_counter[username] = 1

        df = pd.DataFrame(msg_counter.items(), columns=['TTV_UserName', '#Comments']).sort_values(by="#Comments", ascending=False).head(10)
        return render_template("details.html", details=df.to_html(index=False, justify="justify-all", classes="table table-striped table-bordered table-light"))
    except:
        return render_template("details.html", details="<div class='alert alert-danger' role='alert'>Invalid url, please try again</div>")

if __name__=='__main__':
    app.debug=True
    # app.run(host="192.168.0.2")
    app.run()