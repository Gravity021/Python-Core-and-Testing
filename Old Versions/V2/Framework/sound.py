class Sound:
    def __init__(self, clip, channel, volume=1, play_times=0):
        self.clip = clip
        self.channel = channel
        self.volume = volume
        self.loops = play_times