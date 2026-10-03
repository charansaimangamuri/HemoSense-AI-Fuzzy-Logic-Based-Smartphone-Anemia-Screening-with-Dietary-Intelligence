import { useRef, useState, useEffect } from 'react'
import { MAX_IMAGES, MIN_IMAGES } from '../api.js'
import Icon from './Icon.jsx'

const ACCEPTED = ['image/jpeg', 'image/png', 'image/webp', 'image/bmp']
const MAX_MB = 10

const TIPS = [
  { icon: 'sun', title: 'Even daylight', text: 'Avoid coloured or dim light.' },
  { icon: 'eye', title: 'Show the lining', text: 'Gently pull the lower eyelid down.' },
  { icon: 'camera', title: '10–15 cm away', text: 'Steady, no filters or flash glare.' },
  { icon: 'image', title: 'Both eyes', text: 'Several angles give a stronger result.' },
]

let nextId = 1

export default function PhotoUploader({ photos, setPhotos, disabled }) {
  const fileInput = useRef(null)
  const [dragging, setDragging] = useState(false)
  const [notice, setNotice] = useState(null)
  
  // WebRTC Camera State
  const [isCameraOpen, setIsCameraOpen] = useState(false)
  const videoRef = useRef(null)
  const streamRef = useRef(null)

  async function openCamera() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment' } 
      })
      streamRef.current = stream
      setIsCameraOpen(true)
    } catch (err) {
      alert("Camera access denied or unavailable on this device.")
    }
  }

  function closeCamera() {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(t => t.stop())
      streamRef.current = null
    }
    setIsCameraOpen(false)
  }

  function capturePhoto() {
    if (!videoRef.current) return
    const video = videoRef.current
    const canvas = document.createElement('canvas')
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    const ctx = canvas.getContext('2d')
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
    
    canvas.toBlob((blob) => {
      if (!blob) return
      const file = new File([blob], `camera-${Date.now()}.jpg`, { type: 'image/jpeg' })
      addFiles([file])
      closeCamera()
    }, 'image/jpeg', 0.9)
  }

  useEffect(() => {
    if (isCameraOpen && videoRef.current && streamRef.current) {
      videoRef.current.srcObject = streamRef.current
    }
  }, [isCameraOpen])

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(t => t.stop())
      }
    }
  }, [])

  function addFiles(fileList) {
    const incoming = Array.from(fileList || [])
    const rejected = []
    const accepted = []
    for (const f of incoming) {
      if (!ACCEPTED.includes(f.type)) rejected.push(`${f.name}: unsupported format`)
      else if (f.size > MAX_MB * 1024 * 1024) rejected.push(`${f.name}: larger than ${MAX_MB} MB`)
      else accepted.push(f)
    }
    const room = MAX_IMAGES - photos.length
    if (accepted.length > room) {
      rejected.push(`Only ${MAX_IMAGES} photos allowed — ${accepted.length - room} skipped`)
    }
    const added = accepted.slice(0, Math.max(room, 0)).map((file) => ({
      id: nextId++,
      file,
      url: URL.createObjectURL(file),
    }))
    if (added.length) setPhotos((prev) => [...prev, ...added])
    setNotice(rejected.length ? rejected : null)
  }

  function remove(id) {
    setPhotos((prev) => {
      const p = prev.find((x) => x.id === id)
      if (p) URL.revokeObjectURL(p.url)
      return prev.filter((x) => x.id !== id)
    })
  }

  const full = photos.length >= MAX_IMAGES
  const locked = full || disabled
  const pct = Math.min(100, (photos.length / MAX_IMAGES) * 100)
  const pick = () => fileInput.current?.click()

  return (
    <section className="card">
      <div className="card-head">
        <div className="card-title">
          <div className="card-icon">
            <Icon name="camera" />
          </div>
          <div>
            <h2>Conjunctiva photos</h2>
            <p>
              Upload {MIN_IMAGES}–{MAX_IMAGES} close-ups of the lower eyelid
            </p>
          </div>
        </div>
        <div className={`counter ${photos.length >= MIN_IMAGES ? 'ok' : ''}`}>
          <div className="meter" aria-hidden="true">
            <div className="meter-bar" style={{ width: `${pct}%` }} />
          </div>
          <span>
            <strong>{photos.length}</strong> / {MAX_IMAGES}
          </span>
        </div>
      </div>

      <div className="card-body">
        {isCameraOpen ? (
          <div className="camera-container" style={{ display: 'flex', flexDirection: 'column', gap: '16px', alignItems: 'center', padding: '20px', background: '#f8f9fa', borderRadius: '8px' }}>
            <video 
              ref={videoRef} 
              autoPlay 
              playsInline 
              style={{ width: '100%', maxWidth: '400px', borderRadius: '8px', backgroundColor: '#000', transform: 'scaleX(-1)' }} 
            />
            <div style={{ display: 'flex', gap: '12px' }}>
              <button type="button" className="btn btn-primary" onClick={capturePhoto} style={{ background: '#2563eb', color: 'white', border: 'none' }}>
                <Icon name="camera" size={16} /> Capture
              </button>
              <button type="button" className="btn" onClick={closeCamera}>
                Cancel
              </button>
            </div>
          </div>
        ) : photos.length === 0 ? (
          <div
            className={`dropzone ${dragging ? 'dragging' : ''} ${locked ? 'disabled' : ''}`}
            onDragOver={(e) => {
              e.preventDefault()
              if (!locked) setDragging(true)
            }}
            onDragLeave={() => setDragging(false)}
            onDrop={(e) => {
              e.preventDefault()
              setDragging(false)
              if (!locked) addFiles(e.dataTransfer.files)
            }}
          >
            <div className="dropzone-icon">
              <Icon name="upload" size={22} />
            </div>
            <h3>Drag and drop eye photos here</h3>
            <div className="dropzone-buttons">
              <button type="button" className="btn" disabled={locked} onClick={pick}>
                <Icon name="image" size={16} /> Browse files
              </button>
              <button
                type="button"
                className="btn"
                disabled={locked}
                onClick={openCamera}
              >
                <Icon name="camera" size={16} /> Use camera
              </button>
            </div>
            <p className="hint">JPG, PNG, WEBP or BMP · up to {MAX_MB} MB each</p>
          </div>

        ) : (
          <ul
            className="thumbs"
            style={{ marginTop: 0 }}
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => {
              e.preventDefault()
              if (!locked) addFiles(e.dataTransfer.files)
            }}
          >
            {photos.map((p, i) => (
              <li key={p.id} className="thumb">
                <img src={p.url} alt={`Eye photo ${i + 1}`} />
                <span className="thumb-index">#{i + 1}</span>
                {!disabled && (
                  <button
                    type="button"
                    className="thumb-remove"
                    aria-label={`Remove photo ${i + 1}`}
                    onClick={() => remove(p.id)}
                  >
                    <Icon name="x" size={14} strokeWidth={2.4} />
                  </button>
                )}
              </li>
            ))}
            {!locked && (
              <li>
                <button type="button" className="thumb-add" onClick={pick}>
                  <Icon name="plus" size={20} />
                  Add photo
                </button>
              </li>
            )}
          </ul>
        )}

        {notice && (
          <div className="alert alert-warn" style={{ marginTop: 14 }}>
            <Icon name="alert" />
            <div>
              <div className="alert-title">Some files were not added</div>
              <ul>
                {notice.map((n) => (
                  <li key={n}>{n}</li>
                ))}
              </ul>
            </div>
          </div>
        )}

        <ul className="tips">
          {TIPS.map((t) => (
            <li key={t.title}>
              <Icon name={t.icon} size={16} />
              <span>
                <strong>{t.title}</strong>
                {t.text}
              </span>
            </li>
          ))}
        </ul>

        <input
          ref={fileInput}
          type="file"
          accept={ACCEPTED.join(',')}
          multiple
          hidden
          onChange={(e) => {
            addFiles(e.target.files)
            e.target.value = ''
          }}
        />
      </div>
    </section>
  )
}
