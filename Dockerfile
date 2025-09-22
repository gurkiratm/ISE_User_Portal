FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

RUN chmod +x /app/entrypoint.sh

# CMD ["python", "ISE_user_portal.py"]
ENTRYPOINT ["/app/entrypoint.sh"]