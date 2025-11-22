
const fileInput = document.getElementById('fileInput');
const preview = document.getElementById('preview');
const log = document.getElementById('log');
let currentBlob = null;

fileInput.addEventListener('change', (e)=>{
  const f = e.target.files[0];
  preview.innerHTML = '';
  if (!f) { preview.innerHTML = '<span class="text-gray-400">No file selected</span>'; return; }
  if (f.type.startsWith('image/')){
    const img = document.createElement('img'); img.src = URL.createObjectURL(f); img.className='max-h-48 object-contain';
    preview.appendChild(img);
  } else if (f.type.startsWith('video/')){
    const v = document.createElement('video'); v.src = URL.createObjectURL(f); v.controls = true; v.className='max-h-48';
    preview.appendChild(v);
  } else {
    preview.textContent = 'Unsupported file type';
  }
  log.textContent = 'File ready: ' + f.name;
  currentBlob = f;
});

document.getElementById('btnRemove').onclick = ()=> alert('Remove BG clicked — connect to backend /api/process/remove-bg');
document.getElementById('btnEnhance').onclick = ()=> alert('Enhance clicked — connect to backend /api/process/enhance-image');
document.getElementById('btnUpscale').onclick = ()=> alert('Upscale clicked — connect to backend /api/process/upscale-image');
document.getElementById('btnSubtitle').onclick = ()=> alert('Auto Subtitle clicked — connect to backend /api/process/video_subtitle');
