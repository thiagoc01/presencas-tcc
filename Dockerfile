FROM python:3.12.7-alpine

RUN adduser -h /app -u 2024 -D -s /bin/false presencas

WORKDIR /app

ADD . .

RUN chown -R presencas:presencas /app && touch /var/log/presencas.log && chown presencas:presencas /var/log/presencas.log

USER presencas

RUN pip3 install -r requirements.txt

ENV PATH "/app/.local/bin:$PATH"

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0", "-w", "4", "-c", "presencas/log.py", "presencas:app"]
