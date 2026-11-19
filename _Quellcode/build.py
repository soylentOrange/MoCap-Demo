import base64, gzip, json, sys
dl = sys.argv[1]; out = sys.argv[2]
s = open(sys.argv[3]).read()
ver = json.load(open(f"{dl}/package/package.json"))["version"]
def r(path): return base64.b64encode(gzip.compress(open(path,'rb').read(), 9)).decode()
for key, path in [("BUNDLE","package/vision_bundle.mjs"),("WASMJS","package/wasm/vision_wasm_internal.js"),
                  ("WASM","package/wasm/vision_wasm_internal.wasm"),("FULL","pose_landmarker_full.task"),("LITE","pose_landmarker_lite.task")]:
    s = s.replace(f"__RES_{key}__", r(f"{dl}/{path}"))
s = s.replace("__MP_VERSION__", ver)
open(out,'w').write(s)
