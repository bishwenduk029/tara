import { utils } from "@ricky0123/vad-react";

let source: AudioBufferSourceNode;
let sourceIsStarted = false;
const conversationThusFar = [];

export const onSpeechStart = () => {
  console.log("speech started");
  stopSourceIfNeeded();
};

export const onSpeechStartEmpty = () => {
  console.log("speech started in wrong vad");
};

export const createOnSpeechEnd = (getToken) => {
  const onSpeechEnd = async (audio) => {
    console.log("speech ended");
    await processAudio(audio, getToken);
  };

  return onSpeechEnd;
};

export const onMisfire = () => {
  console.log("vad misfire");
};

const stopSourceIfNeeded = () => {
  if (source && sourceIsStarted) {
    source.stop(0);
    sourceIsStarted = false;
  }
};

const processAudio = async (audio, getToken) => {
  const blob = createAudioBlob(audio);
  await validate(blob);
  const supabaseAccessToken = await getToken({
    template: "supabase-tarat-clerk",
  });
  sendData(blob, supabaseAccessToken);
};

const createAudioBlob = (audio) => {
  const wavBuffer = utils.encodeWAV(audio);
  return new Blob([wavBuffer], { type: "audio/wav" });
};

const debounce = (func, timeout = 300) => {
  let timer;
  return function (...args) { // use a regular function to keep 'this' context
    clearTimeout(timer);
    timer = setTimeout(() => {
      func.apply(this, args); // 'this' refers to the function ('sendData' in this case)
    }, timeout);
  };
};

const sendData = debounce(function(blob, jwtToken) { // if 'sendData' uses 'this', make it a regular function
  console.log("sending data");
  fetch("http://localhost:8000/inference", {
    method: "POST",
    body: createBody(blob),
    headers: {
      Authorization: `bearer ${jwtToken}`,
    },
  })
    .then(handleResponse)
    .then(handleSuccess)
    .catch(handleError);
}, 10);

function base64Encode(str: string) {
  const encoder = new TextEncoder();
  const data = encoder.encode(str);
  return window.btoa(String.fromCharCode(...new Uint8Array(data)));
}

function base64Decode(base64: string) {
  const binaryStr = window.atob(base64);
  const bytes = new Uint8Array(
    [...binaryStr].map((char) => char.charCodeAt(0))
  );
  return new TextDecoder().decode(bytes);
}

const handleResponse = async (res) => {
  if (!res.ok) {
    return res.text().then((error) => {
      throw new Error(error);
    });
  }
  return res.blob();
};

const createBody = (data) => {
  const formData = new FormData();
  formData.append("audio", data, "audio.wav");
  return formData;
};

const handleSuccess = async (blob) => {
  const audioContext = new (window.AudioContext || window.webkitAudioContext)();

  stopSourceIfNeeded();

  source = audioContext.createBufferSource();
  source.buffer = await audioContext.decodeAudioData(await blob.arrayBuffer());
  source.connect(audioContext.destination);
  source.start(0);
  sourceIsStarted = true;
};

const handleError = (error) => {
  console.log(`error encountered: ${error.message}`);
};

const validate = async (data) => {
  const decodedData = await new AudioContext().decodeAudioData(
    await data.arrayBuffer()
  );
  const duration = decodedData.duration;
  const minDuration = 0.4;

  if (duration < minDuration)
    throw new Error(
      `Duration is ${duration}s, which is less than minimum of ${minDuration}s`
    );
};
