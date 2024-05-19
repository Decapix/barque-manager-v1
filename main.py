from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
import os
import httpx
import shutil
from fastapi.templating import Jinja2Templates
import uuid
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# c'est ce server aui se charge de la file d'attente et de l'envoi des video au server ia
# on a besoin de celery rabbitmq



# add db https://www.youtube.com/watch?v=__XNtJ3pDh0&t=14055s
# we have a database on oracl cloud =>  HEDT2N0D1FEUGLTCAlways

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/received_videos", StaticFiles(directory="received_videos"), name="received_videos")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def send_file(image, video, callback_url, key):
    files = {
        "image": ("image", image, 'image/png'),  # Assumption for content type
        "video": ("video", video, 'video/mp4')   # Assumption for content type
    }
    data = {"callback_url": callback_url, "key": key}
    with httpx.Client() as client:
        response = client.post("https://nscompetentkowalevskvbubdixu-barque-des-rapteux-server-ia.functions.fnc.fr-par.scw.cloud/upload/", files=files, data=data)
    return response.status_code


@app.post("/send/")
async def send_to_processing(image: UploadFile = File(...), video: UploadFile = File(...)):
    image_data = await image.read()
    video_data = await video.read()
    callback_url = "https://la-barque-des-rapteux.ovh/callback/"
    key = "labarquedesrapteux-jsuisdansmaparanioa"
    send_file(image_data, video_data, callback_url, key)
    return RedirectResponse(url="/receive/", status_code=303)



@app.post("/callback/")
async def receive_processed_video(video: UploadFile = File(...)):
    path_to_save = os.path.join("received_videos", f"{uuid.uuid4()}.mp4")

    with open(path_to_save, "wb") as f:
        shutil.copyfileobj(video.file, f)
    return {"message": "Processed video received and saved"}




##################################################################################
# interface utilisateur 
##################################################################################


@app.get("/gallery/")
async def show_gallery(request: Request):
    video_dir = 'received_videos'
    videos = os.listdir(video_dir)
    return templates.TemplateResponse("gallery.html", {"request": request, "videos": videos})



@app.get("/delete/{filename}")
async def delete_file(filename: str):
    os.remove(os.path.join('received_videos', filename))
    return RedirectResponse(url="/gallery/", status_code=303)



@app.get("/receive/")
async def show_gallery(request: Request):
    return templates.TemplateResponse("receive.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("send.html", {"request": request})




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)