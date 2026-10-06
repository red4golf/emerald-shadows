# Emerald Shadows — 2:00 teaser: on-screen transcript

Everything below is text the real game printed during a scripted playthrough (the winning path, run through the actual game code in a terminal). Commands are shown as typed. Long passages are **excerpted** for running time — paragraphs are cut, never reworded, and the game's own history asides are left out. Timecodes are when each command is typed.

## Title  ·  0:00

```
[EMERALD SHADOWS — block-letter title logo]

Seattle, Washington. October 1947. The war is two years over and the city hasn't
slept. Neither have you.
```

## Bullpen and evidence room  ·  0:10.0

```
The bullpen never really sleeps. Typewriters clatter on the night shift,
somebody's percolator is burning the bottom of the pot, and the fluorescent
light above your desk flickers like it can't make up its mind. Your name is on
the door: J. DIAMOND, DETECTIVE. The files on your desk are neat. Everything
else about this case is not. Through the window, the top of Smith Tower catches
the last of the evening light.

Exits: outside, upstairs

You can see: badge, case_file, notebook
```

**0:14.8**  `> upstairs`

```
The evidence room smells of old paper, gun oil, and bad decisions. Steel shelves
run floor to ceiling, each item tagged and catalogued by someone who believed in
order. A work table in the center is scarred from years of use. Whatever went
missing in '46 left gaps on those shelves that nobody talks about. You notice
the gaps immediately.

Exits: downstairs

You can see: cipher_wheel, radio_manual, photo
```

## The photograph  ·  0:20.3

**0:20.3**  `> examine photo`

```
Two men in overcoats unloading crates from a panel truck backed up to a
warehouse door. Night shot, grainy — whoever took this was working fast and
didn't have good light. The shorter man's face is turned away. The taller one is
half-visible, and something about the set of his shoulders is familiar in the
way that makes your jaw tighten. You've seen this man before. You'll know him
when you find him.

Behind the truck, half out of frame, sits a dark sedan. Its rear plate catches
just enough of the flash to read the first two figures and no more:

   WA-44??

Washington registration. Two figures out of four. Somebody in this city stood
close enough to that car to have seen the rest of it.
```

## The cipher wheel  ·  0:28.6

**0:28.6**  `> turn wheel to c`

```
Setting C:

   UFXXBTWI FSLJQX FIRNYX GJFWJW FY UNJW XJAJS FKYJW RNISNLMY...

Still noise. Turn it again.
```

**0:31.7**  `> turn wheel to q`

```
Setting Q:

   GRJJNFIU REXVCJ RUDZKJ SVRIVI RK GZVI JVMVE RWKVI DZUEZXYK...

Still noise. Turn it again.
```

**0:34.2**  `> turn wheel to h`

```
You align the outer A with the inner H. The rings settle into a detent somebody
wore smooth a long time ago.

   PASSWORD ANGELS ADMITS BEARER AT PIER SEVEN AFTER MIDNIGHT ASK ONLY FOR THE
   HARBORMASTER BURN THIS

Twenty-six settings and only one of them is English. This isn't evidence of the
```

## The witnesses  ·  0:41.1

**0:41.1**  `> ask harold about sedan`

```
Harold has the brass gate half-open and his cap squared. Pacific, you'd guess —
he has the way of standing that men brought back from it.

'Detective. Floor?' A beat. 'Or not a floor.'
'Blue sedan. Pulls up at the Yesler door, never the front.' Harold looks out
through the revolving door at the wet street, remembering properly.

'Third figure on the plate was a seven. I'd swear to that in a courtroom. The
first two I never had the angle on, and the last one the frame ate.'
[You write it in the notebook.]
```

**0:47.7**  `> ask roy about frequency`

```
He is quiet for a full block. Then he takes one hand off the controller, digs in
his coat, and holds out a folded scrap of paper without looking at you.

'They talk on the radio. Nightly, two in the morning. I wrote it down off a set
in the barn where they park the trucks.'

'Don't use the telephone. Don't come and find me again. I've got eight months to
a pension and a wife who thinks I drive a streetcar.'
```

**0:52.8**  `> examine informant_note`

```
The handwriting is cramped and hurried, like a man who knew he wasn't safe
standing still long enough to write slowly. It has been in a coat pocket in
Seattle in October, and the rain has had the worst of it:

   'Emergency frequency 415.? MHz — they broadcast shipment times
    nightly at 2 AM. Don't use the phone. —R.'

The last digit is a blue smear. Ten numbers it could be, and a man risked his
pension to write down all four. You'll have to find the last one yourself, on
the dial, in the dark. That's the job.
```

## The plate  ·  0:59.9

**0:59.9**  `> solve`

```
You put your back against the pergola and open the notebook to the page where
you've been keeping the sedan.

A blue sedan, seen near three separate scenes by three people who each caught a
different piece of it. Nobody got the whole plate. Between them, they might
have.

What you have, and who gave it to you:
  - the surveillance photograph — first two figures, the rest lost to grain
  - Harold at the Smith Tower — 'third one was a seven, I'd swear to it'
  - Ches at the Anchor — 'ended in a one. I remember because it didn't'
```

## The casebook  ·  1:06.2

**1:06.2**  `> case`

```
DIAMOND'S CASEBOOK
==================
Act 1 — Legwork        Case progress: 170 points

THE SEDAN
---------
  Plate so far: WA-447?

OPEN
----
  - You don't have a name for the company behind it.
  - A blue sedan keeps turning up. Nobody saw the whole plate.
  - The cargo goes somewhere between the dock and the boat. Where?
  - You've never actually watched the docks work at night.
  - Something is going on under Pioneer Square and you haven't been down.
```

## The Anchor  ·  1:12.8

**1:12.8**  `> use badge`

```
You set the badge on the bar. Ches looks at it for a long moment — not afraid of
it, just reading it — then sets down the glass he's been wiping.

'The ship in the roads.' His voice is low enough that the men in the booth can't
hear. 'Sitting out there three nights running. Waiting. A launch went out from
Pier 7 last night, around three. Came back light. Whatever it was going for, it
didn't get it yet.'

He picks up the badge with two fingers and slides it back across the bar.

'I didn't say that. You didn't hear it. Understood?'
```

## The radio  ·  1:19.4

**1:19.4**  `> tune 415.3`

```
415.3 — a voice surfaces and drowns before it's a word. Close enough to know
it's real. Not close enough to use.
```

**1:22.2**  `> tune 415.6`

```
415.6.

The static parts like a curtain and there are men in the room with you.

'—second pallet's short. Tell him the count was short.'
'He knows what the count was.'
'Then tell him the Harbormaster wants it moved tonight, not Friday. Pier seven.
Same as always.'

A third voice says something you don't catch, and somebody laughs, and then it's
just carrier tone and the rain on the window.
```

## The tunnels  ·  1:28.9

**1:28.9**  `> underground`

```
          .-===========-.
         //   _______   \\
[EMERALD SHADOWS — block-letter title logo]
 It is pitch dark. Something moves in the dark nearby — patient, unhurried.
It has done this before. Use your flashlight, Diamond.
It is pitch dark. You are likely to be eaten by a grue.
```

**1:34.1**  `> use flashlight`

```
You kill the light and stand still.

It comes again — metal on metal, somewhere ahead where the tunnel bends. Not
settling. Not water. Someone down here is tapping on a pipe, patiently, the same
short phrase over and over, the way you signal when you can't afford to be heard
saying it.

   .-- ..--- ..---
```

**1:38.9**  `> tap W22`

```
You tap it back against the brick — .-- ..--- ..--- — and the pipe goes quiet,
and then answers once. Acknowledged.
```

## Pier 7  ·  1:42.8

**1:42.8**  `> south`

```
Pier 7 at twenty past eleven, and the rain has stopped, which is worse. Without
it the waterfront is very quiet and you can hear everything: the hull working
against the pilings, a winch somewhere aft, men talking low in the shed at the
end of the pier where a light is burning that has no business burning at this
hour.

The ship that has been sitting out in the roads three nights is alongside now.
Crates are coming off her, and the stencils have been painted over, badly.

A man is standing at the shed door with a clipboard, waiting for somebody who
knows the word.

This is the end of it. When you're ready: 'arrest'.
```

## Closing card  ·  1:50.5

```
[EMERALD SHADOWS — block-letter title logo]

  A NOIR DETECTIVE TEXT ADVENTURE  -  SEATTLE, 1947

  Download for Windows:
  github.com/red4golf/emerald-shadows/releases
```
