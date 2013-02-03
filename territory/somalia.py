from math import sqrt
import svgwrite

somalia = [
   (10,30),
   (10,120),
   (30,150),
   (50,150),
   (70,170),
   (100,170),
   (180,250),
   (150,250),
   (100,270),
   (80,280),
   (60,290),
   (40,310),
   (60,340),
   (90,320),
   (120,330),
   (140,330),
   (150,340),
   (190,340),
   (210,350),
   (240,350),
   (250,360),
   (270,360),
   (270,320),
   (250,280),
   (240,260),
   (220,240),
   (180,140),
   (110,90),
   (50,50),
   (20,10)
]

territories = [
    #Awdal
    {
        'code':'A1',
        'name':'Borama',
        'pts':[(40,310),(60,340),(70,333),(70,310),(80,310),(80,280),(60,290)],
        'connectsto':['A2','B1'],
        'special': None,
        'center': (55,315),
    },
    {
        'code':'A2',
        'name':'Berbera',
        'pts':[(70,333),(90,320),(120,330),(120,310),(100,310),(80,310),(70,310)],
        'connectsto':['A1','B1','B2','C1'],
        'special': None,
        'center': (90,312),
        },
    #Togdheer
    {
        'code':'B1',
        'name':'Udweyne',
        'pts':[(80,280),(80,310),(100,310),(100,300),(120,280),(110,266),(100,270)],
        'connectsto':['A1','A2','B2','B3','P1'],
        'special': None,
        'center': (90,285),
        },
    {
        'code':'B2',
        'name':'Burco',
        'pts':[(100,310),(100,300),(120,280),(150,280),(150,290),(120,310)],
        'connectsto':['A2','B1','B3','C1','E1'],
        'special': None,
        'center': (120,290),
        },
    {
        'code':'B3',
        'name':'Bohotle',
        'pts':[(110,266),(120,280),(150,280),(160,270),(160,250),(150,250),(140,254)],
        'connectsto':['B1','B2','E1','E2','P3','P1'],
        'special': None,
        'center': (135,265),
        },
    #Sanaag
    {
        'code':'C1',
        'name':'Xiis',
        'pts':[(120,330),(140,330),(150,340),(150,320),(160,290),(150,290),(120,310)],
        'connectsto':['A2','B2','E1','C2','C3'],
        'special': None,
        'center': (130,315),
        },
    {
        'code':'C2',
        'name':'Erigavo',
        'pts':[(150,340),(190,340),(210,350),(210,320),(150,320)],
        'connectsto':['C1','C3','D1'],
        'special': None,
        'center': (170,330),
        },
    {
        'code':'C3',
        'name':'Xin Galool',
        'pts':[(150,320),(210,320),(210,300),(210,290),(190,290),(170,290),(160,290)],
        'connectsto':['C1','C2','D1','D3','E3','E2','E1'],
        'special': None,
        'center': (175,305),
        },
    # Bari
    {
        'code':'D1',
        'name':'Busaso',
        'pts':[(210,350),(240,350),(240,330),(270,320),(250,280),(240,300),(210,300),(210,320)],
        'connectsto':['C2','C3','D2','D3'],
        'special': None,
        'center': (220,320),
        },
    {
        'code':'D2',
        'name':'Calula',
        'pts':[(240,350),(250,360),(270,360),(270,320),(240,330)],
        'connectsto':['D1'],
        'special': None,
        'center': (250,340),
        },
    {
        'code':'D3',
        'name':'Dudo',
        'pts':[(210,300),(240,300),(250,280),(240,260),(210,280),(210,290)],
        'connectsto':['C3','D1','E3','E4'],
        'special': None,
        'center': (220,285),
        },
    #Nugaal
     {
        'code':'E1',
        'name':'Baarka',
        'pts':[(150,290),(160,290),(170,290),(170,280),(160,270),(150,280)],
        'connectsto':['C1','C3','E2','B3','B2'],
        'special': None,
        'center': (157,280),
        },
    {
        'code':'E2',
        'name':'Lascanood',
        'pts':[(170,290),(190,290),(190,250),(180,250),(160,250),(160,270),(170,280)],
        'connectsto':['B3','E1','C3','E3','F1','P3'],
        'special': None,
        'center': (170,270),
        },
    {
        'code':'E3',
        'name':'Gaaroowe',
        'pts':[(190,290),(210,290),(210,280),(200,250),(195,250),(190,250)],
        'connectsto':['C3','D3','E2','E4','F2','F1'],
        'special': None,
        'center': (195,270),
        },
    {
        'code':'E4',
        'name':'Eyl',
        'pts':[(210,280),(240,260),(220,240),(200,250)],
        'connectsto':['E3','D3','F2'],
        'special': None,
        'center': (215,255),
        },
    #Mudug
    {
        'code':'F1',
        'name':'Galcaio',
        'pts':[(180,250),(190,250),(195,250),(195,210),(160,210),(160,200),(130,200),(140,210)],
        'connectsto':['E2','E3','F2','F3','G1','P2','P3'],
        'special': None,
        'center': (170,220),
        },
    {
        'code':'F2',
        'name':'Xamure',
        'pts':[(195,250),(200,250),(220,240),(208,210),(195,210)],
        'connectsto':['E3','E4','F1','F3'],
        'special': None,
        'center': (200,230),
        },
    {
        'code':'F3',
        'name':'Mirsaale',
        'pts':[(160,210),(195,210),(208,210),(200,190),(170,190),(160,190),(160,200)],
        'connectsto':['F1','F2','F4','G1'],
        'special': None,
        'center': (180,200),
        },
    {
        'code':'F4',
        'name':'Hobyo',
        'pts':[(170,190),(200,190),(184,150),(170,150),(170,180)],
        'connectsto':['F3','G1','G2','G3'],
        'special': None,
        'center': (180,170),
        },
    #Galguduud
    {
        'code':'G1',
        'name':'Dusa Marreb',
        'pts':[(130,200),(160,200),(160,190),(170,190),(170,180),(130,180),(130,160),(125,160),(120,160),(120,190)],
        'connectsto':['P2','F1','F3','F4','G2','H2','H1'],
        'special': None,
        'center': (130,190),
        },
    {
        'code':'G2',
        'name':'Ceel Buur',
        'pts':[(130,180),(170,180),(170,150),(130,150),(125,150),(125,160),(130,160)],
        'connectsto':['G1','F4','G3','H3','H2'],
        'special': None,
        'center': (145,160),
        },
    {
        'code':'G3',
        'name':'Celdheere',
        'pts':[(130,150),(170,150),(184,150),(180,140),(166,130),(130,140)],
        'connectsto':['G2','F4','I1','H3'],
        'special': None,
        'center': (150,140),
        },
    # Hiraan
    {
        'code':'H1',
        'name':'Beledweyne',
        'pts':[(100,170),(120,190),(120,160),(110,160),(110,150),(100,150),(90,150),(90,170)],
        'connectsto':['P2','G1','H2','H3','J2'],
        'special': None,
        'center': (105,165),
        },
    {
        'code':'H2',
        'name':'Muqakoori',
        'pts':[(110,160),(120,160),(125,160),(125,150),(110,150)],
        'connectsto':['H1','G1','G2','H3'],
        'special': None,
        'center': (114,152),
        },
    {
        'code':'H3',
        'name':'Bulobarde',
        'pts':[(100,150),(110,150),(125,150),(130,150),(130,140),(120,130),(120,120),(110,120),(100,120),(100,130)],
        'connectsto':['H1','H2','I1','I2','G2','G3','J2','K2','L3'],
        'special': None,
        'center': (105,130),
        },
    #Middle Shabele
    {
        'code':'I1',
        'name':'Cadale',
        'pts':[(130,140),(166,130),(138,110),(120,120),(120,130)],
        'connectsto':['H3','G3','I2'],
        'special': None,
        'center': (135,120),
        },
    {
        'code':'I2',
        'name':'Jawhar',
        'pts':[(110,120),(120,120),(138,110),(110,90)],
        'connectsto':['L3','H3','I1'],
        'special': None,
        'center': (115,108),
        },
    # Bakool
    {
        'code':'J1',
        'name':'Xuddur',
        'pts':[(50,150),(70,170),(80,150),(80,130),(60,130),(60,140)],
        'connectsto':['M2','K2','J2'],
        'special': None,
        'center': (65,140),
        },
    {
        'code':'J2',
        'name':'Taiglo',
        'pts':[(70,170),(90,170),(90,150),(100,150),(100,130),(80,130),(80,150)],
        'connectsto':['J1','H1','H3','K2'],
        'special': None,
        'center': (85,140),
        },
    # Bay
    {
        'code':'K1',
        'name':'Diinsoor',
        'pts':[(50,120),(60,120),(70,110),(70,90),(60,80),(55,90),(50,100)],
        'connectsto':['M2','K2','K3','L1','N2','N1','M3'],
        'special': None,
        'center': (55,105),
        },
    {
        'code':'K2',
        'name':'Baidoa',
        'pts':[(60,120),(60,130),(80,130),(100,130),(100,120),(100,110),(70,110)],
        'connectsto':['M2','J1','J2','H3','L3','K3','K1'],
        'special': None,
        'center': (75,115),
        },
    {
        'code':'K3',
        'name':'Buur Hakaba',
        'pts':[(70,110),(100,110),(92,104.5),(80,96.6),(70,90)],
        'connectsto':['K1','K2','L3','L2','L1'],
        'special': None,
        'center': (75,105),
        },
    #Lower Shabele
    {
        'code':'L1',
        'name':'Haaway',
        'pts':[(60,80),(70,90),(80,96.6),(93,79),(74,66)],
        'connectsto':['N2','K1','K3','L2'],
        'special': None,
        'center': (75,75),
        },
    {
        'code':'L2',
        'name':'Marka',
        'pts':[(80,96.6),(92,104.5), (102,90), (102,85),(93,79)],
        'connectsto':['L1','K3','L3'],
        'special': None,
        'center': (90,92),
        },
    {
        'code': 'L3',
        'name': 'Wanlaweyn',
        'pts': [(92,104.5), (100, 110), (100, 120), (110, 120), (110, 90), (102, 90), ],
        'connectsto': ['K2','K3','H3','I2','L2'],
        'special': None,
        'center': (98, 102),
    },

    {
        'code':'M1',
        'name':'El Beru Hagia',#'West Gedo',
        'pts':[(10,120),(30,150),(30,120),(30,100),(10,100)],
        'connectsto':['M2','M3','N1'],
        'special': None,
        'center': (15,110),
        },
    {
        'code':'M2',
        'name':'Garbahaarey',#'North Gedo',
        'pts':[(30,150),(50,150),(60,140),(60,130),(60,120),(50,120),(30,120)],
        'connectsto':['M1','J1','K2','K1','M3'],
        'special': None,
        'center': (40,130),
        },
    {
        'code':'M3',
        'name':'Bardheere',#'South Gedo',
        'pts':[(30,120),(50,120),(50,100),(30,100)],
        'connectsto':['M1','M2','K1','N1'],
        'special': None,
        'center': (35,108),
        },
    {
        'code':'N1',
        'name':'Juba River', #West Middle Juba
        'pts':[(10,100),(30,100),(50,100),(55,90),(40,80),(20,80),(10,80)],
        'connectsto':['M1','M3','K1','N2','O2','O1'],
        'special': None,
        'center': (30,90),
        },
    {
        'code':'N2',
        'name':'Buaale', #East Middle Juba
        'pts':[(40,80),(55,90),(60,80),(74,66),(50,50),(40,60)],
        'connectsto':['N1','K1','L1','O3','O2'],
        'special': None,
        'center': (50,65),
        },
    {
        'code':'O1',
        'name':'Lag Badana',#West Lower Juba
        'pts':[(10,80),(20,80),(20,60),(35,30),(20,10),(10,30)],
        'connectsto':['N1','O2','O3'],
        'special': None,
        'center': (20,30),
        },
    {
        'code':'O2',
        'name':'Afmadow',#'North Lower Juba',
        'pts':[(20,80),(40,80),(40,60),(20,60)],
        'connectsto':['N1','N2','O3','O1'],
        'special': None,
        'center': (25,65),
        },
    {
        'code':'O3',
        'name':'Kismaayo',#'South Lower Juba',
        'pts':[(20,60),(40,60),(50,50),(35,30)],
        'connectsto':['O1','O2','N2'],
        'special': None,
        'center': (35,45),
        },
    {
        'code':'P1',
        'name':'Degeh Bur',
        'pts':[(100,270),(110,266),(140,254),(140,230),(130,230),(130,220),(100,220)],
        'connectsto':['B1','B3','P3','P2'],
        'special': None,
        'center': (115,240),
    },
    {
        'code':'P2',
        'name':'Kebri Dehar',
        'pts':[(100,220),(130,220),(130,230),(140,230),(140,210),(130,200),(120,190),(100,170)],
        'connectsto':['P1','P3','H1','G1','F1'],
        'special': None,
        'center': (110,200),
        },
    {
        'code':'P3',
        'name':'Werder',
        'pts':[(140,254),(150,250),(160,250),(180,250),(140,210),(140,230)],
        'connectsto':['P1','P2','B3','E2','F1'],
        'special': None,
        'center': (150,235),
        },
]

mogadishu = {
    'name': 'Mogadishu',
    'pts': [(110, 90), (102, 90), (102, 85)],
    'connectsto': [], #None
    'special': None,
    'center': (55, 315),
}


def namecode(place):
#    print place
    return place['name'].replace(' ', '')[:3].upper()

#for p in territories: print namecode(p)


def convert_pt(pt):
    return pt[0]*2.5, (370-pt[1])*2.5

def convert_points(pts):
    return map(convert_pt, pts)

def fmtseg(seg):
    if seg[1] > seg[0]:
        return (seg[1], seg[0])
    return seg

def get_segs(t):
    segs = []
    # Convert each polygon (point set) to a set of line segments.
    for x in range(0, len(t['pts']) - 1):
        segs.append(
            (t['pts'][x], t['pts'][x + 1])
        )
        # Make sure to grab the last one.
    segs.append(
        (t['pts'][len(t['pts']) - 1], t['pts'][0])
    )
    return map(fmtseg,segs)

def external_border(territory_code):
    ts = filter(lambda x: x['code'][0] == territory_code, territories)
    outer_set = set()
    for t in ts:
        outer_set = outer_set ^ set(get_segs(t))
    return outer_set

def seg_len(s):
    dx = abs(s[0][0] - s[1][0])
    dy = abs(s[0][1] - s[1][1])
    return sqrt(dx ** 2 + dy**2)

null_seg = ((0,0),(1,1))

def max_seg(x, y):
    return x if seg_len(x) >= seg_len(y) else y

def best_border(t1,t2):
    x =  reduce(max_seg,set(get_segs(t1)) & set(get_segs(t2)),null_seg)
#    print t1['code'],t2['code'], x
    return x

def border_center(b):
    b = fmtseg(b)
    return (b[0][0]-((b[0][0] - b[1][0]) / 2.0), b[0][1]-((b[0][1] - b[1][1]) / 2.0))

def seg_slope(s):
    dx = s[0][0] - s[1][0]
    dy = s[0][1] - s[1][1]
    return dy/float(dx)

#def border_line(s):
#    slope = -1/seg_slope(s)
#    center = border_center(s)
#    if abs(slope) >= 1:
#        start_x = center[0] / slope
#        start_y = center[1]

all_codes = map(chr, range(ord('A'),ord('P')+1))

def borders(codes=all_codes):
    border_set = set()
    for c in codes:
        border_set |= external_border(c)
    return border_set

#draw_territories = ['A1','A2','C1','C2','D1','D2','B3','E1','E2']
draw_codes = all_codes #map(lambda x: x[0], draw_territories)

somalia = convert_points(somalia)
dwg = svgwrite.Drawing(filename='somalia2.svg', size=(800,1000))
for f in territories:
#    if not f['code'] in draw_territories: continue
    dwg.add(dwg.polygon(points=convert_points(f['pts']), stroke='green', class_='territory', stroke_dasharray='1,1', fill='#f6f6ff',
        onmouseover="evt.target.setAttribute('opacity', '0.5');",
        onmouseout="evt.target.setAttribute('opacity','1)');",
        id="terr_%s" % f['code']))
    dwg.add(dwg.text(f['name'], x=[convert_pt(f['center'])[0]-10], y=[convert_pt(f['center'])[1]], style="font-size:8px;"))

for b in borders(codes=draw_codes):
    dwg.add(dwg.polyline(points=convert_points(b), stroke="orange", stroke_dasharray='1,2', stroke_width='2'))

#dwg.add(dwg.polyline(points=convert_points(compute_border('D')), stroke_dasharray='3,5', stroke_width=2, stroke='blue', fill='none'))
#dwg.add(dwg.polyline(points=convert_points(compute_border('E')), stroke_dasharray='3,5', stroke_width=2, stroke='blue', fill='none'))

dwg.add(dwg.polygon(points=convert_points(mogadishu['pts']), stroke='green', fill='#0000aa'))
dwg.add(dwg.polygon(points=somalia, stroke='blue', fill='none', stroke_width=2))

for t in territories:
    for c in t['connectsto']:
        for x in territories:
            if x['code'] == c:
                x,y = convert_pt(border_center(best_border(t,x)))
                dwg.add(dwg.text('x', x=[x-3], y=[y+5]))

#print "A-OK"

dwg.save()