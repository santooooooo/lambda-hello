FROM python:3.10-slim

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
ARG IS_TEST="False"
ENV IS_TEST=${IS_TEST}
# 実行日（JST, YYYY-MM-DD）。未指定や空なら従来ロジック（12週間前の平日）を使用
ARG EXECUTE_DATE=""
ENV EXECUTE_DATE=${EXECUTE_DATE}

COPY ./aws-batch/ .

CMD ["pipenv", "run","python", "-m", "aws-batch.app"]
