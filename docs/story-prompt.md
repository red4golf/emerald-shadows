# Emerald Shadows — Story Adaptation Prompt

A ready-to-use prompt for turning the game into a piece of prose fiction. Paste
everything below the line into Cowork.

**Before you paste:** if you can, attach or point Cowork at this repository
(`red4golf/emerald-shadows`). The prompt works standalone — every fact it needs
is in the canon sheet — but the game's own prose is the best thing about it, and
a writer who can read the source files will produce something much closer to the
voice you already have. The files worth reading are named in the prompt.

---

## THE TASK

Write a complete noir detective novella, **8,000–12,000 words**, adapted from a
text adventure game called *Emerald Shadows*, set in Seattle in October 1947.

This is an adaptation, not a transcript. The game gives you the case, the cast,
the city, and the voice. Your job is to turn a thing that was *played* into a
thing that is *read* — which means interiority, consequence, and scenes that
breathe, not a walkthrough with adjectives.

## SOURCE MATERIAL

If you have access to the repository, read these first. They carry the voice:

| File | What's in it |
|---|---|
| `emerald_shadows/config_locations.py` | Every location description, plus a historical note per location. The Seattle history is real and load-bearing. |
| `emerald_shadows/config_dialogue.py` | Every witness, in their own words. This is your dialogue bible. |
| `emerald_shadows/item_manager.py` | Every piece of evidence, described in close-up. |
| `emerald_shadows/game_manager.py` | The act openings and the closing expense-account memo. |
| `emerald_shadows/puzzles/` | The four investigative set pieces. |

Treat the game's prose as raw material you may quote, compress, or rewrite —
but never contradict.

## THE CANON — do not change any of this

**The detective.** Johnny Diamond, Detective, Seattle PD. Badge No. 7714. His
name is on the door: J. DIAMOND, DETECTIVE. Gold-toned shield, dented on one
corner from a disagreement in '44 that he came out of better than the other
party. He is not a private eye — he is a working police detective, which matters:
his problem is that the rot is *inside the building*.

**The crime.** Army medical supplies — morphine sulfate, penicillin, whole blood
plasma — that were supposed to be destroyed under the 1946 demobilization orders.
Not destroyed. Redirected. They were meant for veterans' hospitals. They are
being sold instead.

**The front.** Northwest Maritime Imports. A shell company with the same
registered agent as four others. All previously investigated. None prosecuted.

**The hub.** Warehouse 22, down past the grain terminal. Cargo goes in, comes out
with a different bill of lading, and is legal by the time it's on a boat. That's
the whole trick. There is no clever part.

**The people:**

- **Sullivan, E.D.** — "the Harbormaster." Runs the water. Nobody has met him;
  everybody has been paid by him. Comes into the Anchor twice a month, drinks one
  thing slowly, pays in bills that have never been folded. He is *polite*. He asks
  after your family. That's worse.
- **Captain Harlan Voss** — "Voss, H.R.", Port Authority liaison to the police
  department. Eagles Third Chapter No. 1144, member number 1144. Chairs the
  Thursday room. Rides the Smith Tower elevator to the 35th floor — the Chinese
  Room — to meet a man who doesn't sign the book, and takes his lodge pin off in
  the elevator every time, before the doors open. He signs the paper. He is not
  the Harbormaster; he is the man who signs for him.
- **Walt Mathers** — Badge 447, Third District. Came up through the academy with
  Diamond in '39. Diamond stood up at his wedding. Waved three trucks through a
  gate on Tuesdays and Fridays after midnight. His wife thinks the money is from
  her father. Her father has been dead two years. **He is the emotional center of
  this story. He is not a villain — he is a weak man who did it once and then
  found there was no version of the second time where he was a man who did it
  once.**
- **Roy Hendricks** — motorman on the waterfront trolley line, nineteen years.
  Signs himself only "R." His brother came back from Anzio and waited eleven weeks
  in a bed in Bremerton for morphine the Army said it had already destroyed. Roy
  copied a radio frequency off a set in the barn where they park the trucks and
  handed it to a stranger. He has eight months to a pension and a wife who thinks
  he drives a streetcar. He says: *"I'm not being brave. I'm being angry, and it
  took me until now to tell the difference."*
- **Ches** — barman at the Anchor Tavern. Wipes a glass that's been dry ten
  minutes when he's deciding about somebody. Hears what comes in the door and
  nothing that doesn't.
- **Harold** — Smith Tower elevator operator. Pacific war veteran. Sees
  everything, says nothing, and has built a whole life on people forgetting the
  operator is standing there.
- **The night porter** — Eagles hall. A grey man in a grey cardigan who
  materialises from a side corridor without any of the floorboards mentioning it.
  "Members only after nine, sir."

**The hard details — get these exactly right:**

- The coded memo decodes to: **PASSWORD ANGELS ADMITS BEARER AT PIER SEVEN AFTER
  MIDNIGHT ASK ONLY FOR THE HARBORMASTER BURN THIS**
- The radio frequency is **415.6 MHz**. They broadcast nightly at **2 AM**.
- The blue sedan's plate is **WA-4471**, registered to the shell company.
- The tapped signal in the tunnels reads **W22** — in Morse, `.-- ..--- ..---`
- The lodge is **Eagles Third Chapter No. 1144**; Voss's member number is 1144.
- The manifest: lot 44-F, 1,500 units, declared weight 3,200 lbs — when 1,500
  units of packaged morphine and penicillin would weigh about 850. There is a
  second load underneath the first.
- The Eagles minutes: March 1946, a "civic improvement partnership" with Northwest
  Maritime Imports, moved by Voss, seconded by a name that's been whited out,
  carried unanimously. Quarterly payments into a fund called "waterfront
  development." Voss's signature is full and clear, no ambiguity.

**The ending — this is fixed:**

Sullivan is taken at **Pier 7 at twenty past three in the morning**, with six of
his crew and two tons of stolen Army medical supplies. Northwest Maritime Imports
dissolves before the ink dries on the warrant. Voss resigns his commission before
the arraignment; the department accepts it without comment; the Eagles chapter
votes to expunge his membership three days later, and the minutes of that vote
are not available for general circulation. Mathers submits his papers the morning
of the arrest and beats Diamond to the paperwork by two hours — last anyone
heard, he moved to Spokane. Roy Hendricks collects his pension the following
spring and moves to Olympia; Diamond never learns his last name until it's over.
The P-I runs PORT AUTHORITY CAPTAIN RESIGNS below the fold. These things always
do.

This is a **bittersweet win**, not a triumph. Diamond closes the case and it
costs him a friend, and the city does not notice. Do not give it a happier
ending, and do not give it a cynical one where nothing changes — the arrest is
real and it matters.

## STRUCTURE — three acts, following the game

**Act One — Legwork.** Diamond works the case and nobody much minds. The bullpen,
the evidence room, the rain on Second Avenue. He assembles the shape of the thing
from paper and from people who each hold one piece. Ends when he breaks the
cipher and puts a name to the company.

**Act Two — Heat.** He decoded something in a locked room at eleven at night and
by morning the city knows. The desk sergeant doesn't meet his eye. There's a car
at the end of Third that was there when he went in and is there when he comes
out, and the man in it is reading a newspaper in the rain, which nobody does.
From here everything he learns costs somebody something. **Mathers is waiting on
the edge of his desk with his hat in his hands.** This confrontation is the peak
of the story — write it as such.

**Act Three — Pier Seven.** The ship that has been sitting out in the roads three
nights is alongside. Crates coming off her with the stencils painted over, badly.
A man at the shed door with a clipboard, waiting for somebody who knows the word.
Diamond has the password, the pier, and the hour. He goes down there and finishes
it.

## THE FOUR SET PIECES — put all of these on the page as scenes

These are the game's investigative centerpieces. Dramatize them; don't summarize.
Each one should be a scene the reader watches happen.

1. **The cipher wheel**, at the scarred work table in the evidence room. Two rings
   of letters, one inside the other. He turns it through all twenty-six settings,
   watching the memo's first word change: `WHZZDVYK`, `VGYYCUXJ`, `UFXXBTWI` …
   twenty-five strings of nonsense, and then at setting H the word **PASSWORD**
   falls out of the noise. He isn't guessing a key. He's looking for a word he
   expects to see. This is the moment the case turns.

2. **The radio sweep**, in the warehouse office. The informant's note has been in
   a wet coat pocket and the last digit is a blue smear: *415.? MHz*. Ten numbers
   it could be. He works the dial across the band, and the static thins, and a
   voice surfaces and drowns before it's a word, and then at 415.6 the static
   parts like a curtain and there are men in the room with him: *"—second pallet's
   short. Tell him the count was short." "He knows what the count was." "Then tell
   him the Harbormaster wants it moved tonight, not Friday. Pier seven. Same as
   always."*

3. **The tapping in the tunnels**, beneath Pioneer Square. Pitch dark, brick and
   timber and old iron, water in the mortar. Metal on metal somewhere ahead where
   the tunnel bends — the same short phrase over and over, the way you signal when
   you can't afford to be heard saying it. He decodes it by hand against the code
   chart in the back of his radio manual: W-22. Then he taps it back, and the pipe
   goes quiet, and then answers once.

4. **The plate, assembled from three people.** Nobody saw the whole thing. The
   surveillance photograph gives the first two figures and loses the rest to
   grain. Harold saw the third — "a seven, I'd swear to it in a courtroom." Ches
   saw the last — "ended in a one. I remember because it didn't; the frame's bent
   and it reads like a seven until you're close." WA-4471. This is the scene that
   shows what detective work actually is: not deduction, but going and asking, and
   being the kind of man people will tell things to.

## VOICE

**First person, past tense, Diamond narrating.** (The game is second person
present — "You are standing at the beginning of a long investigation" — which is
right for play and wrong for prose. Convert it.)

The register is 1940s radio drama by way of Chandler: the game is explicitly a
tribute to *Yours Truly, Johnny Dollar* and *Richard Diamond, Private Detective*.
Diamond even listens to Richard Diamond on the radio at the end and finds it
comforting that the man is having a worse night.

What that means in practice:

- **Dry, not hard-boiled parody.** Understatement over simile. The game's own
  best lines work by refusing to escalate: *"He's not frightening in the way you'd
  want him to be. He's polite. He asks after your family. That's worse."*
- **Concrete over atmospheric.** The rain "comes down the way it always does in
  October in Seattle — not hard, just permanent, like it intends to stay." That's
  the level. One good specific beats three moody abstractions.
- **Let the detail carry the feeling.** Mathers turning his hat around once. The
  porter folding his hands. Roy taking one hand off the controller to pass the
  note and putting it straight back.
- **Diamond is tired and decent and stubborn.** Not a drunk, not a wisecracker,
  not tortured. He kept the case quiet for three weeks and then stopped being
  quiet. He knows closing it will cost somebody a badge, and he already decided.
- **The expense-account framing is the story's signature.** The game closes on a
  memo that reckons the case in cab fare, shoe leather, a nickel newspaper, and
  six hours of sleep not taken — total, four dollars and twenty cents. Use this.
  Either frame the whole novella as the filed report, or land on it at the end.

## THE CITY — real history, used properly

Seattle in October 1947 is a character, and the history in the game is real. Work
these in where they earn their place; don't lecture.

- Before the Great Fire of 1889 the downtown blocks sat twenty feet lower. The
  city rebuilt upward and buried its mistakes below street level. **In Seattle the
  past is not behind you, it is underneath you** — and the smuggling literally
  runs through those buried streets.
- Smith Tower, 1914, forty-two stories of white terracotta, still the tallest
  building west of the Mississippi. Italian marble lobby, brass elevator gates.
  The Chinese Room on the 35th floor, given by the Empress of China, with a
  wishing well at its center — sailors climbed up to make wishes during the war,
  and most of those wishes didn't come back.
- Yesler Way is the original Skid Road: Henry Yesler skidded logs down it to his
  1852 sawmill, and the term traveled east with the men who worked these docks and
  came to mean something darker.
- Ivar Haglund opened his fish bar at Pier 54 in 1938. The Kalakala runs to
  Bremerton. Half of Bremerton's naval shipyard workers ride the tram past that
  stop every morning.
- The Fraternal Order of Eagles was founded in Seattle in 1898 by six theater
  owners, and by 1947 it is one of the most politically connected fraternal
  organizations in the country. **In a city where the port authority, the police
  department, and organized labor all drank from the same well, the Eagles
  provided the cup.**
- The ILWU has held the waterfront since the 1934 strike. The men who work these
  docks know every crate that moves, and know better than to talk about it.
- The department's reputation took a beating during Prohibition and never
  recovered. Half the city knows which sergeant you pay to look the other way.
  Three evidence packages vanished from the evidence room in spring 1946; the
  official report called it a clerical error.

## CONSTRAINTS

- **October 1947. No anachronisms.** No Korean War, no television, no zip codes,
  no interstates, no jet aircraft. The Defense Department is still becoming the
  Defense Department. Check any technology, slang, or brand before you use it.
- **Don't invent a love interest.** There isn't one and the story doesn't want one.
- **Don't make Mathers irredeemable, and don't let him off.** Both would be
  cheaper than what's actually there.
- **Don't put the Harbormaster on the page early.** Sullivan works because he's a
  rumor for most of the book. Hold him.
- **Keep the women and the working people of the city present and real** — the
  night-shift typists in the bullpen, the fishmongers hauling up the Market hill,
  Mathers's wife who thinks the money came from her father. They are not scenery.
- **One judgment call is yours:** the game has a Zork tribute in the tunnels — go
  in without a light and you are eaten by a grue. It's a deliberate wink at the
  player and it is *not* literal canon. Render the darkness under Pioneer Square
  as genuine dread — something patient and unhurried that has done this before —
  but don't put a monster in a realist crime novella. If you want the nod, bury it
  as an image, not an event.

## OUTPUT

- Markdown. A title, then three act headings, with scene breaks inside them.
- 8,000–12,000 words. Write the whole thing — do not stop and ask whether to
  continue, and do not deliver an outline instead of prose.
- Open on Diamond in the bullpen with the case file in front of him and the rain
  starting, and close on the filed report.
- Then add a short note listing anything you invented to bridge a gap (a minor
  character, a connecting scene, a line of dialogue), so it can be checked against
  the game.
