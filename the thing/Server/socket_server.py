import asyncio
import websockets
import wave
import struct

# create handler for each connection


async def handler(websocket):
    with open("data.bin", "wb+") as f:
        f.close()
    while True:
        try:
            data_chunk = await websocket.recv()
            if data_chunk.lower() == "done":
                print("Done!")
                break
        except websockets.ConnectionClosed:
            break
        with open("data.bin", "ab+") as f:
            f.write(data_chunk)

    channels = 1
    sample_width = 2  # 16-bit
    frame_rate = 44100
    n_frames = 200  # number of frames to write
    comptype = "NONE"
    compname = "not compressed"

    with wave.open("server/output.wav", "w") as wav_file:
        wav_file.setparams(
            (channels, sample_width, frame_rate, n_frames, comptype, compname))
        with open("data.bin", "rb") as bin_file:
            data_chunk = bin_file.read(2)
            while data_chunk:
                # convert the 2 bytes to a signed 16-bit integer
                sample = struct.unpack("<h", data_chunk)[0]
                # write the sample to the WAV file
                wav_file.writeframesraw(struct.pack("<h", sample))
                data_chunk = bin_file.read(2)
    import speech_to_text, summarization, pdf
    print("Converting speech to text...")
    text = speech_to_text.startConvertion()
    print("Text: {}".format(text))
    print("Generating summary...")
    summary = summarization.summary(text)
    print("Summary: {}".format(summary))
    pdf.generate_pdf(summary)
    await websocket.send(summary)
    print("Sent summary!")
    await handler(websocket)
async def main():
    print("Started!")
    async with websockets.serve(handler, "localhost", 5000):
        await asyncio.Future()
asyncio.run(main())