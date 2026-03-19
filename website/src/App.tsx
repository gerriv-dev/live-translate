import Hls from "hls.js";
import { useEffect, useRef, useState } from "react";

export default function App() {
  const [serverIp, setServerIp] = useState<string | null>(null);
  const stream = useRef<HTMLAudioElement>(null);
  fetch("/server-ip").then(async (response) =>
    setServerIp((await response.json()).ip),
  );

  useEffect(() => {
    if (Hls.isSupported() && serverIp && stream.current) {
      const hls = new Hls();
      hls.on(Hls.Events.MEDIA_ATTACHED, () => {
        hls.loadSource(`http://${serverIp}:8888/mic/index.m3u8`);
      });
      hls.attachMedia(stream.current);
    }
  }, [serverIp]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-8 bg-black text-white">
      <div className="flex flex-col items-center">
        <h1 className="text-3xl font-bold tracking-widest">Übersetzung</h1>
        <p className="text-xs font-light tracking-tight">
          Live-Übersetzung der Bibelgemeinde Gifhorn
        </p>
      </div>
      <audio ref={stream} controls autoPlay />
    </div>
  );
}
