import json

import openai
from flask import Blueprint, flash, render_template, request
from flask_login import current_user, login_required

from . import db
from .models import AiEmail

aiemail = Blueprint("aiemail", __name__)

with open("/mnt/sdb3/Code/Projects/personal-website/config.json") as f:
    config = json.load(f)

openai.api_key = config["key"]


@aiemail.route("/ai-emails", methods=["GET", "POST"])
@login_required
def aiemails():
    answer = ""
    if request.method == "POST":
        userPrompt = request.form.get("input")
        if request.form["style"] == "friendly":
            style = "friendly"
        else:
            style = "professional"

        customPrompt = f"Human:I would like you to write a {style} email to a customer in HTML syntax to explain and offer additional assistance or follow-up if needed about the following, {userPrompt}, avoid using I'm happy to let you know or I hope this email finds you well, make the email customer focused and show that we care about him, and make the email not too short. AI:"
        print("customPrompt: %s" % (customPrompt))
        if len(userPrompt) < 20:
            flash("Description is too short", category="error")
        else:
            prompt = customPrompt
            model = "text-davinci-003"
            max_tokens = 500
            response = openai.Completion.create(
                model=model,
                prompt=prompt,
                temperature=0,
                max_tokens=max_tokens,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=[" Human:", " AI:"],
            )
            print(response)

            answer = response["choices"][0]["text"]
            tokens = response["usage"]["total_tokens"]
            print("tokens: %s" % (tokens))
            # price is $0.0200  / 1K tokens
            new_email = AiEmail(
                input=prompt,
                style=style,
                output=answer,
                tokens=tokens,
                model=model,
                user_id=current_user.id,
            )
            db.session.add(new_email)
            db.session.commit()
    return render_template("ai-emails.html", user=current_user, answer=answer)


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


# class AiEmail(db.Model):
#       id = db.Column(db.Integer, primary_key=True)
#     input = db.Column(db.String(1000))
#     style = db.Column(db.String(32))
#     output = db.Column(db.String(32000))
#     tokens = db.Column(db.Integer)
#       date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
