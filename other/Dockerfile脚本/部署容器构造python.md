cat > app.py <<EOF
from flask import Flask
import json
app = Flask(__name__)
@app.route('/')
def index():
    resp = {"code": 0, "status": "1", "userid": "2"}
    resp = json.dumps(resp)
    return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=False)
EOF

cat > Dockerfile <<EOF
FROM python:3.6-alpine
MAINTAINER XenonStack
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com flask
EXPOSE 5001
CMD ["python", "app.py"]
EOF

docker build -t k8s_python_sample_code .

