FROM python:3.9
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

# Define environment variable
ENV DATABASE_URL="sqlite:///./predictions.db"
# ENV FLASK_APP=app/main.py
# ENV FLASK_RUN_PORT=8000
EXPOSE 8000
# CMD ["flask", "run", "--host=0.0.0.0"]
ENTRYPOINT ["python"]
CMD [ "app/main.py"]