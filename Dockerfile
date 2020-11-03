FROM python:3.8

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV SECRET_KEY="61132a91df01d0a13c1c24ff081886f9" \
    SQLALCHEMY_DATABASE_URI="sqlite:///site.db"

ENTRYPOINT ["python"]

CMD ["run.py"]
