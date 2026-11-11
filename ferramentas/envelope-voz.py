# Uso: python ferramentas/envelope-voz.py <ffmpeg> <total de quadros>  (rode dentro de motion/; lê src/linha.json e public/voz/, grava src/voz-envelope.json)
# Energia da voz por quadro (30 q/s) em faixas de frequência, para a onda reagir à fala de verdade.
import sys, json, subprocess
import numpy as np
ff=sys.argv[1]; SR=16000; FPS=30; N=int(sys.argv[2]) if len(sys.argv)>2 else 1800; NB=32
linha=json.load(open('src/linha.json'))['falas']
total=np.zeros(int(N/FPS*SR)+SR); quem=np.zeros(N,dtype=np.int8)  # 0 ninguém, 1 vendedor, 2 hub
for fa in linha:
    raw=subprocess.run([ff,'-v','error','-i','public/voz/'+fa['arq'],'-f','f32le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
    a=np.frombuffer(raw,np.float32)
    ini=int(fa['trim']/FPS*SR); fim=len(a) if fa['dur']==0 else ini+int(fa['dur']/FPS*SR)
    seg=a[ini:fim]; p=int(fa['em']/FPS*SR)
    total[p:p+len(seg)]+=seg[:max(0,len(total)-p)]
    q0=fa['em']; q1=min(N,fa['em']+int(np.ceil(len(seg)/SR*FPS)))
    quem[q0:q1]=1 if fa['quem']=='vendedor' else 2
win=1024; hann=np.hanning(win)
freqs=np.fft.rfftfreq(win,1/SR)
edges=np.geomspace(90,5200,NB+1)
bands=np.zeros((N,NB)); rms=np.zeros(N)
for q in range(N):
    c=int((q+0.5)/FPS*SR); s=total[max(0,c-win//2):c+win//2]
    if len(s)<win: s=np.pad(s,(0,win-len(s)))
    rms[q]=np.sqrt(np.mean(s**2))
    sp=np.abs(np.fft.rfft(s*hann))
    for b in range(NB):
        m=(freqs>=edges[b])&(freqs<edges[b+1]); bands[q,b]=sp[m].mean() if m.any() else 0
# compressão (voz tem faixa dinâmica grande) e normalização
bands=np.log1p(bands*20); bands/=np.percentile(bands[bands>0],98); bands=np.clip(bands,0,1)
rms=np.log1p(rms*40); rms/=np.percentile(rms[rms>0],98); rms=np.clip(rms,0,1)
# ataque rápido, soltura lenta (como um medidor de áudio)
def suaviza(x,at=0.65,rel=0.18):
    y=np.zeros_like(x)
    for i in range(1,len(x)):
        k=at if (x[i]>y[i-1]).any() else rel
        y[i]=y[i-1]+(x[i]-y[i-1])*np.where(x[i]>y[i-1],at,rel)
    return y
bands=suaviza(bands); rms=suaviza(rms[:,None])[:,0]
json.dump({'bandas':np.round(bands,3).tolist(),'rms':np.round(rms,3).tolist(),'quem':quem.tolist()},open('src/voz-envelope.json','w'))
print('ok', bands.shape, 'rms>0.2 em', int((rms>0.2).sum()), 'quadros')
