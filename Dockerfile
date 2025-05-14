FROM python:3.8-slim

WORKDIR /app

RUN apt-get update
COPY . /app/

# Pipenv をインストール
RUN pip install --no-cache-dir pipenv

# プロジェクトのファイルをコンテナにコピー
COPY Pipfile Pipfile.lock ./

# Pipfile.lock が存在する場合は、それに基づいて依存関係をインストール
RUN if [ -f Pipfile.lock ]; then \
    pipenv sync --dev; \
    else \
    pipenv install --dev; \
    fi

# 環境変数の設定
ENV IS_TEST="False"

COPY ./aws-batch/ .

CMD ["pipenv", "run","python", "-m", "aws-batch.app"]
