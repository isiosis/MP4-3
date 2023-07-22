import pika
import json
import tempfile
import os
from bson.objectid import ObjectId
import moviepy.editor
import logging


def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)

    # temporary file to store video
    tf = tempfile.NamedTemporaryFile()

    # get video from gridfs(mongodb)
    out = fs_videos.get(ObjectId(message["video_fid"]))
    # write the video to the created temporary file
    tf.write(out.read())

    logging.error("out: ", out)
    logging.error("ObjectID: ", ObjectId(message["video_fid"]))
    logging.error("video file created: ", tf.name)

    # create the audio file from the video
    audio = moviepy.editor.VideoFileClip(tf.name).audio

    logging.error("audio file created: ", audio)

    # close temporary file
    tf.close()

    # generate temporary file path for the audio file
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"

    # write the audio file to the temporary file path
    audio.write_audiofile(tf_path)

    # open the temporary audio file
    f = open(tf_path, "rb")

    # read the temporary audio file
    data = f.read()

    # store the audio file in gridfs(mongodb)

    fid = fs_mp3s.put(data)

    # close the temporary audio file
    f.close()

    # delete the temporary audio file
    os.remove(tf_path)

    message["mp3_fid"] = str(fid)

    try:
        # publish the message to the mp3 queue
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as err:
        fs_mp3s.delete(fid)
        return "failed to publish message"
