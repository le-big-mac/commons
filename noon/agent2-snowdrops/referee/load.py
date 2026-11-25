"""Referee loader: reads the raw DWD files. Written blind (before opening snowdrops.py)."""
import sys, datetime, collections
import numpy as np

D = '/home/agent2/downloads/dwd-phenology/'
REC = D + 'PH_Jahresmelder_Wildwachsende_Pflanze_Schneegloeckchen_1925_2024_hist.txt'
STA = D + 'PH_Beschreibung_Phaenologie_Stationen_Jahresmelder.txt'


def read_records():
    rows = []
    bad = []
    with open(REC, encoding='latin-1', newline='') as f:
        header = f.readline()
        for ln, line in enumerate(f, start=2):
            parts = [p.strip() for p in line.rstrip('\r\n').split(';')]
            if len(parts) < 8 or parts[0] == '':
                bad.append((ln, line))
                continue
            try:
                sid, yr, qn, obj, ph, date, qb, jul = (int(x) for x in parts[:8])
            except ValueError:
                bad.append((ln, line))
                continue
            rows.append((sid, yr, qn, obj, ph, date, qb, jul))
    return header, np.array(rows, dtype=np.int64), bad


def read_stations():
    st = {}
    bad = []
    with open(STA, encoding='latin-1', newline='') as f:
        header = f.readline()
        for ln, line in enumerate(f, start=2):
            parts = [p.strip() for p in line.rstrip('\r\n').split(';')]
            if len(parts) < 5 or parts[0] == '':
                bad.append((ln, line))
                continue
            try:
                sid = int(parts[0]); lat = float(parts[2]); lon = float(parts[3]); alt = float(parts[4])
            except ValueError:
                bad.append((ln, line))
                continue
            if sid in st:
                bad.append((ln, 'DUP ' + line))
            st[sid] = (parts[1], lat, lon, alt, parts[9] if len(parts) > 9 else '', parts[10] if len(parts) > 10 else '')
    return header, st, bad


def read_temp(month):
    fn = D + 'regional_averages_tm_%02d.txt' % month
    out = {}
    with open(fn, encoding='latin-1') as f:
        f.readline()
        hdr = [h.strip() for h in f.readline().rstrip('\r\n').split(';')]
        k = hdr.index('Deutschland')
        for line in f:
            p = [x.strip() for x in line.rstrip('\r\n').split(';')]
            if len(p) <= k or not p[0]:
                continue
            assert int(p[1]) == month, line
            out[int(p[0])] = float(p[k])
    return out


def true_doy(refyear, date):
    """Days from 31 Dec of (refyear-1): 1 Jan of refyear = 1. Returns None for an invalid date."""
    y, m, d = date // 10000, (date // 100) % 100, date % 100
    try:
        dt = datetime.date(y, m, d)
    except ValueError:
        return None
    return (dt - datetime.date(refyear, 1, 1)).days + 1
