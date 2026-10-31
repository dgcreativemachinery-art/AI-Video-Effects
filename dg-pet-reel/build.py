#!/usr/bin/env python3
"""Builds index.html and the mixed soundtrack for the DG Tech PET reel from one edit list.

Edit EDL below and re-run:  python3 build.py
Voice is the presenter's real recordings (raw/vo/*.wav), trimmed to the spoken words.
"""
import json, subprocess, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
UP = "/root/.claude/uploads/50efbe4b-3fc4-59b5-924c-896447c25b9e"
VO_SRC = {  # real voice sources
    "IMG_8130": f"{UP}/1c40cdb7-IMG_8130.MOV", "IMG_8137": f"{UP}/2a2cc835-IMG_8137.MOV",
    "IMG_8144": f"{UP}/ec9840b2-IMG_8144.MOV", "IMG_8148": f"{UP}/b851cdcf-IMG_8148.MOV",
    "IMG_8158": f"{UP}/329f7f4d-IMG_8158.MOV", "IMG_8165": f"{UP}/0a9ac861-IMG_8165.MOV",
    "v7": f"{UP}/8c1bbc93-v7.mp4", "v8": f"{UP}/a9ccdb03-v8.mp4", "v_10": f"{UP}/8cb36b2a-v_10.mp4", "v_13": f"{UP}/a319b65c-v_13.mp4",
    "v_14": f"{UP}/16105261-v_14.mp4", "v_15": f"{UP}/e5d97b18-v_15.mp4",
}
W, H, GAP = 2160, 3840, 0.06

# Each segment: vo=(source, in, out) or dur for a voiceless beat.
# shots: (clip, media_start, duration or None=rest, motion)   motion: in|out|left|right|shake
# caps: (text, rel_start, rel_end, style, accent)   style: chin|kin|pill|slam
EDL = [
 dict(id="A", vo=("IMG_8130", 1.28, 2.62), sfx=[("impact-bass-1", 0.0, .55), ("heartbeat", 0.0, .9)],
      shots=[("p1_walk_bales", 1.28, None, "in")],
      caps=[("یہ صرف کباڑ", .02, .84, "chin", None), ("نہیں ہے!", .84, 1.34, "chin", "red")],
      pill=("DG TECH MACHINERY", 0, 1.34)),
 dict(id="A2", vo=("v_13", 3.15, 6.90), sfx=[("whoosh-short", -.05, .45), ("impact-bass-2", .55, .45)],
      shots=[("r1_flakes_presenter", 3.15, None, "out")],
      caps=[("یہ کروڑوں کا", .03, 1.09, "chin", "gold"), ("وہ خام مال ہے", 1.09, 1.95, "chin", None),
            ("دنیا جسے", 1.95, 2.79, "chin", None), ("کچرا سمجھتی ہے", 2.79, 3.75, "chin", "red")]),
 dict(id="B", vo=("IMG_8137", 0.95, 2.48), sfx=[("whoosh-short", -.05, .5)],
      shots=[("p2_pick_bottles", 0.95, None, "out")], carousel="f2",
      caps=[("لیکن ہم اس سے", .05, .79, "chin", None), ("نوٹ کمائیں گے", .79, 1.53, "chin", "gold")]),
 dict(id="M1", vo=("v_14", 0.85, 3.66), sfx=[("whoosh-cinematic", -.1, .45)],
      shots=[("r2_bales_conveyor", 0.0, None, "in")],
      caps=[("پہلا قدم", .0, .53, "kin", "gold"), ("گلی گلی سے بکھرے ہوئے", .53, 1.81, "kin", None),
            ("اس پلاسٹک کو اٹھانا", 1.81, 2.81, "kin", "cyan")],
      pill=("STEP 1 · دھلائی", 0, 2.81)),
 dict(id="M2", vo=("v_14", 3.66, 7.68), sfx=[("whoosh", -.05, .45), ("whoosh-short", 1.95, .35)],
      shots=[("r2_bales_conveyor", 4.6, 1.6, "shake"), ("ai1_wash_tank", 0.5, None, "in")],
      caps=[("پھر DG Tech مشینری کے", .02, 1.40, "kin", "gold"), ("اس طاقتور پلانٹ پر", 1.40, 2.56, "kin", None),
            ("اس کی زبردست دھلائی", 2.56, 3.60, "kin", "cyan"), ("ہوتی ہے", 3.60, 4.02, "kin", None)],
      pill=("STEP 1 · دھلائی", 0, 4.02)),
 dict(id="M3", vo=("v_14", 7.66, 9.72), sfx=[("whoosh-short", -.05, .4), ("sparkle", 1.0, .35)],
      shots=[("ai2_wash_jets", 1.4, None, "in")],
      caps=[("جہاں میل کا", .0, .86, "kin", None), ("نام و نشان مٹ جاتا ہے", .86, 2.06, "kin", "cyan")]),
 dict(id="M4", vo=("v_15", 0.0, 1.86), sfx=[("impact-bass-1", 0.0, .6), ("glitch-1", .78, .3)],
      shots=[("ai3_crusher", 0.4, None, "shake")],
      caps=[("اس کے بعد آتا ہے", .0, .8, "kin", None), ("کرشنگ کا وہ مرحلہ", .8, 1.86, "slam", "red")],
      pill=("STEP 2 · کرشنگ", 0, 1.86)),
 dict(id="M5", vo=("v_15", 2.25, 5.40), sfx=[("whoosh", -.05, .4), ("impact-bass-2", .87, .4), ("whoosh-short", 1.55, .35)],
      shots=[("ai3_crusher", 2.3, 0.9, "shake"), ("ai4_flakes_pour", 0.5, 1.3, "in"), ("r1_flakes_presenter", 0.0, None, "out")],
      caps=[("جس پر سخت بوتلیں", .0, .87, "kin", None), ("ریزہ ریزہ ہو کر", .87, 1.65, "kin", "red"),
            ("چمکدار فلیکس", 1.65, 2.47, "kin", "lime"), ("بن جاتی ہیں", 2.47, 3.15, "kin", None)],
      pill=("STEP 2 · کرشنگ", 0, 3.15)),
 dict(id="M6", vo=("v_15", 5.92, 9.45), sfx=[("whoosh", -.05, .4), ("riser", -.2, .3), ("impact-bass-1", 1.98, .7), ("chime", 2.1, .45)],
      shots=[("f1_flakes_yard", 1.5, 1.8, "in"), ("r1_flakes_presenter", 7.0, None, "in")],
      caps=[("اور یہیں سے", .0, .5, "kin", None), ("شروع ہوتی ہے", .5, 1.12, "kin", None),
            ("اصل گیم", 1.12, 1.98, "kin", "gold"), ("یعنی کیش جنریشن!", 1.98, 3.53, "top", "gold")]),
 dict(id="C", vo=("v_10", 0.72, 3.62), sfx=[("whoosh", -.05, .45)],
      shots=[("m5_factory_wide", 0.0, None, "in", 0.86)],
      caps=[("اب ان فلیکس کو", .1, .7, "kin", None), ("ڈالا جاتا ہے", .7, 1.32, "kin", None),
            ("DG Tech", 1.32, 1.7, "kin", "gold"), ("انجیکشن مولڈنگ مشین میں", 1.7, 2.9, "kin", "cyan")],
      pill=("STEP 3 · پری فارم", 0, 2.9)),
 dict(id="D", vo=("IMG_8144", 0.70, 3.33), sfx=[("whoosh-short", -.05, .45)],
      shots=[("p3_preforms", 0.70, None, "out")], carousel="f3",
      caps=[("جو بناتی ہے", .05, .72, "chin", None), ("ایک بہترین اور", .72, 1.54, "chin", None),
            ("مضبوط پری فارم", 1.54, 2.63, "chin", "cyan")]),
 dict(id="E", vo=("v_10", 5.96, 7.92), sfx=[("whoosh", -.05, .45), ("impact-bass-2", .38, .45)],
      shots=[("m2_blow_load", 2.0, None, "shake")],
      caps=[("اور پھر آخری وار", .02, 1.04, "kin", "red"), ("بلو مولڈنگ مشین", 1.04, 1.96, "kin", "cyan")],
      pill=("STEP 4 · بوتل", 0, 1.96)),
 dict(id="F", vo=("IMG_8148", 1.83, 5.32), sfx=[("whoosh-short", 1.55, .4), ("pop", 2.75, .5)],
      shots=[("p4_heater", 1.83, 1.6, "in"), ("m6_mould_closeup", 3.0, 1.15, "in"), ("m3_mould_bottles", 0.0, None, "out")],
      caps=[("جو اس پری فارم کو", .02, .79, "chin", None), ("سیکنڈوں میں", .79, 1.41, "kin", "gold"),
            ("ایک تیار بوتل میں", 1.41, 2.61, "kin", "cyan"), ("بدل دیتی ہے", 2.61, 3.49, "kin", None)]),
 dict(id="G", vo=("IMG_8158", 0.83, 2.40), sfx=[("whoosh-cinematic", -.1, .45), ("chime", .55, .5)],
      shots=[("m4_compressor", 0.83, None, "in")],
      caps=[("اب سنیے", .05, .55, "kin", None), ("پرافٹ کا فارمولا", .55, 1.57, "slam", "gold")]),
 dict(id="H", vo=("v7", 2.12, 9.50), sfx=[("whoosh", 2.35, .4), ("whoosh-short", 4.95, .4), ("sparkle", 4.9, .45), ("chime", 6.15, .4)],
      shots=[("s2_stacks_b", 1.0, 2.5, "left"), ("m1_blow_button", 1.0, 2.4, "in"), ("ai5_cash", 0.5, None, "in")],
      caps=[("یہ تیار شدہ بوتلیں", .04, 1.16, "kin", None), ("اور پروڈکٹس جب", 1.16, 1.82, "kin", None),
            ("بڑی بڑی ملٹی نیشنل", 1.82, 2.78, "kin", "cyan"), ("کمپنیوں کو سپلائی ہوتی ہیں", 2.78, 4.08, "kin", None),
            ("تو لاگت سے", 4.08, 4.9, "kin", None), ("کئی گنا زیادہ منافع", 4.9, 6.1, "slam", "gold"),
            ("سیدھا آپ کی جیب میں", 6.1, 6.94, "kin", "lime"), ("آتا ہے!", 6.94, 7.38, "kin", None)],
      pill=("STEP 5 · پرافٹ", 0, 7.38)),
 dict(id="I1", vo=("v8", 0.16, 3.66), sfx=[("whoosh", -.05, .45)],
      shots=[("s1_stacks_a", 1.0, None, "in")],
      caps=[("بغیر ایک روپیہ", .0, .78, "kin", None), ("فالتو گنوائے", .78, 1.46, "kin", "red"),
            ("صرف DG Tech مشینری", 1.46, 2.54, "kin", "gold"), ("اور دماغ چلا کے", 2.54, 3.5, "kin", "cyan")]),
 dict(id="I2", vo=("v8", 4.04, 7.30), sfx=[("whoosh-cinematic", -.1, .45), ("riser", 0.0, .3)],
      shots=[("p5_banner", 0.0, 1.3, "in"), ("GFX", 0, None, "in")],
      caps=[("پیسے گھر لے جانے کا", .04, 1.0, "kin", "lime"), ("یہ موقع", 1.0, 1.54, "kin", "gold"),
            ("ہاتھ سے جانے مت دو", 1.54, 2.52, "kin", "red"), ("یاد رکھو", 2.52, 3.26, "slam", None)]),
 dict(id="J1", vo=("v8", 7.26, 8.22), sfx=[("impact-bass-2", 0.0, .8)],
      shots=[("GFX", 0, None, "shake")], caps=[("THINK BIG", .0, .96, "slam", "gold")]),
 dict(id="J2", vo=("IMG_8165", 1.30, 2.50), tail=1.6, sfx=[("impact-bass-1", 0.0, .6)],
      shots=[("p5_banner", 1.30, 2.05, "in"), ("GFX", 0, None, "in")], caps=[("TO GET BIG", .0, 2.6, "slam", "gold")], endcard=True),
]

ACC = {"gold": "#FFC83D", "red": "#FF4B3E", "cyan": "#3FE0FF", "lime": "#8BFF5A", None: "#FFFFFF"}

def run(cmd):
    subprocess.run(cmd, check=True)

def build():
    t, plan = 0.0, []
    for s in EDL:
        if "vo" in s:
            d = s["vo"][2] - s["vo"][1] + s.get("tail", 0)
        else:
            d = s["dur"]
        plan.append((s, round(t, 3), round(d, 3)))
        t += d + GAP
    total = round(t - GAP + 0.4, 2)

    # ---------- soundtrack ----------
    os.makedirs(f"{ROOT}/assets/audio", exist_ok=True)
    inputs, filt, labels = [], [], []
    for i, (s, st, d) in enumerate(plan):
        if "vo" not in s: continue
        src, a, b = s["vo"]
        n = len(inputs)//2; inputs += ["-i", VO_SRC[src]]
        filt.append(f"[{n}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,highpass=f=80,"
                    f"loudnorm=I=-16:TP=-1.5:LRA=7,afade=t=in:d=0.02,afade=t=out:st={b-a-0.04:.3f}:d=0.04,"
                    f"aresample=48000,adelay={int(st*1000)}|{int(st*1000)}[v{i}]")
        labels.append(f"[v{i}]")
    filt.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,apad=whole_dur={total}[vo]")
    # music: ducked under the voice, louder over the voiceless montage
    n = len(inputs)//2; inputs += ["-i", f"{ROOT}/assets/music/bgm.wav"]
    vol = []
    for s, st, d in plan:
        if s.get("music_up"):
            vol.append(f"between(t,{st+0.15},{st+d-0.15})*0.55")
    vexpr = "0.16+" + "+".join(vol) if vol else "0.16"
    filt.append(f"[{n}:a]atrim=0:{total},asetpts=PTS-STARTPTS,aresample=48000,volume='{vexpr}':eval=frame,"
                f"afade=t=in:d=0.3,afade=t=out:st={total-1.5}:d=1.5[bgm]")
    sl = []
    for i, (s, st, d) in enumerate(plan):
        for j, (name, off, v) in enumerate(s.get("sfx", [])):
            path = f"{ROOT}/assets/sfx/{name}.mp3"
            if not os.path.exists(path): path = f"{ROOT}/assets/sfx/{name}.wav"
            n = len(inputs)//2; inputs += ["-i", path]
            ms = max(0, int((st + off) * 1000))
            filt.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,volume={v},adelay={ms}|{ms}[s{i}_{j}]")
            sl.append(f"[s{i}_{j}]")
    filt.append(f"[vo]aformat=channel_layouts=stereo[vos]")
    filt.append(f"[vos][bgm]{''.join(sl)}amix=inputs={2+len(sl)}:normalize=0:duration=first,"
                f"alimiter=limit=0.89,loudnorm=I=-14:TP=-1:LRA=11[out]")
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt),
         "-map", "[out]", "-ar", "48000", "-c:a", "pcm_s16le", f"{ROOT}/assets/audio/mix.wav"])

    # ---------- picture ----------
    els, js, z = [], [], 10
    sid = 0
    for s, st, d in plan:
        # shots
        ts = st
        shots = s["shots"]
        for k, sh in enumerate(shots):
            clip, ms, dur, motion = sh[:4]
            rate = sh[4] if len(sh) > 4 else 1.0
            if dur is None or k == len(shots) - 1:
                dur = st + d - ts
            dur = round(dur, 3)
            sid += 1
            i = f"sh{sid}"
            if clip == "GFX":
                els.append(f'<div id="{i}" class="clip gfx" data-start="{ts}" data-duration="{dur}" data-track-index="1" style="z-index:{z}"><div class="gfx-in" id="{i}g"><div class="orb o1"></div><div class="orb o2"></div><div class="gfx-brand">DG TECH MACHINERY</div></div></div>')
                tgt = f"#{i}g"
            else:
                rate_attr = f' data-playback-rate="{rate}"' if rate != 1.0 else ""
                els.append(f'<div id="{i}" class="shot" style="z-index:{z}">'
                           f'<div class="mv" id="{i}m"><video id="{i}v" class="clip" src="assets/footage/{clip}.mp4" data-start="{ts}" data-duration="{dur}" data-media-start="{ms}"{rate_attr} data-track-index="1" muted playsinline></video></div></div>')
                tgt = f"#{i}m"
            if motion == "in":   js.append(f'tl.fromTo("{tgt}",{{scale:1.0}},{{scale:1.12,duration:{dur},ease:"none"}},{ts});')
            elif motion == "out": js.append(f'tl.fromTo("{tgt}",{{scale:1.14}},{{scale:1.0,duration:{dur},ease:"power1.out"}},{ts});')
            elif motion == "left": js.append(f'tl.fromTo("{tgt}",{{scale:1.14,x:90}},{{scale:1.14,x:-90,duration:{dur},ease:"none"}},{ts});')
            elif motion == "right": js.append(f'tl.fromTo("{tgt}",{{scale:1.14,x:-90}},{{scale:1.14,x:90,duration:{dur},ease:"none"}},{ts});')
            elif motion == "shake":
                js.append(f'tl.fromTo("{tgt}",{{scale:1.22}},{{scale:1.08,duration:0.35,ease:"power3.out"}},{ts});')
                js.append(f'tl.to("{tgt}",{{scale:1.0,duration:{max(0.1,dur-0.35)},ease:"none"}},{ts+0.35});')
                for q, (dx, dy) in enumerate([(26,-18),(-22,14),(16,10),(-10,-8),(6,4),(0,0)]):
                    js.append(f'tl.to("{tgt}",{{x:{dx},y:{dy},duration:0.045,ease:"none"}},{ts+0.02+q*0.045:.3f});')
            # flash on every cut except the first
            if ts > 0:
                sid += 1
                els.append(f'<div id="fl{sid}" class="clip flash" data-start="{max(0,ts-0.05):.3f}" data-duration="0.3" data-track-index="2" style="z-index:300"><div class="flash-in" id="fl{sid}i"></div></div>')
                js.append(f'tl.fromTo("#fl{sid}i",{{opacity:0.55}},{{opacity:0,duration:0.25,ease:"power2.out"}},{max(0,ts-0.05):.3f});')
            ts = round(ts + dur, 3)
        # glass carousel beside the presenter (never over the face)
        if s.get("carousel"):
            sid += 1; c = f"cr{sid}"
            cards = "".join(f'<div class="card" id="{c}c{n}" data-layout-ignore><img src="assets/cards/{s["carousel"]}_{n}.jpg" alt=""><div class="shine"></div></div>' for n in range(6))
            els.append(f'<div id="{c}" class="clip carousel" data-start="{st}" data-duration="{d}" data-track-index="3" style="z-index:150" data-layout-allow-overlap data-layout-allow-occlusion><div class="ring" id="{c}r">{cards}</div></div>')
            js.append(f'tl.fromTo("#{c}r",{{opacity:0,y:160}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{st});')
            js.append(f'tl.to("#{c}r",{{opacity:0,duration:0.2,ease:"power2.in"}},{st+d-0.2:.3f});')
            for n in range(6):
                a0 = n * 60 + 30
                js.append(f'tl.fromTo("#{c}c{n}",{{"--a":{a0}}},{{"--a":{a0+70},duration:{d},ease:"none",onUpdate:carouselPose,onUpdateParams:["#{c}c{n}"]}},{st});')
        # top glass pill
        if s.get("pill"):
            txt, a, b = s["pill"]
            sid += 1; p = f"pl{sid}"
            els.append(f'<div id="{p}" class="clip pillwrap" data-start="{st+a:.3f}" data-duration="{b-a:.3f}" data-track-index="4" style="z-index:200"><div class="pill" id="{p}i">{html.escape(txt)}</div></div>')
            js.append(f'tl.fromTo("#{p}i",{{opacity:0,y:-60,scale:0.9}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},{st+a:.3f});')
            js.append(f'tl.to("#{p}i",{{opacity:0,y:-30,duration:0.2,ease:"power2.in"}},{st+b-0.2:.3f});')
        # captions
        for k, (txt, a, b, style, acc) in enumerate(s["caps"]):
            sid += 1; g = f"cp{sid}"
            col = ACC[acc]
            latin = all(ord(ch) < 128 for ch in txt)
            wstyle = style
            if style == "top": style = "slam"
            cls = f"cap {style}{' latin' if latin else ''}"
            els.append(f'<div id="{g}" class="clip capwrap {wstyle}w" data-start="{st+a:.3f}" data-duration="{b-a:.3f}" data-track-index="5" style="z-index:250"><div class="{cls}" id="{g}t" style="--c:{col}">{html.escape(txt)}</div></div>')
            if style == "slam":
                js.append(f'tl.fromTo("#{g}t",{{opacity:0,scale:2.2}},{{opacity:1,scale:1,duration:0.22,ease:"power4.in"}},{st+a:.3f});')
                js.append(f'tl.fromTo("#{g}t",{{x:-14}},{{x:0,duration:0.12,ease:"elastic.out(1,0.3)"}},{st+a+0.22:.3f});')
            elif style == "kin":
                js.append(f'tl.fromTo("#{g}t",{{opacity:0,y:80,scale:0.85,filter:"blur(12px)"}},{{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:0.22,ease:"power3.out"}},{st+a:.3f});')
            else:
                js.append(f'tl.fromTo("#{g}t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.16,ease:"power2.out"}},{st+a:.3f});')
            js.append(f'tl.to("#{g}t",{{opacity:0,duration:0.1,ease:"power2.in"}},{st+b-0.1:.3f});')
        if s.get("endcard"):
            sid += 1
            els.append(f'<div id="end{sid}" class="clip endcard" data-start="{st+1.2:.3f}" data-duration="{total-st-1.2:.3f}" data-track-index="6" style="z-index:260"><div class="end-in" id="end{sid}i"><div class="end-logo">DG TECH MACHINERY</div><div class="end-sub">PET Recycling · Injection · Blow Moulding</div></div></div>')
            js.append(f'tl.fromTo("#end{sid}i",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{st+1.2:.3f});')

    page = TEMPLATE.replace("%TOTAL%", str(total)).replace("%W%", str(W)).replace("%H%", str(H)) \
        .replace("%ELS%", "\n      ".join(els)).replace("%JS%", "\n      ".join(js))
    open(f"{ROOT}/index.html", "w").write(page)
    json.dump([{"id": s["id"], "start": st, "dur": d} for s, st, d in plan], open(f"{ROOT}/timeline.json", "w"), indent=1)
    print("total", total, "segments", [(s["id"], st, d) for s, st, d in plan])

TEMPLATE = r"""<!doctype html>
<html lang="ur">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=%W%, height=%H%" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Nastaliq"; src: url("assets/fonts/nastaliq-700.ttf"); font-weight: 700; }
      @font-face { font-family: "Anton"; src: url("assets/fonts/anton.ttf"); }
      @font-face { font-family: "MontBlack"; src: url("assets/fonts/montserrat-900.ttf"); font-weight: 900; }
      :root { --ground: #07090c; --ink: #ffffff; --gold: #ffc83d; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: %W%px; height: %H%px; overflow: hidden; background: var(--ground); }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: var(--ground); }
      .shot, .gfx { position: absolute; inset: 0; overflow: hidden; }
      .mv { position: absolute; inset: 0; }
      .mv video { width: 100%; height: 100%; object-fit: cover; display: block; }
      .gfx-in { position: absolute; inset: 0; background: radial-gradient(120% 80% at 50% 40%, #1a2430 0%, #07090c 70%); }
      .orb { position: absolute; border-radius: 50%; filter: blur(120px); opacity: .55; }
      .o1 { width: 1400px; height: 1400px; left: -300px; top: 600px; background: #ffb21e; }
      .o2 { width: 1300px; height: 1300px; right: -400px; top: 2000px; background: #1fb8ff; }
      .gfx-brand { position: absolute; left: 0; right: 0; top: 3080px; text-align: center; font-family: "MontBlack"; font-weight: 900;
        font-size: 92px; letter-spacing: .32em; color: rgba(255,255,255,.55); }
      .flash { position: absolute; inset: 0; pointer-events: none; }
      .flash-in { position: absolute; inset: 0; background: #fff; mix-blend-mode: screen; opacity: 0; }
      /* top glass pill */
      .pillwrap { position: absolute; left: 0; right: 0; top: 430px; height: 240px; display: flex; justify-content: center; }
      .pill { font-family: "Nastaliq", "MontBlack"; font-weight: 700; font-size: 74px; line-height: 1.9; color: #fff; direction: rtl;
        padding: 6px 70px 18px; border-radius: 120px; background: linear-gradient(180deg, rgba(255,255,255,.26), rgba(255,255,255,.08));
        border: 3px solid rgba(255,255,255,.45); backdrop-filter: blur(28px) saturate(160%); -webkit-backdrop-filter: blur(28px) saturate(160%);
        box-shadow: 0 30px 80px rgba(0,0,0,.35), inset 0 2px 0 rgba(255,255,255,.6); white-space: nowrap; }
      /* captions */
      .capwrap { position: absolute; left: 0; right: 0; display: flex; justify-content: center; text-align: center; overflow: visible; }
      .chinw { top: 2180px; }
      .kinw { top: 2250px; }
      .slamw { top: 1700px; }
      .topw { top: 700px; }
      .cap { font-family: "Nastaliq"; font-weight: 700; direction: rtl; color: var(--c); white-space: nowrap; overflow: visible; }
      .cap.chin { font-size: 132px; line-height: 2.0; text-shadow: 0 8px 30px rgba(0,0,0,.85), 0 0 4px rgba(0,0,0,.9); }
      .cap.kin { font-size: 190px; line-height: 2.0; text-shadow: 0 10px 40px rgba(0,0,0,.9), 0 0 6px rgba(0,0,0,.8);
        -webkit-text-stroke: 3px rgba(0,0,0,.35); }
      .cap.slam { font-size: 260px; line-height: 2.0; text-shadow: 0 16px 60px rgba(0,0,0,.9); }
      .cap.latin { font-family: "Anton"; direction: ltr; letter-spacing: .02em; line-height: 1.15; }
      .cap.slam.latin { font-size: 380px; }
      /* glass carousel: cards ride a ring around the presenter's waist, below the face */
      .carousel { position: absolute; inset: 0; pointer-events: none; perspective: 2600px; }
      .ring { position: absolute; left: 1080px; top: 2620px; width: 0; height: 0; transform-style: preserve-3d; }
      .card { position: absolute; left: -270px; top: -360px; width: 540px; height: 720px; border-radius: 46px; overflow: hidden;
        border: 4px solid rgba(255,255,255,.55); box-shadow: 0 40px 90px rgba(0,0,0,.45); background: rgba(255,255,255,.12); }
      .card img { width: 100%; height: 100%; object-fit: cover; display: block; }
      .shine { position: absolute; inset: 0; background: linear-gradient(135deg, rgba(255,255,255,.45) 0%, rgba(255,255,255,0) 38%, rgba(255,255,255,0) 70%, rgba(255,255,255,.18) 100%); }
      /* end card */
      .endcard { position: absolute; left: 0; right: 0; top: 2650px; align-items: flex-start; display: flex; justify-content: center; }
      .end-in { padding: 50px 90px; border-radius: 60px; text-align: center; background: rgba(10,12,16,.55);
        border: 3px solid rgba(255,255,255,.35); backdrop-filter: blur(30px); -webkit-backdrop-filter: blur(30px); }
      .end-logo { font-family: "MontBlack"; font-weight: 900; font-size: 120px; letter-spacing: .06em; color: var(--gold); }
      .end-sub { font-family: "MontBlack"; font-weight: 900; font-size: 60px; letter-spacing: .1em; color: #fff; margin-top: 20px; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="%TOTAL%" data-width="%W%" data-height="%H%">
      %ELS%
      <audio id="mix" class="clip" src="assets/audio/mix.wav" data-start="0" data-duration="%TOTAL%" data-track-index="0" data-volume="1"></audio>
    </div>
    <script>
      // Carousel pose from the card's --a angle: x/z on an ellipse, cards at the back hidden behind the presenter.
      function carouselPose(sel) {
        const el = document.querySelector(sel);
        const a = parseFloat(gsap.getProperty(el, "--a")) * Math.PI / 180;
        const x = Math.sin(a) * 820, z = Math.cos(a) * 520;
        const front = Math.cos(a);
        // keep the centre-front lane clear so cards never sit on the presenter
        const side = Math.abs(Math.sin(a));
        const op = front < -0.2 ? 0 : Math.min(1, side * 1.6) * (0.55 + 0.45 * Math.max(0, front));
        gsap.set(el, { x: x, z: z, rotationY: a * 180 / Math.PI * 0.55, opacity: op, scale: 0.7 + 0.3 * Math.max(0, front) });
      }
      const tl = gsap.timeline({ paused: true });
      %JS%
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""

if __name__ == "__main__":
    build()
