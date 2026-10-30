# Meshy GLB -> ゲーム用（色の画像1024px・金属/凹凸の画像を外す・表面をなめらかに）
import json,struct,io,sys,numpy as np
from PIL import Image
src,dst=sys.argv[1],sys.argv[2]
b=open(src,'rb').read(); l0=struct.unpack('<I',b[12:16])[0]; js=json.loads(b[20:20+l0]); off=20+l0; l1=struct.unpack('<I',b[off:off+4])[0]; bin_=b[off+8:off+8+l1]
bv=js['bufferViews']; prim=js['meshes'][0]['primitives'][0]; at=prim['attributes']
def raw(i): v=bv[i]; return bin_[v['byteOffset']:v['byteOffset']+v['byteLength']]
def acc(i,dt,n):
    a=js['accessors'][i]; v=bv[a['bufferView']]; return np.frombuffer(bin_,dtype=dt,count=a['count']*n,offset=v['byteOffset']+a.get('byteOffset',0)).reshape(-1,n)
P=acc(at['POSITION'],np.float32,3).astype(np.float64); I=acc(prim['indices'],np.uint32,1).ravel(); T=I.reshape(-1,3)
U,key=np.unique(np.round(P,5),axis=0,return_inverse=True); key=key.ravel(); TU=key[T]; nU=len(U)
E=np.concatenate([TU[:,[0,1]],TU[:,[1,2]],TU[:,[2,0]]]); E=np.concatenate([E,E[:,::-1]]); E=np.unique(E,axis=0); deg=np.bincount(E[:,0],minlength=nU).astype(float)
fn=np.cross(U[TU[:,1]]-U[TU[:,0]],U[TU[:,2]]-U[TU[:,0]]); A=np.zeros((nU,3))
for k in range(3): np.add.at(A,TU[:,k],fn)
N=A/(np.linalg.norm(A,axis=1,keepdims=True)+1e-12)
for _ in range(40):
    S=np.zeros_like(N); np.add.at(S,E[:,0],N[E[:,1]]); N=N+S/np.maximum(deg,1)[:,None]; N/=np.linalg.norm(N,axis=1,keepdims=True)
Nv=N[key].astype(np.float32)
base_tex=js['materials'][0]['pbrMetallicRoughness']['baseColorTexture']['index']; img_i=js['textures'][base_tex]['source']
im=Image.open(io.BytesIO(raw(js['images'][img_i]['bufferView']))).convert('RGB').resize((1024,1024),Image.LANCZOS); o=io.BytesIO(); im.save(o,'JPEG',quality=88,optimize=True)
newbin=bytearray(); views=[]
def add(data,target=None):
    while len(newbin)%4: newbin.append(0)
    d={'buffer':0,'byteOffset':len(newbin),'byteLength':len(data)}
    if target: d['target']=target
    newbin.extend(data); views.append(d); return len(views)-1
acs=[]
def addacc(i,data=None,mn=None,mx=None,target=34962):
    a=dict(js['accessors'][i]); a.pop('byteOffset',None)
    if data is None:
        v=bv[a['bufferView']]; comp={5126:4,5125:4,5123:2}[a['componentType']]; n={'SCALAR':1,'VEC2':2,'VEC3':3}[a['type']]
        data=bin_[v['byteOffset']+js['accessors'][i].get('byteOffset',0):][:a['count']*comp*n]
    a['bufferView']=add(bytes(data),target)
    if mn is not None: a['min'],a['max']=mn,mx
    acs.append(a); return len(acs)-1
newat={'POSITION':addacc(at['POSITION']),'NORMAL':addacc(at['NORMAL'],Nv.tobytes(),Nv.min(0).tolist(),Nv.max(0).tolist()),'TEXCOORD_0':addacc(at['TEXCOORD_0'])}
ind=addacc(prim['indices'],target=34963)
imgv=add(o.getvalue())
out={'asset':{'version':'2.0','generator':'himitsu-no-niwa prep'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0}],
 'meshes':[{'primitives':[{'attributes':newat,'indices':ind,'mode':4,'material':0}]}],
 'materials':[{'pbrMetallicRoughness':{'baseColorFactor':[1,1,1,1],'metallicFactor':0.0,'roughnessFactor':0.8,'baseColorTexture':{'index':0}},'alphaMode':'OPAQUE','doubleSided':True}],
 'textures':[{'sampler':0,'source':0}],'samplers':[{'magFilter':9729,'minFilter':9987,'wrapS':10497,'wrapT':10497}],'images':[{'mimeType':'image/jpeg','bufferView':imgv}],
 'accessors':acs,'bufferViews':views}
while len(newbin)%4: newbin.append(0)
out['buffers']=[{'byteLength':len(newbin)}]
j=json.dumps(out,separators=(',',':')).encode()
while len(j)%4: j+=b' '
data=struct.pack('<4sII',b'glTF',2,12+8+len(j)+8+len(newbin))+struct.pack('<I4s',len(j),b'JSON')+j+struct.pack('<I4s',len(newbin),b'BIN\x00')+bytes(newbin)
open(dst,'wb').write(data)
# facing check: white (belly) centroid z should be > 0
UV=acc(at['TEXCOORD_0'],np.float32,2); Aimg=np.asarray(im); h,w=Aimg.shape[:2]; C=Aimg[(UV[:,1]*(h-1)).astype(int),(UV[:,0]*(w-1)).astype(int)]
wh=C.min(1)>200; print(dst, round(len(data)/1e6,2),'MB', 'verts',len(P), 'bbox',P.min(0).round(2).tolist(),P.max(0).round(2).tolist(),'white centroid',P[wh].mean(0).round(2).tolist())
