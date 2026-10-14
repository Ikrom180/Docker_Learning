#-> Docker pulls python:3.12-slim from Docker Hub (if not cached locally).
FROM  python:3.12-slim

COPY requirements.txt /app/

COPY src /app/

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["python", "server.py"]

# CMD ["python", "server.py"]
#🔄 CMD vs RUN:

#RUN = build time
#
#CMD = container startup time
#
#
#COPY requirements.txt /app/
#
#
#2️⃣ COPY requirements.txt /app/
#Your version: "they put req files inside app"
#
#Correct. But note:
#
#COPY <source> <destination>
#
#requirements.txt is on your host machine (where you run docker build).
#
#/app/ is a directory inside the image.
#
#Docker creates /app automatically if it doesn't exist.
#
#The file ends up at /app/requirements.txt.
#
#⚠️ Important: The COPY command's source is relative to the build context (usually the folder containing the Dockerfile), not your whole computer.
#
#
#COPY src /app/
#3️⃣ COPY src /app/
#Your version: "they put inside src all files to inside app"
#
#Correct.
#
#Copies the entire src folder from your host into /app/ inside the image.
#
#So if src/ contains server.py, it becomes /app/server.py.
#
#If src/ contains subfolders, they're copied too.
#
#
#CMD ["python", "server.py"]
#🔄 CMD vs RUN:
#
#RUN = build time
#
#CMD = container startup time