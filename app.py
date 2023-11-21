import os
import gi
import tempfile
import time
import multiprocessing


gi.require_version('Gst', '1.0')


from gi.repository import GObject, Gst


Gst.init(None)
Gst.debug_set_active(False)


class Screencast(GObject.GObject):
    __gsignals__ = {
        "flush-done": (GObject.SignalFlags.RUN_LAST, None, ())
    }


    def __init__(self,parent):
        GObject.GObject.__init__(self)
        self.parent = parent
        self.temp_fh = tempfile.mkstemp(prefix="kazam_", dir='./', suffix=".webm")
        self.tempfile = self.temp_fh[1]
        self.muxer_tempfile = "{0}.mux".format(self.tempfile)
        self.pipeline = Gst.Pipeline()
        self.area = None
        self.xid = None
        self.crop_vid = False
        self.cores = max(1, multiprocessing.cpu_count() - 1)
        self.setup_sources()


    def setup_sources(self, video_source={'x': 0, 'y': 0, 'width': 1920, 'height': 1080},
                      audio_source=int(0), audio_channels=int(2)):

        self.audio_source = audio_source
        self.audio_channels = audio_channels
        self.video_source = video_source

        self.setup_video_source()
        self.setup_audio_sources()
        self.setup_filesink()
        self.setup_pipeline()
        self.setup_links()


    def setup_video_source(self):
        self.video_src = Gst.ElementFactory.make("ximagesrc", "video_src")
        startx = self.video_source['x']
        starty = self.video_source['y']
        width = self.video_source['width']
        height = self.video_source['height']
        endx = startx + width - 1
        endy = starty + height - 1
        self.video_src.set_property("startx", startx)
        self.video_src.set_property("starty", starty)
        self.video_src.set_property("endx", endx)
        self.video_src.set_property("endy", endy)
        self.video_src.set_property("use-damage", False)
        self.video_src.set_property("show-pointer", False)
        self.video_caps = Gst.caps_from_string("video/x-raw, framerate={}/1".format(int(15)))
        self.f_video_caps = Gst.ElementFactory.make("capsfilter", "vid_filter")
        self.f_video_caps.set_property("caps", self.video_caps)
        self.video_convert = Gst.ElementFactory.make("videoconvert", "videoconvert")
        self.video_rate = Gst.ElementFactory.make("videorate", "video_rate")
        self.video_enc = Gst.ElementFactory.make('vp8enc', "video_encoder")
        self.video_enc.set_property("cpu-used", 2)
        self.video_enc.set_property("end-usage", "vbr")
        self.video_enc.set_property("target-bitrate", 800000000)
        self.video_enc.set_property("static-threshold", 1000)
        self.video_enc.set_property("token-partitions", 2)
        self.video_enc.set_property("max-quantizer", 30)
        self.video_enc.set_property("threads", self.cores)
        self.mux = Gst.ElementFactory.make("webmmux", "muxer")
        self.q_video_src = Gst.ElementFactory.make("queue", "queue_video_source")
        self.q_video_in = Gst.ElementFactory.make("queue", "queue_video_in")
        self.q_video_out = Gst.ElementFactory.make("queue", "queue_video_out")


    def setup_audio_sources(self):
        self.aud_out_queue = Gst.ElementFactory.make("queue", "queue_a_out")
        self.audioconv = Gst.ElementFactory.make("audioconvert", "audio_conv")
        self.audioenc = Gst.ElementFactory.make("vorbisenc", "audio_encoder")
        self.audioenc.set_property("quality", 1)
        self.audiosrc = Gst.ElementFactory.make("pulsesrc", "audio_src")
        self.audiosrc.set_property("device", self.audio_source)
        self.aud_caps = Gst.caps_from_string("audio/x-raw, channels=(int){}".format(self.audio_channels))
        self.f_aud_caps = Gst.ElementFactory.make("capsfilter", "aud_filter")
        self.f_aud_caps.set_property("caps", self.aud_caps)
        self.aud_in_queue = Gst.ElementFactory.make("queue", "queue_a_in")


    def setup_filesink(self):
        self.final_queue = Gst.ElementFactory.make("queue", "queue_final")
        self.sink = Gst.ElementFactory.make("filesink", "sink")
        self.sink.set_property("location", self.tempfile)


    def setup_pipeline(self):
        self.pipeline.add(self.video_src)
        self.pipeline.add(self.f_video_caps)
        self.pipeline.add(self.q_video_src)
        self.pipeline.add(self.video_rate)
        self.pipeline.add(self.video_convert)
        self.pipeline.add(self.q_video_out)
        self.pipeline.add(self.final_queue)
        self.pipeline.add(self.video_enc)
        self.pipeline.add(self.audioconv)
        self.pipeline.add(self.audioenc)
        self.pipeline.add(self.aud_out_queue)
        self.pipeline.add(self.audiosrc)
        self.pipeline.add(self.aud_in_queue)
        self.pipeline.add(self.f_aud_caps)
        self.pipeline.add(self.mux)
        self.pipeline.add(self.sink)


    def setup_links(self):
        ret = self.video_src.link(self.f_video_caps)
        ret = self.f_video_caps.link(self.q_video_src)
        ret = self.q_video_src.link(self.video_rate)
        ret = self.video_rate.link(self.video_convert)
        ret = self.video_convert.link(self.video_enc)
        ret = self.video_enc.link(self.q_video_out)
        ret = self.q_video_out.link(self.mux)
        ret = self.audiosrc.link(self.aud_in_queue)
        ret = self.aud_in_queue.link(self.f_aud_caps)
        ret = self.f_aud_caps.link(self.audioconv)
        ret = self.audioconv.link(self.audioenc)
        ret = self.audioenc.link(self.aud_out_queue)
        ret = self.aud_out_queue.link(self.mux)
        ret = self.mux.link(self.final_queue)
        ret = self.final_queue.link(self.sink)


    def start_recording(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        self.gui.update_recording_state("Идёт запись", "green")


    def pause_recording(self):
        self.pipeline.set_state(Gst.State.PAUSED)
        self.gui.update_recording_state("Пауза", "orange")


    def unpause_recording(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        self.gui.update_recording_state("Идёт запись", "green")


    def stop_recording(self):
        self.pipeline.set_state(Gst.State.NULL)
        self.emit("flush-done")
        self.gui.update_recording_state("Остановлен", "red")
