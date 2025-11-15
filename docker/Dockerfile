FROM python:3.12-alpine AS builder
WORKDIR /app

# Install build tools for PyInstaller
RUN apk add --no-cache py3-pip build-base linux-headers

COPY app.py .

RUN pip install pyinstaller
RUN pyinstaller --onefile app.py

# Runtime
FROM alpine:3.20
COPY --from=builder /app/dist/app /server
EXPOSE 80
ENTRYPOINT ["/server"]
