#Author: Miguel Grinberg and Carlos Tezna
import time
import threading
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class CameraEvent(object):
    """An Event-like class that signals all active clients when a new frame is
    available.
    """
    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()


class BaseCamera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    is_active = 0  # if client is asking for frames
    thread_duration = 0 # how long camera threads will last
    event = CameraEvent()

    def __init__(self, start_thread=0, duration=10):
        """Starts background thread if user specifies"""
        BaseCamera.thread_duration = duration
        if start_thread == 1:
            BaseCamera.start_camera_thread()

    def start_camera_thread(self):
        """ Starts camera thread """
        if BaseCamera.thread is None:
            BaseCamera.last_access = time.time()
            BaseCamera.is_active =  1
            # start background frame thread
            BaseCamera.thread = threading.Thread(target=self._thread)
            BaseCamera.thread.start()

            # wait until frames are available
            while self.get_frame() is None:
                time.sleep(0)

    def stop_camera_thread(self):
        """ Stops camera thread """
        BaseCamera.thread = None
        BaseCamera.is_active = 0

    def get_frame(self):
        """Return the current camera frame."""
        BaseCamera.last_access = time.time()
        # wait for a signal from the camera thread
        BaseCamera.event.wait()
        BaseCamera.event.clear()

        return BaseCamera.frame

    @staticmethod
    def frames():
        """"Generator that returns frames from the camera."""
        raise RuntimeError('Must be implemented by subclasses.')

    @classmethod
    def _thread(cls):
        """Camera background thread."""
        print('Starting camera thread.')
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.event.set()  # send signal to clients
            time.sleep(0)

            # if client asks for stream to close or
            # if there hasn't been any clients asking for frames in
            # certain time period then stop the thread
            if BaseCamera.is_active == 0 or \
            time.time() - BaseCamera.last_access > BaseCamera.thread_duration:
                frames_iterator.close()
                print('Stopping camera thread.')
                break
        BaseCamera.thread = None