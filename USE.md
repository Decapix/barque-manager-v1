local :

cd /home/solenopsis/Documents/work-business/barque-postauto/dev/manager-small-v0.0.1
source .env/bin/activate
cd barque-manager-v1
uvicorn main:app --reload --port 8020
