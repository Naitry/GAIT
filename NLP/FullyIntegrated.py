from elevenlabs import generate, play
import whisper

model: whisper.Whisper = whisper.load_model("base")
result: dict[str, str | list[dict[str, int]]] = model.transcribe("audio file")
outputText: str = result["text"]

# audio: bytes = generate(text="Hey, my name is Clyde!",
# 						voice="Clyde",
# 						model="eleven_monolingual_v1")
#
# play(audio)
