""""""
import os

import gtts
from pygame.mixer import music
from elevenlabs import generate,save,api

from lib import Settings
from lib.logger import Logger

# ---- This file make the TTS ----
class Audio:
    """
    A class for manage the audio in Virgil
    """
    def __init__(self):
        self.logger = Logger()
        self.settings = Settings()

        self.volume = self.settings.volume
        self.api_key = self.settings.elevenlabs

    def create(self,text:str = "",file:bool = False,namefile:str = "") -> None:
        """
        Create a mp3 or wav file with text from tts

        Args:
            text (str, optional): the text to transform in audio. Defaults to "".
            file (bool, optional): is a file? Defaults to False.
            namefile (str, optional): the file to play Defaults to "".
        """
        music.unload()
        if music.get_volume != float(self.volume):
            music.set_volume(float(self.volume))
            if file:
                file = os.path.join(f"asset/{namefile}.mp3")
                music.load(file)
                music.play()
                return
            try:
                sound = generate(
                    api_key = self.api_key,
                    text=text,
                    voice="Antoni",
                    model='eleven_multilingual_v1'
                )
                save(sound,'audio.mp3')
            except api.error.APIError:
                print(self.logger.log(" Google text to speech has started the cause could be a missing valid key or the end of the elevenLabs plan if you are aware of this you can ignore the message"), flush=True)
                sound = gtts.gTTS(text,lang=self.settings.language)
                sound.save("audio.mp3")

        file = os.path.join("audio.mp3")
        music.load(file)
        music.play()
