import pexpect, json, os, sys, tempfile, re
COLS, ROWS = 80, 25
ANSI=re.compile(r'\x1b\[[0-9;?]*[A-Za-z]')
STOPS={"pioneer_square":"Pioneer Square Stop","waterfront":"Waterfront Stop","smith_tower":"Smith Tower Stop","pike_place":"Pike Place Stop"}
PLAN = ["take all","upstairs","take all","examine photo","examine radio_manual","turn wheel to c","turn wheel to q","turn wheel to h",
"combine badge with photo","downstairs","outside","west","take all","examine membership_register",
"ask porter about voss","back","take all","hall","east","north","ask harold about sedan","trolley",
"ask roy about case","ask roy about supplies","ask roy about frequency","take informant_note",
"examine informant_note","case","RIDE:pioneer_square","take all","examine bulletin_notice","north","south","trolley",
"RIDE:waterfront","tavern","use badge","ask ches about supplies","ask ches about harbormaster",
"ask ches about sullivan","ask ches about sedan","outside","trolley","RIDE:pioneer_square","solve",
"north","east","enter","take all","office","tune 415.3","tune 415.6","door","outside","south","shack",
"take all","outside","underground","use flashlight","listen","tap W22","up","south"]
def main(out):
    work = tempfile.mkdtemp()
    env = dict(os.environ, TERM="xterm-256color", PYTHONPATH="/home/user/emerald-shadows",
               PYTHONIOENCODING="utf-8", COLUMNS=str(COLS), LINES=str(ROWS)); env.pop("NO_COLOR",None)
    c = pexpect.spawn(sys.executable, ["-m","emerald_shadows"], cwd=work, env=env, dimensions=(ROWS,COLS), encoding="utf-8", timeout=30)
    segs=[]
    c.expect("Press Enter to begin"); segs.append({"cmd":None,"out":c.before+c.after})
    c.sendline(""); c.expect(r"\n> "); segs.append({"cmd":"","out":c.before+"\n> "})
    def step(cmd):
        c.sendline(cmd)
        i=c.expect([r"\n> ","What have you got"])
        o=c.before; segs.append({"cmd":cmd,"out":o}); 
        if i==1:
            c.sendline("WA-4471"); c.expect(r"\n> "); segs.append({"cmd":"WA-4471","out":c.before})
        return o
    for cmd in PLAN:
        if cmd.startswith("RIDE:"):
            want=STOPS[cmd[5:]]
            for _ in range(10):
                o=step("next")
                if want in ANSI.sub("",o): break
            step("off")
        else: step(cmd)
    json.dump(segs, open(out,"w")); print(len(segs))
main("run_full2.json")
