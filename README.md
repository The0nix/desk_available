### Server:
```
cd server
WEB_CONCURRENCY=1 uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

### Client:
```
cd client
python .
```
