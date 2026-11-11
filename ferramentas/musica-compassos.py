# Uso: python ferramentas/musica-compassos.py <ffmpeg> <faixa.wav>  (acha o andamento e compara cada compasso com os "gêmeos", para emendas e repetições sem pulo)
# Acha o andamento da faixa e compara cada compasso com os compassos "gêmeos" (4 e 8 compassos antes/depois):
# o compasso com a voz estranha destoa dos gêmeos na faixa da voz (300–3000 Hz).
import sys, subprocess, numpy as np
ff, arq = sys.argv[1], sys.argv[2]
sr=22050
raw=subprocess.run([ff,'-v','error','-i',arq,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout
x=np.frombuffer(raw,np.float32)
hop=256; n=2048; win=np.hanning(n)
fr=np.lib.stride_tricks.sliding_window_view(x,n)[::hop]*win
S=np.abs(np.fft.rfft(fr,axis=1)); f=np.fft.rfftfreq(n,1/sr)
# tempo por autocorrelação do fluxo espectral
flux=np.maximum(0,np.diff(np.log1p(S),axis=0)).sum(1); flux-=flux.mean()
ac=np.correlate(flux,flux,'full')[len(flux)-1:]
fps=sr/hop; lags=np.arange(len(ac))/fps
bpms=60/lags[1:]; ok=(bpms>90)&(bpms<150); i=np.argmax(ac[1:][ok]); bpm=bpms[ok][i]
print('bpm aprox', round(bpm,2))
# fase: maximiza a soma do fluxo nas batidas
beat=60/bpm; best=None
for ph in np.linspace(0,beat,64,endpoint=False):
    t=np.arange(ph,len(x)/sr,beat); idx=(t*fps).astype(int); idx=idx[idx<len(flux)]
    v=flux[idx].sum()
    if best is None or v>best[0]: best=(v,ph)
ph=best[1]; print('fase', round(ph,3))
bar=4*beat
banda=(f>300)&(f<3000)
nb=int((len(x)/sr-ph)//bar)
spec=[]
for b in range(nb):
    a=int((ph+b*bar)*fps); z=int((ph+(b+1)*bar)*fps)
    spec.append(np.log1p(S[a:z][:,banda]).mean(0))
spec=np.array(spec)
print('compasso  início(s faixa)  início(s vídeo)  diferença p/ gêmeos')
for b in range(nb):
    viz=[spec[b+k] for k in (-8,-4,4,8) if 0<=b+k<nb]
    d=min(np.abs(spec[b]-v).mean() for v in viz) if viz else 0
    t0=ph+b*bar
    print(f'{b:3d}  {t0:6.2f}  {t0+20/30:6.2f}  {d:.4f}')
