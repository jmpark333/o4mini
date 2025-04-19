# demo_app.py  (2025-04-18 08:47:50 수정)
# demo_app.py  (2025-04-18 08:50:44 수정)
# demo_app.py  (2025-04-18 09:27:09 수정)
import os, requests, openai
from flask import Flask, request, render_template, jsonify

app = Flask(__name__, static_folder="static", template_folder="templates")
openai.api_key = os.getenv("OPENAI_API_KEY")
BRAVE_KEY = os.getenv("BRAVE_WEBSEARCH_API_KEY")

@app.route("/")  
def index():  
    return render_template("index.html")

@app.route("/search", methods=["POST"])  
def web_search():  
    q = request.json["query"]  
    r = requests.get("https://api.brave.com/search",  # 수정: Brave API URL 대괄호 제거
                     params={"q":q,"size":3},  
                     headers={"Authorization":f"Bearer {BRAVE_KEY}"})  
    return jsonify(r.json())

@app.route("/file-analyze", methods=["POST"])  
def file_analyze():  
    txt = request.files["file"].read().decode()  
    r = openai.ChatCompletion.create(  
        model="o4-mini",  # 수정: 정확한 모델명 변경 (2025-04-18 09:27:09)
        messages=[{"role":"user","content":f"다음 텍스트 요약해줘:\n{txt}"}]  
    )  
    return jsonify(summary=r.choices[0].message.content)

@app.route("/image-analyze", methods=["POST"])  
def image_analyze():  
    img = request.files["image"].read()  
    r = openai.ChatCompletion.create(  
        model="o4-mini",  # 수정: 정확한 모델명 변경 (2025-04-18 09:27:09)
        messages=[{"role":"user","content":"이 이미지에 무엇이 보이나요?"}],  
        files=[{"name":"img.png","data":img}]  
    )  
    return jsonify(desc=r.choices[0].message.content)

@app.route("/generate", methods=["POST"])  
def gen_image():  
    p = request.json["prompt"]  
    r = openai.Image.create(prompt=p, n=1, size="512x512")  
    return jsonify(url=r["data"][0]["url"])

if __name__=="__main__":  
    app.run(debug=True)