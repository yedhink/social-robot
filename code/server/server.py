import tornado.ioloop
import tornado.web
import tornado.httpserver
import classify
import storage as st
import os
import cv2
import threading
from arduino_controller import RunServos
from os import listdir

labels = listdir(
    "../classification/make_dataset/filtered_dataset/")
labels.sort()

arduino_handler = RunServos()


class Userform(tornado.web.RequestHandler):
    # render our template
    def get(self):
        self.render("upload.html")


class Upload(tornado.web.RequestHandler):

    """
    Start the servos on a seperate non-blocking thread
    Handle the GET requests
    Send received bytes for classification
    """
    @tornado.web.asynchronous
    def post(self):
        if not arduino_handler.thread_running and classify.global_prediction is not "person":
            servo_thread = threading.Thread(target=arduino_handler.rotate_base)
            servo_thread.start()
            arduino_handler.thread_running = True
        print("Post request")
        fileinfo = self.request.files['image'][0]
        # filename will be cookie+extension
        fname = fileinfo['filename']
        # create our hash for later oauth
        st.up_file(fname)
        fh = open(st.__UPLOADS__+fname, 'wb')
        fh.write(fileinfo['body'])
        fh.close()
        image = cv2.imread(st.__UPLOADS__+fname)

        cv2.imwrite(st.__UPLOADS__+fname, image)
        st.prediction = classify.predict(fname, labels)
        print("The image has been received\n")
        self.finish(fname + " is uploaded!! Check %s folder" % st.__UPLOADS__)


class Download(tornado.web.RequestHandler):

    """
    Send the prediction to the android phone
    """

    def get(self):
        self.set_header('Content-Type', 'text/plain')
        if len(st.prediction) != 0:
            b = st.prediction[0].encode()
            print("Converted image has been sent to the device\n")
        else:
            b = ""
            print("Unidentified image")
        self.write(b)


application = tornado.web.Application([
    (r"/", Userform),
    (r"/upload", Upload),
    (r"/download", Download),
], debug=True)


if __name__ == "__main__":
    if not os.path.isdir("./uploads"):
        os.makedirs("./uploads")
    if not os.path.isdir("./grayscale"):
        os.makedirs("./grayscale")
    print("\nlabels = {}\n".format(labels))
    server = tornado.httpserver.HTTPServer(application)
    port = 8000
    server.bind(port)
    print(f"The Server is running on {port}!\n")
    server.start()
    tornado.ioloop.IOLoop.instance().start()
