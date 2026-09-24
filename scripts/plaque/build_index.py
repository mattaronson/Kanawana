"""Build a person index from the p_291 plaque audit.

NOTE ON 'Section leader' (the Advance Guard boards' led_by): on the 1963 and
1964 boards this is Julien Tasse, set apart between painted arrows -- and he
was the camp's CARETAKER of thirty-odd years, not the section's senior boy.
He is therefore staff on those boards. The role is left in the JUNIOR set for
any other board that uses it, but Tasse is pinned as staff below, because a
label cannot tell you which of the two situations it is describing.

NOTE ON 'WOLF': the 2009 boards credit a "Wolf" beneath Counsellor and
Tripper. An earlier version of this script classed that as a STAFF title.
It is not: the operator identifies WOLF as a leadership PROGRAMME -- the
Rangers programme revived in 2001 and renamed Wolf later that decade -- so a "Wolf" on a trip board holds that rank, exactly as "L.I.T. Daphne
Pungartnik" and "Lit Amy D." do on other boards. Like CIT and LIT it names
both a programme and a standing within it, so it IS a designation attached
to a person -- but a trainee one. It is counted as leadership-track, never
as staff.

Conservative by design. Two names merge only if their NORMALISED forms are
identical, or if the pair appears in ALIASES -- a hand-curated list, every
entry of which was justified in the audit record. Nothing merges on
similarity alone; near-misses are reported separately for human judgement,
never folded in silently.

Initial-only entries ("Katie A-F.", "Mark C.C.") are indexed but excluded
from cross-year tracing, because an initial is not a name.
"""
import json, re, unicodedata, collections, os

ROLE_KEYS = {
 'director':'Director','directors':'Director','directress':'Directress',
 'section_director':'Section Director','coordinators':'Co-ordinator',
 'masters':'Master','capitaine':'Capitaine','counsellor':'Counsellor',
 'counsellors':'Counsellor','cit':'CIT','cits':'CIT','lit':'LIT','lits':'LIT',
 'jc':'JC','jcs':'JC','jcgs':'JC','tripper':'Tripper','trippers':'Tripper',
 'wolf':'Wolf programme','therapist':'Therapist(joke)','guest':'Guest','crew':'Maintenance',
 'staff':'Staff','swimmers':'Swimmer','recipients':'Award recipient',
 'namers':'Cabin namer','signatories':'Signatory','signed':'Signatory',
 'participants':'Participant','members':'Member','campers':'Camper',
 'rangers':'Ranger','voyageurs':'Voyageur','girls':'Camper','boys':'Camper',
 'section':'Member','led_by':'Section leader','confirmed_subset':'Staff',
 'cit_program_director':'CIT Program Director','cit_director':'CIT Director',
 'jbc':'JBC','roll':'Knight',
}
SKIP_KEYS = {'title','motto','mottos','text','inscription','inscriptions','caption',
 'marginalia','device','devices','carved_devices','epigraph','epitaph','dedication',
 'aside','footer','form','object','structure','quotation','song_list_faded','sessions',
 'session','dates','tags','lakes_mapped','origins_listed','years_down_edge','group_mottos',
 'motto_words','blessing','attached_tag','names_low_confidence','ring_tokens','readable',
 'left','right','col1','col2','col3','col4','upper','lower','house_1','house_2',
 'footer_cluster','closing','acrostic_B_A_S_I_N','others','1st','2nd','3rd','4th',
 'window_1','window_2','window_3','window_4','window_5','lower_row','wheels',
 'group_1','group_2','left_paddle','right_paddle','centre_board','adjacent_cursive_board',
 'shelf_label','special_guests_faded','1st_session','3rd_session','4th_session',
 '1st_session_JCGs','1st_session_leader','3rd_session_lit','3rd_session_tripper',
 '3rd_session_dates','1st_session_jbcs','3rd_cabin','speech_bubbles','trailing',
 'Talahassee_2nd_session','Swazi_4th_session','Talahassee_3rd_session',
 'Basin_Breezers_3rd_session','winning_team','hierarchy','counsellors_note'}
# keys that ARE name lists but whose key gives no role
GENERIC = {'left','right','col1','col2','col3','col4','upper','lower','house_1','house_2',
 'footer_cluster','1st','2nd','3rd','4th','window_1','window_2','window_3','window_4',
 'window_5','lower_row','wheels','group_1','group_2','left_paddle','right_paddle',
 'adjacent_cursive_board','special_guests_faded','1st_session','3rd_session','4th_session',
 '3rd_cabin','Talahassee_2nd_session','Swazi_4th_session','Talahassee_3rd_session',
 'Basin_Breezers_3rd_session','acrostic_B_A_S_I_N','others','readable','ring_tokens'}

GROUP_ROLE = {'Staff':'Staff','CIT':'CIT','LIT':'LIT','JC':'JC','Rangers':'Ranger',
 'Voyageurs':'Voyageur','Knights':'Knight','Maintenance':'Maintenance','Swim':'Swimmer',
 'Advance Guard':'Member','Canoe Staff':'Staff','Sailing Staff':'Staff'}

ALIASES = {  # justified in the audit record; nothing here is a guess
 # --- Staff of '79: the plaque read against the camp's own typed staff list ---
 # The 1979 Director's Report prints the season's full staff roster. Set beside
 # the staff-1979 plaque transcription it resolves twenty-odd painted names that
 # the audit had read phonetically. Every pair below is one person on one board,
 # confirmed by a second document, not a similarity guess.
 # Justin Pulfer is painted "Justin 'JT' Pulfer" on the 2008 LIT board and
 # "Justin J. Pulfer" on the 2009 JC board. shape() strips a quoted nickname but
 # keeps a middle initial, so the two shaped apart and one person became two rows
 # -- which hid a seventh member of the 2008 LIT cohort that moved up together to
 # JC in 2009 (f_2340 names seven; the index showed six). Merged on the grounds
 # this list exists for and not on similarity: same given name and surname,
 # consecutive years, and the LIT-to-JC step the other six make on the same pair
 # of boards. Found 2026-09-06 checking f_2340 against the index.
 "justin 'jt' pulfer":'justin pulfer','justin j. pulfer':'justin pulfer',
 'allan iundall':'allan gandall','allan gandall':'allan gandall',
 'ann jourdeau':'ann gourdeau','ann gourdeau':'ann gourdeau',
 'aylene tickeawin':'aylene mckeown','aylene mckeown':'aylene mckeown',
 'bob bierman':'bob bluman','bob bluman':'bob bluman',
 'carola hayrey':'carola haney','carola haney':'carola haney',
 'cheryl scoff':'cheryl scaife','cheryl scaife':'cheryl scaife','chery scaife':'cheryl scaife',
 'johanna gallir':'johanna galler','johanna galler':'johanna galler',
 'john pisrosaro':'john pierosara','john pierosara':'john pierosara',
 'josie denis':'josee denis','josee denis':'josee denis',
 'jurnette penwarn':'jeannette penwarn','jeannette penwarn':'jeannette penwarn',
 'karin reichel':'karen reichel','karen reichel':'karen reichel',
 'kevin fowler':'kevin forster','kevin forster':'kevin forster',
 'kevin mcilrath':'kevin mcgrath','kevin mcgrath':'kevin mcgrath',
 'larry lacy':'larry lacey','larry lacey':'larry lacey',
 'paul schneiderist':'paul schneidereit','paul schneidereit':'paul schneidereit',
 'pippa hobbs':'pippa hobbes','pippa hobbes':'pippa hobbes',
 'renu cosgrove':'renee cosgrove','renee cosgrove':'renee cosgrove',
 'robyn chalmers':'robyn chaloner','robyn chaloner':'robyn chaloner',
 'steve weeks':'stephen wells','stephen wells':'stephen wells',
 'therese maxim':'therese marin','therese marin':'therese marin',
 'yizhi cagalino':'isabella casalino','isabella casalino':'isabella casalino',
 'jeff lorette':'jeff surette','jeff surette':'jeff surette',
 'dave bennett':'david bennet','david bennet':'david bennet',
 'carole bell':'carol bell','carol bell':'carol bell',
 'jim pelton':'james pelton','james pelton':'james pelton',
 'julian tasse':'julien tasse',
 'matt hamerman':'matt hamerman','matthew hammerman':'matt hamerman',
 'matt wiviott':'matt wiviott','matthew wiviott':'matt wiviott','matt iviott':'matt wiviott',
 'evan frankel':'evan frankel','evan frenkel':'evan frankel',
 'tiff bollhorn':'tiff bollhorn','tiffany ballhorn':'tiff bollhorn',
 'alex bollhorn':'alex bollhorn','alex ballhorn':'alex bollhorn',
 'sarah a-frankel':'sarah addleman frankel','sarah addleman frankel':'sarah addleman frankel',
 'sarah a[ddleman]-frankel':'sarah addleman frankel',
 'nick zarins':'nick zarins','nikk zarins':'nick zarins',
 'lindsay mcdougall':'lindsay mcdougall','lindsay macdougall':'lindsay mcdougall',
 'helena longpre':'helena longpre','heléna longpré':'helena longpre',
 'scott macleod':'scott macleod','scott mcleod':'scott macleod',
 'j.m. sotiran':'jm sotiron','j.m. (jeff) sotiron':'jm sotiron',
 'sam trowbridge':'sam trowbridge',"sam 'sassim' trowbridge":'sam trowbridge',
 "sam 'saddam' trowbridge":'sam trowbridge',
 'jonathan nagles':'jonathan nagles','johnny nagles':'jonathan nagles',
 'sydney hassoun':'sydney hassoun','sydney hassan':'sydney hassoun',
 'caroline di tommaso':'caroline di tommaso','caroline di tomasso':'caroline di tommaso',
 'reiko webster':'reiko webster','rieke webster':'reiko webster',
 'razi fraticelli':'razi fraticelli','razz fraficelli':'razi fraticelli',
 'meyland g-labelle':'meyland g-labelle','myland g-l.':'meyland g-labelle',
 'nanette lloyd-hughes':'nanette lloyd-hughes','nam l-hughes':'nanette lloyd-hughes',
 'jess dobrinski':'jess dobrinski','jessica dobrinski':'jess dobrinski',
 'emily lecker':'emily lecker','em lecker':'emily lecker',
 'jonathan mee':'jon mee','jon mee':'jon mee',
 'nicolas muszynski':'nick muszynski','nick muszynski':'nick muszynski',
 'charles shulman':'charlie shulman','charlie shulman':'charlie shulman',
 'julien tasse':'julien tasse','julien tassé':'julien tasse',
 'yves tasse':'yves tasse','yves tassé':'yves tasse',
 'emily feldman':'emily feldman',"emily 'melvin' feldman":'emily feldman',
 'jeff muss':'jeff muss',"jeff 'travolta' muss":'jeff muss',
 'nancy fletcher':'nancy fletcher',"nandy 'fletch' fletcher":'nancy fletcher',
 'andrew eldridge':'andrew eldridge',"andrew 'hippo' eldridge":'andrew eldridge',
 "andrew 'hippo' elridge":'andrew eldridge',
 'louis lessard':'louis lessard','louis less[ard]':'louis lessard',
 'jen kaufman':'jennifer kaufman','jennifer kaufman':'jennifer kaufman',
 'jenny kaufman':'jennifer kaufman','jen kauf[man]':'jennifer kaufman',
 'dylan o brian':'dylan obrien','dylan o brien':'dylan obrien',
 'mike zeltzer':'michael zeitzer','micheal zeitzer':'michael zeitzer',
 'ariel mcgeary':'ariel mcgeary hall','ariel mcgeary hall':'ariel mcgeary hall',
 'sally waff':'sally watt','sally watt':'sally watt',
}

# Display name where the plaques disagree and one reading is settled. Each
# entry was resolved against a specific board during the p_291 audit, not
# chosen for looking tidier.
PREFERRED = {
 # Staff of '79, corrected against the camp's own typed roster in the 1979
 # Director's Report. The plaque readings were phonetic; these are the names.
 'allan gandall':'Allan Gandall','ann gourdeau':'Ann Gourdeau',
 'aylene mckeown':'Aylene McKeown','bob bluman':'Bob Bluman',
 'carola haney':'Carola Haney','cheryl scaife':'Cheryl Scaife',
 'johanna galler':'Johanna Galler','john pierosara':'John Pierosara',
 'josee denis':'Josee Denis','jeannette penwarn':'Jeannette Penwarn',
 'karen reichel':'Karen Reichel','kevin forster':'Kevin Forster',
 'kevin mcgrath':'Kevin McGrath','larry lacey':'Larry Lacey',
 'paul schneidereit':'Paul Schneidereit','pippa hobbes':'Pippa Hobbes',
 'renee cosgrove':'Renee Cosgrove','robyn chaloner':'Robyn Chaloner',
 'stephen wells':'Stephen Wells','therese marin':'Therese Marin',
 'isabella casalino':'Isabella Casalino','jeff surette':'Jeff Surette',
 'david bennet':'David Bennet','carol bell':'Carol Bell','james pelton':'James Pelton',
 'sally watt':'Sally Watt',                 # confirmed from the 1983 paddle in senior-boys-1987.jpg
 'matt wiviott':'Matt Wiviott',             # 'Iviott' loses the W against the paddle grain
 'reiko webster':'Reiko Webster',
 'jm sotiron':'J.M. (Jeff) Sotiron',
 'sam trowbridge':"Sam 'Saddam' Trowbridge",# confirmed from voyageurs-1998.jpg
 'ariel mcgeary hall':'Ariel McGeary Hall',
 'tiff bollhorn':'Tiff Bollhorn',
 'alex bollhorn':'Alex Bollhorn',
 'sarah addleman frankel':'Sarah Addleman Frankel',
 'helena longpre':'Helena Longpre',
 'jennifer kaufman':'Jennifer Kaufman',
 'dan shemie':'Dan Shemie',
}

def strip_nick(s):
    s = re.sub(r'"[^"]*"', ' ', s)
    s = re.sub(r"'[^']*'", ' ', s)
    s = re.sub(r'\([^)]*\)', ' ', s)
    s = re.sub(r'\[[^\]]*\]', ' ', s)
    return s

def shape(s):
    """Everything norm() does EXCEPT the alias lookup."""
    s = strip_nick(s)
    s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode()
    s = s.lower().replace('.', ' ').replace('&',' ')
    s = re.sub(r'[^a-z0-9\- ]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    # The Knights of Kanawana roll paints every entry with its title. Left in,
    # "Sir Denys Lawrence" indexes as a different person from the Denys Lawrence
    # on the Staff of '79 board -- so every knight who appears anywhere else was
    # being stored twice and their progression split in half.
    s = re.sub(r'^(sir|lady) ', '', s)
    return s

# The alias table is written the way a person writes names -- "j.m. sotiran",
# "andrew 'hippo' elridge", "julien tasse" with the accent. norm() strips
# periods, quoted nicknames and accents BEFORE it looked the name up, so any
# such key could never match: 16 of the 78 curated entries, one in five, were
# silently doing nothing, and three of the "candidate pairs" p_298 was holding
# for human judgement had ALREADY been decided by this list. Keys are therefore
# put through the same shaping as the names they are matched against.
_ALIAS = {}
for _k, _v in ALIASES.items():
    _sk = shape(_k)
    if _sk in _ALIAS and _ALIAS[_sk] != _v:
        raise SystemExit('alias collision: %r shapes to %r, wanted by both %r and %r'
                         % (_k, _sk, _ALIAS[_sk], _v))
    _ALIAS[_sk] = _v

def norm(s):
    return _ALIAS.get(shape(s), shape(s))

def is_initial_only(n):
    toks = n.split()
    if len(toks) < 2: return True
    return all(len(t.strip('-')) <= 2 for t in toks[1:])

YEAR_RE = re.compile(r'(?:19|20)\d{2}')
def year_of(row):
    for src in (row['names'].get('title',''), row['image']):
        if not isinstance(src, str): continue
        m = YEAR_RE.findall(src)
        if m: return int(m[0])
    m = re.search(r"'(\d{2})\b", str(row['names'].get('title','')))
    if m:
        y = int(m.group(1)); return 1900+y if y > 30 else 2000+y
    m = re.search(r'-(\d{2})\.jpg', row['image'])
    if m:
        y = int(m.group(1)); return 1900+y if y > 30 else 2000+y
    return None

def group_of(row):
    t = (row['names'].get('title') or row['image']).lower()
    for key, label in [('cit','CIT'),('lit','LIT'),('staff','Staff'),('ranger','Rangers'),
      ('voyageur','Voyageurs'),('advance guard','Advance Guard'),('knight','Knights'),
      ('swim','Swim'),('basin','Basin'),('swazi','Swazi'),('malibu','Malibu'),
      ('lookout','Lookout'),('chopsy','Chopsy'),('rock tent','Rock Tent'),
      ('roadhouse','Roadhouse'),('road house','Roadhouse'),('senior girl','Senior Girls'),
      ('senior boy','Senior Boys'),('jbc','JBC'),('junior','Junior'),('jc','JC'),
      ('explorer','Explorer'),('adventurer','Adventurer'),('talahassee','Talahassee'),
      ('nature trip','Nature Trip'),('kanawoodstock','Kanawoodstock'),('rounds','Rounds'),
      ('pink flam','Pink Flamingo'),('maintenance','Maintenance'),('kanoing','Canoe Staff'),
      ('sailing','Sailing Staff'),('pig pen','Pig Pen'),('all-kamp','All-Kamp'),
      ('all kamp','All-Kamp')]:
        if key in t: return label
    return None

rows = [json.loads(l) for l in open('kb/plaque-audit/audit.jsonl')]
index = collections.defaultdict(list)
raw_forms = collections.defaultdict(set)

for r in rows:
    yr, grp = year_of(r), group_of(r)
    for key, val in r['names'].items():
        if key in SKIP_KEYS and key not in GENERIC: continue
        role = ROLE_KEYS.get(key)
        if role is None:
            if key not in GENERIC: continue
            # A generic column key ("col1", "left", "1st_session") says nothing
            # about the role -- but the BOARD does. Names in the columns of a
            # Staff plaque are staff; names in the columns of a CIT plaque are
            # CITs. Reading the key and ignoring the board silently demoted
            # every name on the 1979, 1990 and 2002 staff plaques to "Member".
            role = GROUP_ROLE.get(grp, 'Member')
        items = val if isinstance(val, list) else [val]
        for it in items:
            if isinstance(it, list) and len(it) == 2 and isinstance(it[1], int):
                nm, y2 = it[0], it[1]           # Knights roll: [name, year]
            elif isinstance(it, str):
                nm, y2 = it, yr
            else:
                continue
            n = norm(nm)
            if not n or len(n) < 3: continue
            raw_forms[n].add(nm.strip())
            r2 = role
            # Julien Tasse was the camp's CARETAKER for thirty-odd years and died
            # c.1992-95. Every board he is on -- Advance Guard 1963, 1964 and 1986,
            # Staff 1990 -- catches him at work, not progressing through the ranks,
            # so he is pinned to staff throughout. Without this he reads as a
            # 1986-camper-to-1990-staff progression, which is exactly backwards.
            if n == 'julien tasse':
                r2 = 'Staff'
            index[n].append({'year': y2, 'group': grp, 'role': r2,
                             'image': r['image'], 'as_written': nm.strip()})

os.makedirs('kb/plaque-audit', exist_ok=True)
out = {}
for n, apps in index.items():
    yrs = sorted({a['year'] for a in apps if a['year']})
    disp = PREFERRED.get(n) or sorted(raw_forms[n], key=lambda x:(-len(x), x))[0]
    out[n] = {'display': disp, 'forms': sorted(raw_forms[n], key=lambda x:(-len(x), x)), 'appearances': apps,
              'years': yrs, 'span': (yrs[-1]-yrs[0]) if len(yrs) > 1 else 0,
              'initial_only': is_initial_only(n)}
json.dump(out, open('kb/plaque-audit/person-index.json','w'), indent=1, ensure_ascii=False)

multi = {n: d for n, d in out.items() if len(d['years']) > 1 and not d['initial_only']}
print('distinct normalised names :', len(out))
print('name-appearances          :', sum(len(d['appearances']) for d in out.values()))
print('traced across >1 YEAR     :', len(multi))
print('spanning >=5 years        :', sum(1 for d in multi.values() if d['span'] >= 5))
print('spanning >=10 years       :', sum(1 for d in multi.values() if d['span'] >= 10))
