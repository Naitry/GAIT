from elevenlabs import generate, play
import whisper

model = whisper.load_model("base")
result = model.transcribe("audio file")
outputText = result["text"]


audio = generate{
        text ="Hey, my name is Clyde!",
        voice="Clyde",
        model="eleven_monolinqual_v1"
        }

play(audio)
