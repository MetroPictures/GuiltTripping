import os, json, logging
from sys import argv, exit
from time import sleep

from core.vars import BASE_DIR
from core.api import MPServerAPI
from core.video_pad import MPVideoPad

class GuiltTripping(MPServerAPI, MPVideoPad):
	def __init__(self):
		MPServerAPI.__init__(self)

		self.main_video = "guilt_tripping.mp4"		
		self.conf['d_files'].update({
			'vid' : {
				'log' : os.path.join(BASE_DIR, ".monitor", "%s.log.txt" % self.conf['rpi_id'])
			},
			'video_listener_callback' : {
				'log' : os.path.join(BASE_DIR, ".monitor", "%s.log.txt" % self.conf['rpi_id']),
				'pid' : os.path.join(BASE_DIR, ".monitor", "video_listener_callback.pid.txt")
			}
		})

		MPVideoPad.__init__(self)
		logging.basicConfig(filename=self.conf['d_files']['module']['log'], level=logging.DEBUG)

	def video_listener_callback(self, info):
		try:
			video_info = json.loads(self.db.get("video_%d" % info['index']))
			video_info.update(info['info'])
		except Exception as e:
			video_info = info['info']

		self.db.set("video_%d" % info['index'], json.dumps(video_info))		
		logging.info("VIDEO INFO UPDATED: %s" % self.db.get("video_%d" % info['index']))

	def stop(self):
		if not super(GuiltTripping, self).stop():
			return False

		return self.stop_video_pad()

	def play_main_voiceover(self):
		self.play_video(self.main_video, video_callback=self.video_listener_callback)
		return self.say(os.path.join("prompts", "guilt_tripping.wav"), interruptable=True)

	def press(self, key):
		logging.debug("(press overridden.)")

		try:
			return self.pause() and \
				self.unmute_video(self.main_video) and \
				self.unpause() and \
				self.mute_video(self.main_video)
		except Exception as e:
			print e, type(e)
		
		return False

	def reset_for_call(self):
		for video_mapping in self.video_mappings:
			self.db.delete("video_%s" % video_mapping.index)

		super(GuiltTripping, self).reset_for_call()

	def on_hang_up(self):
		self.stop_video_pad()
		return super(GuiltTripping, self).on_hang_up()

	def run_script(self):
		super(GuiltTripping, self).run_script()
		self.play_main_voiceover()

if __name__ == "__main__":
	res = False
	gt = GuiltTripping()

	if argv[1] in ['--stop', '--restart']:
		res = gt.stop()
		sleep(5)

	if argv[1] in ['--start', '--restart']:
		res = gt.start()

	exit(0 if res else -1)
